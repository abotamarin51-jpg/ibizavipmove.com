from pathlib import Path
from html import escape, unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
HOME=ROOT/'index.html'
CONCIERGE=ROOT/'private-concierge-ibiza'/'index.html'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

HOME_TITLE='Luxury Concierge Ibiza | Ibiza VIP Move'
HOME_DESC='Luxury concierge in Ibiza for private clients, PAs and family offices. Chauffeurs, villas, yachts, aviation, dining, security and bespoke support.'
CONCIERGE_TITLE='Private Concierge Ibiza | Ibiza VIP Move'
CONCIERGE_DESC='Private concierge in Ibiza for discreet lifestyle management, chauffeur transport, villas, yachts, dining, aviation, security and multi-service stays.'


def replace_once(html,pattern,repl,label):
    new,n=re.subn(pattern,repl,html,count=1,flags=re.I|re.S)
    if n!=1:raise SystemExit(f'Phase 85 expected one {label}, found {n}')
    return new


def set_meta(html,attr,name,value):
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>',re.I)
    tag=f'<meta {attr}="{name}" content="{escape(value,quote=True)}">'
    if patt.search(html):return patt.sub(tag,html,count=1)
    return html.replace('</head>',tag+'</head>',1)


def patch_jsonld(html,canonical,title,desc):
    def patch(match):
        try:obj=json.loads(match.group(2))
        except Exception:return match.group(0)
        changed=False
        candidates=[]
        if isinstance(obj,dict) and isinstance(obj.get('@graph'),list):
            candidates=[x for x in obj['@graph'] if isinstance(x,dict)]
        elif isinstance(obj,dict):
            candidates=[obj]
        for node in candidates:
            typ=node.get('@type')
            types=typ if isinstance(typ,list) else [typ]
            if 'WebPage' in types and node.get('url')==canonical:
                node['name']=title
                node['description']=desc
                changed=True
            if canonical.endswith('/private-concierge-ibiza/') and 'Service' in types and node.get('url')==canonical:
                node['description']=desc
                changed=True
        if not changed:return match.group(0)
        return match.group(1)+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+match.group(3)
    return SCRIPT_RE.sub(patch,html)

if not HOME.exists() or not CONCIERGE.exists():
    raise SystemExit('Phase 85 target pages missing')

# HOME owns the broad head term “Luxury Concierge Ibiza”.
h=HOME.read_text(encoding='utf-8')
h=replace_once(h,r'<title>.*?</title>',f'<title>{HOME_TITLE}</title>','home title')
h=set_meta(h,'name','description',HOME_DESC)
h=set_meta(h,'property','og:title',HOME_TITLE)
h=set_meta(h,'property','og:description',HOME_DESC)
h=set_meta(h,'name','twitter:title',HOME_TITLE)
h=set_meta(h,'name','twitter:description',HOME_DESC)
h=replace_once(h,r'<div class="kicker light">Private Concierge · Ibiza</div>','<div class="kicker light">Luxury Concierge · Ibiza</div>','home hero kicker')
h=replace_once(h,r'<h1>Exceptional Ibiza,\s*<br>\s*handled privately\.</h1>','<h1>Luxury concierge in Ibiza,<br>handled privately.</h1>','home h1')
needle='<h2>One trusted contact for the island.</h2>'
if needle not in h:raise SystemExit('Phase 85 home trust heading missing')
h=h.replace(needle,needle+'<p class="ivm-seo-lead">Ibiza VIP Move is a luxury concierge in Ibiza for private clients and professional teams who want one discreet on-island point of coordination.</p>',1)
h=patch_jsonld(h,BASE+'/',HOME_TITLE,HOME_DESC)
HOME.write_text(h,encoding='utf-8')

# /private-concierge-ibiza/ owns the narrower “Private Concierge Ibiza” intent.
c=CONCIERGE.read_text(encoding='utf-8')
c=replace_once(c,r'<title>.*?</title>',f'<title>{CONCIERGE_TITLE}</title>','concierge title')
c=set_meta(c,'name','description',CONCIERGE_DESC)
c=set_meta(c,'property','og:title',CONCIERGE_TITLE)
c=set_meta(c,'property','og:description',CONCIERGE_DESC)
c=set_meta(c,'name','twitter:title',CONCIERGE_TITLE)
c=set_meta(c,'name','twitter:description',CONCIERGE_DESC)
c=patch_jsonld(c,BASE+'/private-concierge-ibiza/',CONCIERGE_TITLE,CONCIERGE_DESC)

marker='<section class="faq">'
if marker not in c:raise SystemExit('Phase 85 concierge FAQ marker missing')
extra='''<section class="editorial ivm-search-intent">
<div><div class="kicker dark">Luxury concierge Ibiza</div><h2>One brief. Multiple moving parts.</h2></div>
<div>
<p class="large">A private concierge becomes most valuable when several parts of an Ibiza stay depend on each other. Flights affect airport movements, villa access affects arrivals, marina times affect yacht days, and restaurant or nightlife plans affect transport and security.</p>
<p>Ibiza VIP Move keeps those confirmed elements connected through one local point of contact rather than treating every request as a separate booking. Typical briefs combine <a href="/private-chauffeur-ibiza/">private chauffeur</a>, <a href="/luxury-villas-ibiza/">villa coordination</a>, <a href="/yacht-charter-ibiza/">yacht charter</a>, <a href="/private-aviation-ibiza/">private aviation support</a>, <a href="/restaurants-nightlife-ibiza/">dining and nightlife</a> and <a href="/private-security-ibiza/">private security</a>.</p>
<p>For peak-season dates, earlier planning creates more room to coordinate availability and timings. Last-minute requests can still be assessed, but reservations, access and supplier services are only treated as confirmed once the relevant terms are agreed.</p>
</div>
</section>
<section class="dark-panel ivm-service-area">
<div class="kicker light">Ibiza service area</div>
<h2>Local coordination across the island.</h2>
<div class="trust-grid">
<div><b>Ibiza Town & Marina Botafoch</b><p>Airport arrivals, hotels, marinas, dining, nightlife and city movements coordinated around the same itinerary.</p></div>
<div><b>Sant Josep & the south</b><p>Villa areas, Cala Jondal, Es Cubells and south-coast movements linked with chauffeur, yacht and dining plans.</p></div>
<div><b>Santa Eulària & the east</b><p>Private stays, marina movements, restaurants and family or multi-day itineraries coordinated locally.</p></div>
<div><b>Sant Antoni & the west</b><p>Villa, beach, sunset and nightlife movements aligned with pre-booked transport and the wider guest schedule.</p></div>
</div>
<p>We operate as a private on-island service. Meetings and services are coordinated at villas, hotels, marinas, Ibiza Airport and other agreed locations rather than through a public walk-in concierge desk.</p>
</section>'''
c=c.replace(marker,extra+marker,1)
CONCIERGE.write_text(c,encoding='utf-8')

print('PASS: Phase 85 search intent — HOME aligned to Luxury Concierge Ibiza; Private Concierge landing deepened with local Ibiza service-area relevance')
