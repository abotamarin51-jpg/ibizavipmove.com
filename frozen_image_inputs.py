"""Read the reviewed legacy image inputs without contacting image providers."""
import argparse
import hashlib
import json
from pathlib import Path
import re


ASSET_ROOT = Path(__file__).resolve().parent / 'editorial-assets/legacy'


def manifest():
    data = json.loads((ASSET_ROOT / 'manifest.json').read_text(encoding='utf-8'))
    if data.get('version') != 1 or not isinstance(data.get('stages'), dict):
        raise SystemExit('Frozen image manifest is invalid')
    return data['stages']


def read_image(stage, name, *, source_url=None):
    stages = manifest()
    if stage not in stages or name not in stages[stage]:
        raise SystemExit(f'Frozen image is not registered: {stage}/{name}')
    if not re.fullmatch(r'[a-z][a-z-]*\.jpg', name):
        raise SystemExit(f'Frozen image name is invalid: {name}')
    record = stages[stage][name]
    if source_url is not None and record.get('source_url') != source_url:
        raise SystemExit(f'Frozen image source mismatch: {stage}/{name}')
    path = (ASSET_ROOT / record['file']).resolve()
    if not path.is_relative_to(ASSET_ROOT.resolve()) or not path.is_file():
        raise SystemExit(f'Frozen image missing: {stage}/{name}')
    data = path.read_bytes()
    if (not data or len(data) != record['bytes']
            or hashlib.sha256(data).hexdigest() != record['sha256']):
        raise SystemExit(f'Frozen image mismatch: {stage}/{name}')
    return data


def copy_stage(stage, target):
    stages = manifest()
    if stage not in stages or not stages[stage]:
        raise SystemExit(f'Frozen image stage is not registered: {stage}')
    # Validate the whole stage before changing any generated output.
    images = {name: read_image(stage, name) for name in stages[stage]}
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    for name, data in images.items():
        (target / name).write_bytes(data)
    return images


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage')
    parser.add_argument('target', type=Path)
    args = parser.parse_args()
    images = copy_stage(args.stage, args.target)
    print(f'PASS: {len(images)} verified frozen images copied for {args.stage}')
