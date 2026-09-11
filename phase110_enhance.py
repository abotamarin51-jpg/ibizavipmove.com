from pathlib import Path
from html import escape
import re

ROOT=Path('_site')

SOURCE_LINKS={
'/private-chauffeur-ibiza/':[
    ('/case-studies/principal-chauffeur-security-three-days/','Principal chauffeur + security case','Operational case'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch private concierge','Ibiza area'),
    ('/private-concierge-cala-jondal-es-cubells-ibiza/','Cala Jondal & Es Cubells concierge','Ibiza area'),
],
'/restaurants-nightlife-ibiza/':[
    ('/case-studies/late-night-dual-vehicle-arrival/','Late-night dual-vehicle logistics case','Operational case'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch private concierge','Ibiza area'),
    ('/private-concierge-cala-jondal-es-cubells-ibiza/','Cala Jondal & Es Cubells concierge','Ibiza area'),
],
'/private-aviation-ibiza/':[
    ('/case-studies/private-aviation-arrival-seven-guests/','Seven-guest private aviation arrival case','Operational case'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch private concierge','Ibiza area'),
],
'/private-security-ibiza/':[
    ('/case-studies/principal-chauffeur-security-three-days/','Principal chauffeur + security case','Operational case'),
    ('/private-concierge-cala-jondal-es-cubells-ibiza/','Cala Jondal & Es Cubells concierge','Ibiza area'),
    ('/private-concierge-santa-eulalia-roca-llisa-ibiza/','Santa Eulària & Roca Llisa concierge','Ibiza area'),
],
'/yacht-charter-ibiza/':[
    ('/case-studies/weekend-concierge-two-guests/','Connected weekend concierge case','Operational case'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch private concierge','Ibiza area'),
    ('/private-concierge-cala-jondal-es-cubells-ibiza/','Cala Jondal & Es Cubells concierge','Ibiza area'),
    ('/private-concierge-santa-eulalia-roca-llisa-ibiza/','Santa Eulària & Roca Llisa concierge','Ibiza area'),
],
'/private-chef-staffing-ibiza/':[
    ('/case-studies/weekend-concierge-two-guests/','Connected weekend concierge case','Operational case'),
    ('/private-concierge-santa-gertrudis-ibiza/','Santa Gertrudis private concierge','Ibiza area'),
    ('/private-concierge-santa-eulalia-roca-llisa-ibiza/','Santa Eulària & Roca Llisa concierge','Ibiza area'),
],
'/wellness-ibiza/':[
    ('/case-studies/weekend-concierge-two-guests/','Connected weekend concierge case','Operational case'),
    ('/private-concierge-santa-gertrudis-ibiza/','Santa Gertrudis private concierge','Ibiza area'),
    ('/private-concierge-santa-eulalia-roca-llisa-ibiza/','Santa Eulària & Roca Llisa concierge','Ibiza area'),
],
'/destination-management-ibiza/':[
    ('/case-studies/multi-day-executive-chauffeur-program/','Multi-day executive chauffeur program','Operational case'),
    ('/case-studies/private-aviation-arrival-seven-guests/','Private aviation arrival case','Operational case'),
],
'/international-clients/':[
    ('/case-studies/multi-day-executive-chauffeur-program/','Multi-day executive chauffeur program','Operational case'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch private concierge','Ibiza area'),
],
}

TARGET_BACKLINKS={
'/case-studies/late-night-dual-vehicle-arrival/':[
    ('/restaurants-nightlife-ibiza/','Restaurants, beach clubs & nightlife'),
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/private-concierge-marina-botafoch-ibiza/','Marina Botafoch concierge'),
],
'/case-studies/multi-day-executive-chauffeur-program/':[
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/destination-management-ibiza/','Destination management'),
    ('/international-clients/','International client support'),
],
'/case-studies/principal-chauffeur-security-three-days/':[
    ('/private-security-ibiza/','Private security'),
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/private-client-services-ibiza/','Private client services'),
],
'/case-studies/private-aviation-arrival-seven-guests/':[
    ('/private-aviation-ibiza/','Private aviation'),
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/luxury-travel-concierge-ibiza/','Luxury travel concierge'),
],
'/case-studies/weekend-concierge-two-guests/':[
    ('/private-concierge-ibiza/','Private concierge'),
    ('/luxury-villas-ibiza/','Luxury villas'),
    ('/yacht-charter-ibiza/','Yachts & charters'),
],
'/private-concierge-marina-botafoch-ibiza/':[
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/restaurants-nightlife-ibiza/','Dining & nightlife'),
    ('/yacht-charter-ibiza/','Yachts & charters'),
],
'/private-concierge-cala-jondal-es-cubells-ibiza/':[
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/restaurants-nightlife-ibiza/','Beach clubs & nightlife'),
    ('/yacht-charter-ibiza/','Yachts & charters'),
],
'/private-concierge-santa-eulalia-roca-llisa-ibiza/':[
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/private-security-ibiza/','Private security'),
    ('/wellness-ibiza/','Wellness & beauty'),
],
'/private-concierge-santa-gertrudis-ibiza/':[
    ('/private-chauffeur-ibiza/','Private chauffeur'),
    ('/private-chef-staffing-ibiza/','Private chef & villa staffing'),
    ('/wellness-ibiza/','Wellness & beauty'),
],
}


def page(path):
    return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'


def source_section(items):
    cards=''.join(
        '<a class="ivm-phase110-card" href="'+escape(href,quote=True)+'">'
        '<span>'+escape(kind)+'</span><strong>'+escape(label)+'</strong><b>Explore →</b></a>'
        for href,label,kind in items
    )
    return '<section class="ivm-phase110-flow" aria-label="Related Ibiza operating context"><div class="section-head"><div class="kicker dark">Related Ibiza operating context</div><h2>See the service in context.</h2><p>Explore relevant operating cases and Ibiza service areas connected to this type of brief.</p></div><div class="ivm-phase110-grid">'+cards+'</div></section>'


def target_section(items):
    links=''.join('<a class="text-link" href="'+escape(href,quote=True)+'">'+escape(label)+' →</a>' for href,label in items)
    return '<section class="ivm-phase110-return" aria-label="Relevant private services"><div><div class="kicker dark">Continue the brief</div><h2>Relevant service pathways.</h2><p>These are the commercial service pages most closely connected to this operating context.</p><div class="ivm-phase110-links">'+links+'</div></div></section>'

for path,items in SOURCE_LINKS.items():
    target=page(path)
    if not target.exists(): raise SystemExit(f'Phase 110 source missing: {path}')
    html=target.read_text(encoding='utf-8')
    if 'ivm-phase110-flow' in html: raise SystemExit(f'Phase 110 duplicate source module: {path}')
    block=source_section(items)
    marker='<section class="partners-strip ivm-phase105-proof"'
    if marker in html:
        html=html.replace(marker,block+marker,1)
    else:
        closings=list(re.finditer(r'<section\b[^>]*class="[^"]*closing[^\"]*"',html,re.I))
        if closings:
            pos=closings[-1].start(); html=html[:pos]+block+html[pos:]
        elif '</main>' in html: html=html.replace('</main>',block+'</main>',1)
        else: raise SystemExit(f'Phase 110 no insertion point: {path}')
    target.write_text(html,encoding='utf-8')

for path,items in TARGET_BACKLINKS.items():
    target=page(path)
    if not target.exists(): raise SystemExit(f'Phase 110 target missing: {path}')
    html=target.read_text(encoding='utf-8')
    if 'ivm-phase110-return' in html: raise SystemExit(f'Phase 110 duplicate target module: {path}')
    block=target_section(items)
    closings=list(re.finditer(r'<section\b[^>]*class="[^"]*closing[^\"]*"',html,re.I))
    if closings:
        pos=closings[-1].start(); html=html[:pos]+block+html[pos:]
    elif '</main>' in html: html=html.replace('</main>',block+'</main>',1)
    else: raise SystemExit(f'Phase 110 no target insertion point: {path}')
    target.write_text(html,encoding='utf-8')

css='''
.ivm-phase110-flow,.ivm-phase110-return{padding:72px 5vw;background:#f3eee5;color:#17140f;border-top:1px solid rgba(30,25,18,.12)}
.ivm-phase110-flow .section-head{max-width:760px;margin-bottom:28px}.ivm-phase110-flow .section-head h2,.ivm-phase110-return h2{font-family:var(--ivm-display);font-weight:300;font-size:clamp(34px,4vw,54px);line-height:1;margin:8px 0 12px}.ivm-phase110-flow .section-head p,.ivm-phase110-return p{max-width:720px;color:#6f6559;line-height:1.7}
.ivm-phase110-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.ivm-phase110-card{display:flex;min-height:150px;padding:22px;flex-direction:column;border:1px solid rgba(40,32,22,.16);background:#ede5d9}.ivm-phase110-card span{font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#8b6b48}.ivm-phase110-card strong{font-family:var(--ivm-display);font-size:25px;font-weight:400;line-height:1.05;margin:12px 0 auto}.ivm-phase110-card b{font-size:11px;font-weight:500;margin-top:18px}.ivm-phase110-links{display:flex;gap:18px;flex-wrap:wrap;margin-top:20px}.ivm-phase110-links .text-link{font-size:13px}
@media(max-width:800px){.ivm-phase110-flow,.ivm-phase110-return{padding:54px 20px}.ivm-phase110-grid{grid-template-columns:1fr}}
'''.strip()
asset=ROOT/'assets'/'phase110.css'; asset.write_text(css,encoding='utf-8')
style='<link rel="stylesheet" href="/assets/phase110.css?v=110">'
for path in set(SOURCE_LINKS)|set(TARGET_BACKLINKS):
    target=page(path); html=target.read_text(encoding='utf-8')
    if style not in html: html=html.replace('</head>',style+'</head>',1)
    target.write_text(html,encoding='utf-8')

print(f'PASS: Phase 110 authority flow — {len(SOURCE_LINKS)} commercial pages route contextually into 5 case studies + 4 Ibiza area pages, with reciprocal topical service pathways and no new URLs')
