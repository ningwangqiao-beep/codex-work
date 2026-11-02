# Read-only scheduler review

Reviewed runner.py and continue_queue.py; no scheduler/source/process modifications, no second GPU process launched. Findings are static code findings, not destructive reproduction against active training.

1. High: runner.py lines 30-35 lock scoped to run_dir. Different directories can each own a valid lock and launch simultaneous GPU jobs. Add project-level GPU lease with owner identity and child lifetime protection.
2. High: lines 41-47 skip completed jobs before fingerprint checks. State job ids are not bound to script, args, queue or data identity. Editing a completed job under same id silently reuses stale success. Store/compare a canonical task digest before skip.
3. Medium: lines 77-80 release lock on monitoring exception without ensuring active child is stopped or remains under an explicit orphan lease. Disk/log failure can leave uncontrolled training. Preserve child ownership; never release the resource lease while child lives.
4. Medium: line 55 interpolates unrestricted job id into log path without inside check. A ../ job id escapes run_dir. Restrict id to safe slug or resolve/check directory containment.
5. Medium: gpu() returns error dictionary and lines 64-65 substitute zeros, continuing with no effective GPU thermal/memory protection. Require retry budget and stop/checkpoint on persistent monitoring failure. Preflight GPU limits before launch as well.
6. Medium: max_hours resets on restart (line 38), checked only after launch; checkpoint resume is not automatic (same argv line 56). Retain absolute deadline and define explicit resume contracts. Cooperative checkpoint stop is marked failed and prevents continuation; distinguish paused/recoverable from fatal failure.
7. Medium: child.terminate targets immediate process only, not Windows spawn workers. Use a Windows job object for descendant lifetime ownership; do not use broad process-name termination.
8. Low: continue_queue has no bounded wait or captured expected queue/state identity, and can follow stale completed state if passed wrong prior file. Bind expected previous queue digest and use bounded heartbeat semantics.

Windows liveness: current implementation uses PROCESS_QUERY_LIMITED_INFORMATION and GetExitCodeProcess, closes handle; it does not signal/terminate target process. Access denied is treated as dead, and PID reuse is not detected; stronger locks should store creation time as well as PID. No liveness test was run by B against live training because parent already verified it.

Suggested safe sequence: finish currently running child, patch scheduler, then use short CPU-only fixtures for changed queue identity, two different run-dir lock competition, failed monitor/orphan lifetime, checkpoint resume and path validation. Existing rule files remain frozen.
