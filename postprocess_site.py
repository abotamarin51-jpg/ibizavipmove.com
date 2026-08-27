from pathlib import Path

ROOT = Path('_site')

favicon_tags = '''<link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/brand-mark.svg"><meta name="theme-color" content="#090e13"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="en_GB"><meta name="twitter:title" content="Ibiza VIP Move"><meta name="twitter:description" content="Private concierge, chauffeur and luxury lifestyle management in Ibiza."><meta name="twitter:image" content="https://ibizavipmove.com/assets/images/villa.jpg">'''

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if 'rel="icon"' not in text:
        text = text.replace('</head>', favicon_tags + '</head>')
    text = text.replace('href="/assets/premium.css?v=1"', 'href="/assets/premium.css?v=4"')
    text = text.replace('src="/assets/premium.js?v=1"', 'src="/assets/premium.js?v=4"')
    path.write_text(text, encoding='utf-8')

not_found = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Ibiza VIP Move</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/premium.css?v=4"></head><body style="background:#090e13;color:#fff;min-height:100vh;display:grid;place-items:center;margin:0"><main style="text-align:center;padding:32px;max-width:760px"><img src="/assets/brand-logo.svg" alt="Ibiza VIP Move" style="width:min(420px,80vw);height:auto;margin:0 auto 54px"><div class="kicker light">404 · Ibiza VIP Move</div><h1 style="color:#fff;font-size:clamp(54px,9vw,100px)">This page has moved.</h1><p style="color:rgba(255,255,255,.65);max-width:560px;margin:28px auto">Return to the private side of Ibiza or contact our concierge team directly.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn gold" href="/">Return home</a><a class="btn ghost" href="https://wa.me/34613756211">WhatsApp Concierge</a></div></main></body></html>'''
(ROOT/'404.html').write_text(not_found, encoding='utf-8')
