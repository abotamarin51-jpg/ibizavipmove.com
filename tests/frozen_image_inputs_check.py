"""Exercise the actual image build stages with all network access unavailable."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
import frozen_image_inputs as frozen


@contextmanager
def isolated_inputs():
    with tempfile.TemporaryDirectory(prefix='ivm-frozen-inputs-') as directory:
        root = Path(directory)
        inputs = root / 'inputs'
        shutil.copytree(frozen.ASSET_ROOT, inputs)
        with patch.object(frozen, 'ASSET_ROOT', inputs), \
             patch('urllib.request.urlopen', side_effect=AssertionError('Network unavailable')) as request, \
             patch('socket.create_connection', side_effect=AssertionError('Network unavailable')) as connect:
            try:
                yield root, inputs
            finally:
                request.assert_not_called()
                connect.assert_not_called()


class FrozenImageInputs(unittest.TestCase):
    def test_corrupt_stage_does_not_overwrite_any_output(self):
        with isolated_inputs() as (root, inputs):
            record = frozen.manifest()['initial']['bespoke.jpg']
            source = inputs / record['file']
            damaged = bytearray(source.read_bytes())
            damaged[-1] ^= 1
            source.write_bytes(damaged)
            output = root / 'output'
            output.mkdir()
            (output / 'hero.jpg').write_bytes(b'previous output')
            with self.assertRaisesRegex(SystemExit, 'Frozen image mismatch: initial/bespoke.jpg'):
                frozen.copy_stage('initial', output)
            self.assertEqual([p.name for p in output.iterdir()], ['hero.jpg'])
            self.assertEqual((output / 'hero.jpg').read_bytes(), b'previous output')

    def test_missing_input_has_no_network_fallback(self):
        with isolated_inputs() as (root, inputs):
            record = frozen.manifest()['secondary']['private-office.jpg']
            (inputs / record['file']).unlink()
            output = root / 'output'
            with self.assertRaisesRegex(SystemExit, 'Frozen image missing: secondary/private-office.jpg'):
                frozen.copy_stage('secondary', output)
            self.assertFalse(output.exists())

    def test_changed_source_url_requires_a_reviewed_input(self):
        with isolated_inputs():
            with self.assertRaisesRegex(SystemExit, 'Frozen image source mismatch: secondary/security.jpg'):
                frozen.read_image('secondary', 'security.jpg', source_url='https://example.invalid/new.jpg')

    def test_actual_image_pipeline_works_offline_and_preserves_final_jpegs(self):
        with tempfile.TemporaryDirectory(prefix='ivm-offline-image-build-') as directory:
            root = Path(directory)
            repo = root / 'repo'
            shutil.copytree(REPO, repo, ignore=shutil.ignore_patterns('.git', '_site', '__pycache__'))
            guard = root / 'network-disabled'
            guard.mkdir()
            (guard / 'sitecustomize.py').write_text(
                'import socket, urllib.request\n'
                'def unavailable(*args, **kwargs):\n'
                '    raise AssertionError("Network unavailable in image build check")\n'
                'socket.create_connection = unavailable\n'
                'socket.socket.connect = unavailable\n'
                'urllib.request.urlopen = unavailable\n')
            for name in ('curl', 'wget'):
                shim = guard / name
                shim.write_text('#!/bin/sh\necho "Network unavailable in image build check" >&2\nexit 86\n')
                shim.chmod(0o755)
            env = os.environ.copy()
            env['PYTHONPATH'] = str(guard)
            env['PATH'] = str(guard) + os.pathsep + env.get('PATH', '')
            commands = [['bash', 'build_site.sh']]
            scripts = ('upgrade_visual_assets.py', 'phase11_enhance.py', 'phase12_enhance.py',
                       'phase13_enhance.py', 'phase14_enhance.py', 'phase16_enhance.py',
                       'phase15_enhance.py', 'phase17_enhance.py', 'phase18_enhance.py',
                       'phase19_enhance.py', 'phase101_enhance.py', 'phase101_image_performance_audit.py')
            commands.extend([sys.executable, script] for script in scripts)
            for command in commands:
                result = subprocess.run(command, cwd=repo, env=env, text=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
                self.assertEqual(result.returncode, 0, f'{command}:\n{result.stdout[-3500:]}')
            expected = {p.name: p for p in (repo / 'editorial-assets/performance').glob('*.jpg')}
            expected.update({name: repo / 'editorial-assets' / name for name in ('villa.jpg', 'chauffeur.jpg')})
            records = json.loads((repo / 'editorial-assets/legacy/manifest.json').read_text())['stages']['secondary']
            expected.update({name: repo / 'editorial-assets/legacy' / records[name]['file']
                             for name in ('security.jpg', 'wellness.jpg', 'bespoke.jpg', 'private-office.jpg')})
            self.assertEqual(len(expected), 14)
            for name, source in expected.items():
                published = repo / '_site/assets/images' / name
                self.assertEqual(hashlib.sha256(published.read_bytes()).digest(),
                                 hashlib.sha256(source.read_bytes()).digest(), name)


if __name__ == '__main__':
    unittest.main()
