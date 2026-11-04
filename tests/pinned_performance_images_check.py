"""Keep the reviewed images available offline and reject damaged frozen assets."""
from contextlib import contextmanager, redirect_stdout
import io
import os
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
STAGE = REPO / 'phase101_enhance.py'
ASSETS = ('villa.jpg', 'chauffeur.jpg', 'hero.jpg', 'yacht.jpg', 'nightlife.jpg',
          'events.jpg', 'chef.jpg', 'aviation.jpg', 'hero-desktop.jpg', 'hero-mobile.jpg')


@contextmanager
def fixture():
    with tempfile.TemporaryDirectory(prefix='ivm-pinned-images-') as directory:
        root = Path(directory)
        shutil.copytree(REPO / 'editorial-assets', root / 'editorial-assets')
        targets = root / '_site/assets/images'
        targets.mkdir(parents=True)
        expected = {}
        for name in ASSETS:
            source = root / 'editorial-assets'
            if name not in ('villa.jpg', 'chauffeur.jpg'):
                source /= 'performance'
            expected[name] = (source / name).read_bytes()
            # Simulate larger inputs from the earlier build stages.
            (targets / name).write_bytes(expected[name] + b'\0' * 100)
        home = root / '_site/index.html'
        home.write_text('<main><img src="/assets/images/hero-desktop.jpg" '
                        'width="2400" height="1528" fetchpriority="high"></main>')
        previous = Path.cwd()
        os.chdir(root)
        try:
            yield root, targets, expected
        finally:
            os.chdir(previous)


def run_offline():
    # A network fallback would reproduce the outage that blocked the release.
    with patch('urllib.request.urlopen', side_effect=AssertionError('Network unavailable')) as request, \
         patch('socket.create_connection', side_effect=AssertionError('Network unavailable')) as connect, \
         redirect_stdout(io.StringIO()):
        try:
            runpy.run_path(str(STAGE), run_name='__main__')
        finally:
            request.assert_not_called()
            connect.assert_not_called()


class FrozenPerformanceImages(unittest.TestCase):
    def test_approved_images_and_hero_dimensions_work_without_network(self):
        with fixture() as (root, targets, expected):
            run_offline()
            self.assertEqual(set(p.name for p in targets.iterdir()), set(ASSETS))
            for name, data in expected.items():
                self.assertEqual((targets / name).read_bytes(), data, name)
            self.assertEqual((root / '_site/index.html').read_text(),
                             '<main><img src="/assets/images/hero-desktop.jpg" '
                             'width="2000" height="1273" fetchpriority="high"></main>')

    def test_same_size_corruption_is_rejected_without_network_fallback(self):
        with fixture() as (root, targets, expected):
            name = 'hero-mobile.jpg'
            damaged = bytearray(expected[name])
            damaged[-1] ^= 1
            (root / 'editorial-assets/performance' / name).write_bytes(damaged)
            untouched = (targets / name).read_bytes()
            with self.assertRaisesRegex(SystemExit, 'hero-mobile.jpg production-baseline mismatch'):
                run_offline()
            self.assertEqual((targets / name).read_bytes(), untouched)

    def test_missing_frozen_image_is_rejected_without_network_fallback(self):
        with fixture() as (root, targets, _):
            name = 'aviation.jpg'
            (root / 'editorial-assets/performance' / name).unlink()
            untouched = (targets / name).read_bytes()
            with self.assertRaisesRegex(SystemExit, 'frozen performance image missing: aviation.jpg'):
                run_offline()
            self.assertEqual((targets / name).read_bytes(), untouched)


if __name__ == '__main__':
    unittest.main()
