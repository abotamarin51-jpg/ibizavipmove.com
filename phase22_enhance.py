from pathlib import Path
import shutil

ROOT = Path('_site')
SOURCE_CSS = Path('premium-motion.css')
TARGET_CSS = ROOT / 'assets' / 'premium-motion.css'

if not SOURCE_CSS.exists():
    raise SystemExit('premium-motion.css source missing')
TARGET_CSS.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE_CSS, TARGET_CSS)

link = '<link rel="stylesheet" href="/assets/premium-motion.css?v=22">'
count = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '</head>' not in text:
        continue
    if '/assets/premium-motion.css?v=22' not in text:
        text = text.replace('</head>', link + '</head>', 1)
        path.write_text(text, encoding='utf-8')
        count += 1

premium_js = ROOT / 'assets' / 'premium.js'
if not premium_js.exists():
    raise SystemExit('premium.js missing from built site')
js = premium_js.read_text(encoding='utf-8')
checks = {
    'scroll header': "classList.toggle('is-scrolled'" in js,
    'intersection observer': 'IntersectionObserver' in js,
    'reduced motion': 'prefers-reduced-motion: reduce' in js,
    'motion css copied': TARGET_CSS.exists() and TARGET_CSS.stat().st_size > 500,
    'home motion css': '/assets/premium-motion.css?v=22' in (ROOT / 'index.html').read_text(encoding='utf-8'),
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if failed:
    raise SystemExit('Phase 22 validation failed: ' + ', '.join(failed))
print(f'PASS: Phase 22 premium motion linked into {count} HTML pages')
