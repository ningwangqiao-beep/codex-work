"""Isolated CPU control test; scoped mocked admission never changes production gate."""
import contextlib
import io
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import torch
from training import next_scale_supervised as scale
from training import next_relative_supervised as reference

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ScaleTrainingTest(unittest.TestCase):
    def test_stream_labels_stop_resume(self):
        torch.set_num_threads(2)
        manifest = ROOT / 'datasets/next_history_scale_smoke_v2/manifest.json'
        m = json.loads(manifest.read_text())
        rows = list(scale.records(list(reversed(m['shards']['train']))))
        self.assertEqual(len(rows), 44)
        self.assertEqual([r['seed'] for r in rows], sorted(r['seed'] for r in rows))
        original_manifest = json.loads((ROOT/'datasets/next_history100/manifest.json').read_text())
        for split in ('train', 'validation'):
            scaled = list(scale.records(m['shards'][split]))
            seeds = {r['seed'] for r in scaled}
            original = [r for r in reference.records(original_manifest['files'][split]) if r['seed'] in seeds]
            self.assertEqual(scaled, original)  # Actual old file order, not a synthesized copy.
        a, at, am = scale.collate(rows[:8], 'cpu')
        b, bt, bm = reference.collate(rows[:8], 'cpu')
        self.assertTrue(all(torch.equal(x, y) for x, y in zip(a, b)))
        self.assertEqual(am, bm)
        self.assertEqual(set(at), set(bt))
        self.assertTrue(all(torch.equal(at[k], bt[k]) for k in at))
        with tempfile.TemporaryDirectory(prefix='next_c_scale_cpu_', dir=ROOT/'reports') as temp:
            temp = pathlib.Path(temp)
            admission = temp/'admission.json'
            admission.write_text(json.dumps({'max_epochs': 2, 'max_batch_size': 8}))
            # Only this test process injects an explicit synthetic admission return.
            # No formal gate/source/manifest file is patched on disk.
            audit = {'training_allowed': True, 'TEST_ONLY': True, 'rl_allowed': False}
            flat = temp/'train.jsonl'
            flat.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            self.assertEqual(list(reference.records(flat)), rows)
            full, interrupted, old = temp/'full', temp/'interrupted', temp/'old_control'
            flatval = temp/'validation.jsonl'
            flatval.write_text(''.join(json.dumps(r)+'\n' for r in scale.records(m['shards']['validation'])))
            oldmanifest = temp/'old_manifest.json'
            oldmanifest.write_text(json.dumps({**m, 'files': {'train': str(flat), 'validation': str(flatval)}}))
            stop = temp/'STOP'
            with patch.object(scale, 'validate_next_manifest', return_value=audit), patch.object(scale, 'resources', return_value={'TEST_ONLY': True}), contextlib.redirect_stdout(io.StringIO()):
                scale.train(manifest, admission, full, ROOT, 2, 8, 42, 'cpu')
                with patch.object(reference, 'validate_next_manifest', return_value=audit), patch.object(reference, 'resources', return_value={'TEST_ONLY': True}):
                    reference.train(oldmanifest, admission, old, ROOT, 2, 8, 42, 'cpu')
                original_step = torch.optim.Adam.step
                calls = 0
                def step(optimizer, *args, **kwargs):
                    nonlocal calls
                    result = original_step(optimizer, *args, **kwargs)
                    calls += 1
                    if calls == 2:
                        stop.write_text('test stop after two real optimizer updates')
                    return result
                with patch.dict(os.environ, {'MAHJONG_STOP_FILE': str(stop)}), patch.object(torch.optim.Adam, 'step', step):
                    with self.assertRaises(SystemExit) as stopped:
                        scale.train(manifest, admission, interrupted, ROOT, 2, 8, 42, 'cpu')
                self.assertEqual(stopped.exception.code, 75)
                saved = torch.load(interrupted/'last.pt', weights_only=False)
                self.assertEqual(saved['optimizer_steps'], 2)
                self.assertEqual(saved['next_batch_index'], 2)
                self.assertFalse(saved['epoch_complete'])
                self.assertEqual(saved['train_epoch_rows'], 16)
                self.assertFalse((interrupted/'COMPLETE.json').exists())
                stop.unlink()
                scale.train(manifest, admission, interrupted, ROOT, 2, 8, 42, 'cpu', True)
                # Completed directories cannot silently be resumed/overwritten.
                with self.assertRaisesRegex(ValueError, 'Completed run immutable'):
                    scale.train(manifest, admission, interrupted, ROOT, 2, 8, 42, 'cpu', True)
            left = torch.load(full/'last.pt', weights_only=False)
            right = torch.load(interrupted/'last.pt', weights_only=False)
            oldstate = torch.load(old/'last.pt', weights_only=False)
            reference_delta = max(float((left['model'][k]-oldstate['model'][k]).abs().max()) for k in left['model'])
            self.assertEqual(reference_delta, 0.)
            delta = max(float((left['model'][k]-right['model'][k]).abs().max()) for k in left['model'])
            self.assertLessEqual(delta, 1e-7)
            self.assertEqual(left['optimizer_steps'], right['optimizer_steps'])
            self.assertEqual(left['optimizer_steps'], 12)
            for key in left['optimizer']['state']:
                for name, value in left['optimizer']['state'][key].items():
                    self.assertTrue(torch.allclose(value, right['optimizer']['state'][key][name], atol=1e-7, rtol=1e-6))
            lm = [json.loads(x) for x in (full/'metrics.jsonl').read_text().splitlines()]
            rm = [json.loads(x) for x in (interrupted/'metrics.jsonl').read_text().splitlines()]
            for x, y in zip(lm, rm):
                for head in x['train_head_loss']:
                    self.assertAlmostEqual(x['train_head_loss'][head], y['train_head_loss'][head], places=6)
                self.assertAlmostEqual(x['validation']['state_v_mae_raw'], y['validation']['state_v_mae_raw'], places=6)
            report = {'passed': True, 'TEST_ONLY_scoped_admission': True, 'formal_training_started': False, 'device': 'cpu', 'train_rows': 44, 'validation_rows': 31, 'epochs': 2, 'batch_size': 8, 'uninterrupted_steps': 12, 'stop_steps': 2, 'stop_exitcode': 75, 'resumed_steps': right['optimizer_steps'], 'model_max_abs_difference': delta, 'optimizer_allclose': True, 'resumed_epoch_loss_totals_preserved': True, 'reference_collate_labels_exact': True, 'reference_stream_order_exact': True}
            report.update(reference_trainer_weight_max_difference=reference_delta, actual_original_file_prefix_order_exact=True, old_and_new_shuffle=False)
            (ROOT/'reports/next_c_scale_training_test.json').write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    unittest.main()
