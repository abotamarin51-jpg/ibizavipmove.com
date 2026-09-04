from pathlib import Path

ROOT=Path('_site')
PAGE=ROOT/'private-concierge-ibiza'/'index.html'

if not PAGE.exists():
    raise SystemExit('Phase 88 private concierge page missing')

html=PAGE.read_text(encoding='utf-8')
if 'ivm-concierge-standards' in html:
    raise SystemExit('Phase 88 duplicate concierge standards section')

marker='<section class="dark-panel ivm-service-area">'
if marker not in html:
    raise SystemExit('Phase 88 service-area marker missing')

section='''<section class="editorial ivm-concierge-standards">
<div><div class="kicker dark">Choosing a concierge in Ibiza</div><h2>What good private coordination should look like.</h2></div>
<div>
<p class="large">The value of a private concierge is not measured by the length of a supplier list. It is measured by whether the right information reaches the right people at the right time, with clear ownership of the itinerary.</p>
<p>For a private client, PA or family office, four things matter especially. First, there should be one accountable point of contact who understands the wider stay rather than one isolated booking. Second, timings, deposits, cancellation terms and access conditions should be confirmed in writing before a request is treated as secured. Third, transport, villa, marina, dining, nightlife, security and aviation movements should be considered together whenever they affect each other. Fourth, a concierge should distinguish clearly between what is requested, what is being checked and what is actually confirmed.</p>
<p>We do not describe third-party availability as guaranteed and we do not promise that money can override venue, operator, property or legal requirements. That distinction is particularly important in peak season, when the quality of coordination often matters more than the number of requests being made.</p>
<p>If you are comparing concierge support for an Ibiza stay, ask who will own the brief, how confirmations are documented, what happens when the itinerary changes and whether the team can coordinate the island logistics around the same schedule. You can also review <a href="/about/">how Ibiza VIP Move works</a> or <a href="/contact/">send the initial brief</a> directly.</p>
</div>
</section>'''

html=html.replace(marker,section+marker,1)
PAGE.write_text(html,encoding='utf-8')

print('PASS: Phase 88 private concierge decision depth — clear selection criteria, confirmation standards and non-guarantee positioning added without new claims')
