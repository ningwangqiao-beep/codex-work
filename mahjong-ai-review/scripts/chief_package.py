from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
out=root.parent/'mahjong_ai_audit.zip'
excluded={'.venv','__pycache__','.git','.pytest_cache'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob('*'):
        if p.is_file() and not excluded.intersection(p.relative_to(root).parts) and p.suffix!='.pyc':
            z.write(p,Path('mahjong_brain')/p.relative_to(root))
print(out)
