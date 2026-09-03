from pathlib import Path
import re

ROOT=Path('_site')
STYLE='/assets/phase38.css?v=38'
CSS_SRC=Path('phase38.css')
CSS_DEST=ROOT/'assets'/'phase38.css'
WA='https://wa.me/34600703303'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'),encoding='utf-8')
page=ROOT/'about'/'index.html'
if not page.exists(): raise SystemExit('About page missing')
html=page.read_text(encoding='utf-8')

main=f'''<main id="main-content">
<section class="page-hero">
  <div class="page-hero-media"><img src="/assets/images/hero-desktop.jpg" alt="Ibiza VIP Move private concierge philosophy in Ibiza" width="2200" height="1400" fetchpriority="high" decoding="async"></div>
  <div><div class="kicker light">About Ibiza VIP Move</div><h1>The island changes quickly.<br>Our standards do not.</h1><p>Private concierge and lifestyle coordination built around discretion, clarity, responsiveness and local judgement.</p><a class="btn gold" href="/contact/">Request Concierge</a>
  <div class="ivm-about-statement"><span>Private by design</span><p>Our role is simple: understand the brief, connect the right moving parts and keep the client out of unnecessary operational friction.</p></div></div>
</section>
<section class="ivm-about-role"><div class="ivm-about-role-inner">
  <div><div class="eyebrow">Our role</div><h2>Less noise.<br>Better coordination.</h2></div>
  <div><p class="lead">Ibiza VIP Move is built for clients and representatives who value time, privacy and a clear line of communication.</p><p>We do not try to turn every stay into a long list of options. We clarify what matters, coordinate the relevant confirmed services and keep the practical details connected as the itinerary evolves.</p><div class="ivm-about-role-rule"><div><span>01</span><strong>Understand the brief</strong></div><div><span>02</span><strong>Align the details</strong></div><div><span>03</span><strong>Stay responsive</strong></div></div></div>
</div></section>
<section class="ivm-about-principles"><div class="ivm-about-principles-inner">
  <div class="ivm-about-principles-head"><div><div class="eyebrow">Operating principles</div><h2>Quiet standards behind every request.</h2></div><p>The luxury is not more communication, more suppliers or more complexity. It is having the right details handled clearly, privately and at the right time.</p></div>
  <div class="ivm-about-principle-grid">
    <article><span>01</span><h3>Discretion</h3><p>Private information is handled on a need-to-know basis around the confirmed service and operational requirement.</p></article>
    <article><span>02</span><h3>Clarity</h3><p>Availability, scope, timing and relevant terms are clarified before a request is treated as confirmed.</p></article>
    <article><span>03</span><h3>Responsiveness</h3><p>Ibiza plans can move quickly. The coordination structure should make changes easier to manage, not harder.</p></article>
    <article><span>04</span><h3>Restraint</h3><p>We favour the right solution over unnecessary choice and keep the client experience as simple as possible.</p></article>
  </div>
</div></section>
<section class="ivm-about-promise"><div class="ivm-about-promise-inner"><div><h2>One trusted contact for the island.</h2></div><div><p>From a single chauffeur request to a multi-day private stay involving villas, yachts, aviation, access, security and lifestyle support, the same principle applies: one clear brief, connected execution and discreet communication.</p><div class="ivm-about-actions"><a class="btn dark" href="/contact/">Start a Private Brief</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div></div></section>
</main>'''

html,n=re.subn(r'<main\b[^>]*>.*?</main>',main,html,count=1,flags=re.I|re.S)
if n!=1: raise SystemExit('Unable to replace About main')
body=re.search(r'<body(?:\s+class="([^"]*)")?>',html,re.I)
if body:
    classes=(body.group(1) or '').split()
    if 'ivm-about-signature' not in classes: classes.append('ivm-about-signature')
    repl='<body class="'+' '.join(x for x in classes if x)+'">'
    html=html[:body.start()]+repl+html[body.end():]
if STYLE not in html: html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
page.write_text(html,encoding='utf-8')

final=page.read_text(encoding='utf-8')
assert CSS_DEST.exists() and CSS_DEST.stat().st_size>4000
assert STYLE in final and 'ivm-about-signature' in final
assert final.count('<h1')==1
assert 'Operating principles' in final and 'Discretion' in final and 'Responsiveness' in final
assert '<link rel="canonical"' in final and 'application/ld+json' in final
assert 'id="main-content"' in final and 'ivm-skip-link' in final
print('PASS: Phase 38 About page upgraded to brand-authority experience')
