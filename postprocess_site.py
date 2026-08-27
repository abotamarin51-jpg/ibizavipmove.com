from pathlib import Path

ROOT = Path('_site')

OLD_PHONE_DISPLAY = '+34 613 75 62 11'
OLD_PHONE_TEL = '+34613756211'
OLD_WA = 'https://wa.me/34613756211'
NEW_PHONE_DISPLAY = '+34 600 703 303'
NEW_PHONE_TEL = '+34600703303'
NEW_WA = 'https://wa.me/34600703303'

favicon_tags = '''<link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/brand-mark.svg"><meta name="theme-color" content="#090e13"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="en_GB"><meta name="twitter:title" content="Ibiza VIP Move"><meta name="twitter:description" content="Private concierge, chauffeur and luxury lifestyle management in Ibiza."><meta name="twitter:image" content="https://ibizavipmove.com/assets/images/villa.jpg">'''

old_wordmark = '<a class="wordmark" href="/"><span class="mark">IVM</span><span><strong>IBIZA VIP MOVE</strong><small>PRIVATE CONCIERGE · IBIZA</small></span></a>'
new_wordmark = '<a class="wordmark" href="/" aria-label="Ibiza VIP Move home"><img src="/assets/brand-logo.svg?v=5" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a>'
old_footer_brand = '<div class="footer-brand">IBIZA VIP MOVE</div>'
new_footer_brand = '<div class="footer-brand"><img src="/assets/brand-logo.svg?v=5" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div>'

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')

    # Permanent contact details in generated HTML, metadata and structured data.
    text = text.replace(OLD_PHONE_DISPLAY, NEW_PHONE_DISPLAY)
    text = text.replace(OLD_PHONE_TEL, NEW_PHONE_TEL)
    text = text.replace(OLD_WA, NEW_WA)

    # Render the official logo directly in HTML so it does not depend on JavaScript.
    text = text.replace(old_wordmark, new_wordmark)
    text = text.replace(old_footer_brand, new_footer_brand)

    if 'rel="icon"' not in text:
        text = text.replace('</head>', favicon_tags + '</head>')
    text = text.replace('href="/assets/premium.css?v=1"', 'href="/assets/premium.css?v=5"')
    text = text.replace('src="/assets/premium.js?v=1"', 'src="/assets/premium.js?v=5"')
    path.write_text(text, encoding='utf-8')

not_found = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Ibiza VIP Move</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/premium.css?v=5"></head><body style="background:#090e13;color:#fff;min-height:100vh;display:grid;place-items:center;margin:0"><main style="text-align:center;padding:32px;max-width:760px"><img src="/assets/brand-logo.svg?v=5" alt="Ibiza VIP Move" style="width:min(420px,80vw);height:auto;margin:0 auto 54px"><div class="kicker light">404 · Ibiza VIP Move</div><h1 style="color:#fff;font-size:clamp(54px,9vw,100px)">This page has moved.</h1><p style="color:rgba(255,255,255,.65);max-width:560px;margin:28px auto">Return to the private side of Ibiza or contact our concierge team directly.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn gold" href="/">Return home</a><a class="btn ghost" href="{NEW_WA}">WhatsApp Concierge</a></div></main></body></html>'''
(ROOT/'404.html').write_text(not_found, encoding='utf-8')
