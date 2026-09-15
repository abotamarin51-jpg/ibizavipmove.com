from pathlib import Path
import shutil

ROOT = Path('_site')
SOURCE_ASSET = Path('analytics-consent.js')
TARGET_ASSET = ROOT / 'assets' / 'analytics-consent.js'
SCRIPT_TAG = '<script defer src="/assets/analytics-consent.js?v=1"></script>'
UPDATED = '15 September 2026'

if not ROOT.exists():
    raise SystemExit('_site does not exist; build the site first')
if not SOURCE_ASSET.is_file():
    raise SystemExit('analytics-consent.js is missing from the repository')

TARGET_ASSET.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE_ASSET, TARGET_ASSET)

html_files = list(ROOT.rglob('*.html'))
if not html_files:
    raise SystemExit('No built HTML files found')

injected = 0
for path in html_files:
    text = path.read_text(encoding='utf-8')
    if SCRIPT_TAG not in text:
        if '</body>' not in text:
            raise SystemExit(f'Cannot inject analytics consent script into {path}: missing </body>')
        text = text.replace('</body>', SCRIPT_TAG + '</body>', 1)
        path.write_text(text, encoding='utf-8')
        injected += 1

cookies_path = ROOT / 'cookies' / 'index.html'
privacy_path = ROOT / 'privacy' / 'index.html'

# Some build phases validate the site before legal_pages.py has run. In that
# early pass we install the consent asset and script only. A later validation
# pass patches and verifies the legal pages once they exist.
if cookies_path.is_file() and privacy_path.is_file():
    cookies = cookies_path.read_text(encoding='utf-8')
    cookies = cookies.replace('Last updated · 27 August 2026', f'Last updated · {UPDATED}')

    old_current = (
        'The website does not currently use advertising cookies or an analytics platform that intentionally places '
        'non-essential tracking cookies for visitor profiling. Essential browser or hosting functions may still use '
        'technical mechanisms required to deliver pages securely and reliably.'
    )
    new_current = (
        'With your consent, this website uses Google Analytics 4 (GA4) to understand website usage and improve our '
        'private concierge experience. Google Analytics is not loaded and analytics tracking is not activated unless '
        'you choose to accept analytics cookies. When enabled, analytics may process information such as pages viewed, '
        'interaction events, device and browser information, referral or campaign information and approximate location '
        'derived from network data. Advertising storage and ad-personalisation signals are disabled.'
    )
    if old_current in cookies:
        cookies = cookies.replace(old_current, new_current, 1)

    old_third_party = (
        'The website may connect to third-party services needed for functionality or presentation, including externally '
        'hosted web fonts. If you choose a WhatsApp, email or telephone contact link, your browser or device then '
        'interacts with that external provider under its own terms and privacy practices.'
    )
    new_third_party = (
        'Google Analytics is provided by Google. If you accept analytics cookies, Google may process analytics information '
        'under its own privacy terms and applicable data-transfer mechanisms. The website may also connect to other '
        'third-party services needed for functionality or presentation, including externally hosted web fonts. If you '
        'choose a WhatsApp, email or telephone contact link, your browser or device then interacts with that external '
        'provider under its own terms and privacy practices. You can change your analytics choice at any time using the '
        'Cookie settings control in the website footer.'
    )
    if old_third_party in cookies:
        cookies = cookies.replace(old_third_party, new_third_party, 1)

    old_future = (
        'If non-essential analytics, advertising or other consent-based cookies are introduced in the future, this policy '
        'will be updated and an appropriate consent mechanism will be provided where required by applicable law.'
    )
    new_future = (
        'If our use of analytics or other consent-based technologies changes, this policy and the consent controls will '
        'be updated where required by applicable law.'
    )
    if old_future in cookies:
        cookies = cookies.replace(old_future, new_future, 1)

    # Fallback for future markup changes: add the disclosure before the existing
    # third-party section if the original prose was no longer an exact match.
    if 'Google Analytics 4 (GA4)' not in cookies:
        marker = 'Third-party services</h2>'
        disclosure = '<h2>Analytics cookies</h2><p>' + new_current + '</p>'
        idx = cookies.find(marker)
        if idx == -1:
            raise SystemExit('Could not locate the cookie policy disclosure area')
        heading_start = cookies.rfind('<h2', 0, idx)
        if heading_start == -1:
            raise SystemExit('Could not locate the cookie policy third-party heading')
        cookies = cookies[:heading_start] + disclosure + cookies[heading_start:]

    cookies_path.write_text(cookies, encoding='utf-8')

    privacy = privacy_path.read_text(encoding='utf-8')
    privacy = privacy.replace('Last updated · 27 August 2026', f'Last updated · {UPDATED}')

    if '<h2>Website analytics</h2>' not in privacy:
        marker = '<h2>Service providers and suppliers</h2>'
        analytics_section = (
            '<h2>Website analytics</h2>'
            '<p>If you accept analytics cookies, we use Google Analytics 4 to measure website usage, including page views '
            'and selected interaction events such as concierge, WhatsApp, phone, email and partner-interest clicks. '
            'Analytics is not loaded before consent. Advertising storage and ad-personalisation signals are disabled. '
            'You can withdraw or change your choice at any time using the Cookie settings control in the website footer.</p>'
        )
        if marker not in privacy:
            raise SystemExit('Could not safely update the privacy policy analytics section')
        privacy = privacy.replace(marker, analytics_section + marker, 1)

    privacy_path.write_text(privacy, encoding='utf-8')

# Build guards: every HTML page that exists in this pass must carry the consent
# layer. If legal pages exist already, they must accurately describe GA4.
for path in html_files:
    text = path.read_text(encoding='utf-8')
    if SCRIPT_TAG not in text:
        raise SystemExit(f'Analytics consent script missing from {path}')

if not TARGET_ASSET.is_file() or TARGET_ASSET.stat().st_size == 0:
    raise SystemExit('Analytics consent JavaScript asset was not copied')
if 'G-C21ZKM1V3K' not in TARGET_ASSET.read_text(encoding='utf-8'):
    raise SystemExit('Analytics consent asset is missing the expected GA4 measurement ID')
if cookies_path.is_file():
    cookie_text = cookies_path.read_text(encoding='utf-8')
    if 'Google Analytics 4 (GA4)' not in cookie_text or old_current in cookie_text:
        raise SystemExit('Cookie policy does not accurately describe GA4')
if privacy_path.is_file() and '<h2>Website analytics</h2>' not in privacy_path.read_text(encoding='utf-8'):
    raise SystemExit('Privacy policy does not describe website analytics')

print(f'GA4 consent layer ready on {len(html_files)} HTML files ({injected} newly injected)')
