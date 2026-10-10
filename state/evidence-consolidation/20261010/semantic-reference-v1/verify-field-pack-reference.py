"""Regenerate existing field pack in scratch, compare baseline/current task refs.
No geometry export, production writes, or new visual approval. Output hashes are
comparison-run hashes; renderer versions may differ from the original build.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '727a0248c0234641453a08e4ae3984e27c9f970b'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='ks-field-reference-') as temp:
    dest = Path(temp)
    for folder in ['data', 'public/field-visuals']:
        shutil.copytree(ROOT/folder, dest/folder)
    for file in ['scripts/build-field-pack.py', 'docs/field-kit/model-projections.json.gz', 'state/reconstruction/quality-review.json', 'state/reconstruction-loop/ITER-001/truth-critic/pdf-visual-review.json']:
        if (ROOT/file).is_file():
            (dest/file).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/file,dest/file)
    (dest/'output').mkdir(exist_ok=True)
    (dest/'output/calibration').symlink_to(ROOT/'output/calibration',target_is_directory=True)
    (dest/'evidence').symlink_to(ROOT/'evidence',target_is_directory=True)
    task = dest/'data/field-tasks.json'
    original = subprocess.check_output(['git','-C',str(ROOT),'show',f'{BASE}:data/field-tasks.json'])
    snapshots=[]
    for content in [original,(ROOT/'data/field-tasks.json').read_bytes()]:
        task.write_bytes(content)
        subprocess.run([sys.executable,str(dest/'scripts/build-field-pack.py')],check=True,stdout=subprocess.DEVNULL)
        files={str(p.relative_to(dest)):sha(p) for folder in ['output/pdf','public/field-pack','public/field-visuals'] for p in (dest/folder).rglob('*') if p.is_file()}
        files['data/visual-guides.json']=sha(dest/'data/visual-guides.json')
        snapshots.append({'outputs':files,'manifest':json.loads((dest/'docs/field-kit/field-pack-manifest.json').read_text())})
    before,after=snapshots
    manifest_changes=[k for k in set(before['manifest'])|set(after['manifest']) if before['manifest'].get(k)!=after['manifest'].get(k)]
    passed=before['outputs']==after['outputs'] and manifest_changes==['task_source_sha256']
    result={'baseline':BASE,'purpose':'Existing renderer output equivalence for reference-only TASK-PAD change; no geometry export or new visual review','passed':passed,'byte_identical_output_count':len(after['outputs']),'outputs':after['outputs'],'manifest_changed_keys':manifest_changes,'old_task_source_sha256':hashlib.sha256(original).hexdigest(),'new_task_source_sha256':sha(task)}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if passed else 1)
