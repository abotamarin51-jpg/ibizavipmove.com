from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
WA = 'https://wa.me/34600703303'
TODAY = '2026-09-03'

ARTICLES = {
    'villa-arrival-planning': {
        'kicker': 'Private Stays',
        'title': 'The Villa Arrival Brief | Ibiza VIP Move',
        'h1': 'The Villa Arrival Brief',
        'desc': 'A private Ibiza villa arrival planning note covering access, luggage, chauffeur timing, guest movements and the first hours of the stay.',
        'intro': 'A villa arrival feels effortless when access, transport, luggage and the first guest requirements are aligned before the car reaches the property.',
        'image': '/assets/images/villa.jpg',
        'sections': [
            ('Start with the handover, not the airport.', [
                'The practical arrival brief should identify who controls access to the property, when access is available and who can resolve an issue if the arrival time changes.',
                'That information should sit beside the guest arrival details rather than in a separate supplier thread. The handover is part of the journey.'
            ]),
            ('Match luggage to the vehicle plan.', [
                'Passenger count alone does not define the transport requirement. Luggage, equipment, child seats and separate guest arrivals can change the number or type of vehicles needed.',
                'Clarifying the load before confirmation reduces unnecessary changes at the airport or villa gate.'
            ]),
            ('Plan the first two hours.', [
                'The first hours often contain several small dependencies: access, luggage placement, groceries or refreshments, staff introductions, room allocation and the next confirmed movement.',
                'A simple sequence keeps the client out of operational conversations and gives the on-island team one clear order of priorities.'
            ]),
            ('Keep the plan flexible.', [
                'Flight times, baggage delivery and guest movements can change. The useful brief is one that makes clear which elements are fixed and which can move if the arrival shifts.',
                'When the dependencies are visible, the affected services can be reviewed without rebuilding the whole stay.'
            ]),
        ],
    },
    'nightlife-transport-planning': {
        'kicker': 'Access & Movement',
        'title': 'Ibiza Nightlife Transport Planning | Ibiza VIP Move',
        'h1': 'The Nightlife Movement Plan',
        'desc': 'Private Ibiza nightlife transport planning for villas, restaurants, clubs, multiple guests, changing pickup times and late-night return logistics.',
        'intro': 'A nightlife booking is only one part of the evening. The movement plan should connect the villa, dinner, venue access, guest changes and the return home.',
        'image': '/assets/images/nightlife.jpg',
        'sections': [
            ('Build the evening as one movement.', [
                'Treating dinner, nightlife and the return as unrelated transfers creates unnecessary gaps. A better brief maps the confirmed sequence and the expected decision points between locations.',
                'This is especially useful when several guests may leave at different times or when a second vehicle could become necessary.'
            ]),
            ('Agree the communication line.', [
                'The principal, assistant and driver should not all need to manage separate operational threads. Decide who can change timing and who should receive movement updates.',
                'A clear communication structure matters more after midnight, when plans tend to move quickly.'
            ]),
            ('Define the pickup logic.', [
                'For each major stop, clarify the planned pickup point and the fallback if access, traffic or venue operations make that point impractical.',
                'The goal is not to over-script the night. It is to remove avoidable confusion when the group is ready to move.'
            ]),
            ('Plan for split departures.', [
                'Groups do not always return together. If that is likely, the brief should make clear whether the vehicle remains with the principal, whether another vehicle can be requested and how the remaining guests will be handled.',
                'Those decisions are easier before the evening begins than at the end of it.'
            ]),
        ],
    },
    'private-aviation-ground-coordination': {
        'kicker': 'Private Aviation',
        'title': 'Private Aviation Ground Coordination Ibiza | Ibiza VIP Move',
        'h1': 'From Aircraft to Ibiza',
        'desc': 'Private aviation ground coordination in Ibiza covering flight timing, luggage, chauffeur vehicles, onward villa movements and changing arrival details.',
        'intro': 'The aviation movement is complete only when the passengers, luggage and ground plan connect cleanly with the rest of the Ibiza itinerary.',
        'image': '/assets/images/aviation.jpg',
        'sections': [
            ('Share the operational essentials early.', [
                'The ground team needs the information that affects the handoff: flight timing, passenger count, luggage profile, onward destination and the contact authorised to communicate schedule changes.',
                'Keeping those details together reduces fragmented updates when the arrival time moves.'
            ]),
            ('Size the ground movement correctly.', [
                'Aviation arrivals can require more ground capacity than the passenger count suggests. Luggage volume, equipment, security requirements and separate guest movements should be considered before vehicles are confirmed.',
                'The objective is a calm handoff rather than solving capacity at the curb.'
            ]),
            ('Connect arrival to villa readiness.', [
                'If the onward destination is a private villa, the ground movement should be considered together with property access and the expected arrival window.',
                'This prevents the transport team and property team from working to different versions of the schedule.'
            ]),
            ('Prepare for a moving ETA.', [
                'Private aviation schedules can evolve. The useful operating brief identifies which downstream services need to be reviewed if the ETA changes and who should receive the update.',
                'That structure keeps the client experience stable even when the timetable is not.'
            ]),
        ],
    },
}


def article_main(data):
    sections = ''.join(
        '<section><h2>' + escape(h) + '</h2>' + ''.join('<p>' + escape(p) + '</p>' for p in ps) + '</section>'
        for h, ps in data['sections']
    )
    return f'''<section class="page-hero intelligence-hero"><div class="page-hero-media"><img src="{data['image']}" alt="{escape(data['h1'])} — Ibiza VIP Move" width="1800" height="1200" fetchpriority="high" decoding="async"></div><div><div class="kicker light">The Ibiza Black Book · {escape(data['kicker'])}</div><h1>{escape(data['h1'])}</h1><p>{escape(data['intro'])}</p></div></section><article class="article-shell"><div class="article-meta"><span>Ibiza VIP Move</span><span>Private planning note</span><span>Ibiza · Spain</span></div><div class="article-body">{sections}<aside class="article-cta"><div class="kicker dark">Private assistance</div><h2>Need this coordinated around a real itinerary?</h2><p>Share the dates, guests and confirmed moving parts. Ibiza VIP Move can continue the brief privately and align the relevant services.</p><a class="btn dark" href="{WA}">Speak to Concierge</a></aside></div></article>'''


def update_jsonld(text, canonical, data):
    pattern = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
    def repl(m):
        try:
            obj = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if not isinstance(obj, dict):
            return m.group(0)
        typ = obj.get('@type')
        if typ in ('WebPage','Article','BlogPosting'):
            obj['name'] = data['h1']
            obj['headline'] = data['h1']
            obj['url'] = canonical
            obj['description'] = data['desc']
            obj['image'] = BASE + data['image']
            obj['dateModified'] = TODAY
            if typ in ('Article','BlogPosting'):
                obj['datePublished'] = TODAY
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
    return pattern.sub(repl, text)


template_path = ROOT / 'ibiza-intelligence' / 'private-arrival' / 'index.html'
if not template_path.exists():
    raise SystemExit('Black Book template page missing')
template = template_path.read_text(encoding='utf-8')

new_paths = []
for slug, data in ARTICLES.items():
    path = f'/ibiza-intelligence/{slug}/'
    canonical = BASE + path
    html = template
    html = re.sub(r'<title>.*?</title>', f'<title>{escape(data["title"])}</title>', html, count=1, flags=re.I | re.S)
    html = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1)+escape(data['desc'])+m.group(2), html, count=1, flags=re.I)
    html = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', lambda m: m.group(1)+canonical+m.group(2), html, count=1, flags=re.I)
    for prop, value in [('og:title', data['title']),('og:description',data['desc']),('og:url',canonical),('og:image',BASE+data['image'])]:
        html = re.sub(rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")', lambda m,v=value: m.group(1)+escape(v)+m.group(2), html, count=1, flags=re.I)
    html = re.sub(r'<main>.*?</main>', '<main>'+article_main(data)+'</main>', html, count=1, flags=re.I | re.S)
    html = update_jsonld(html, canonical, data)
    dest = ROOT / path.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')
    new_paths.append(path)

# Add a second editorial shelf to the Black Book hub without changing its existing opening composition.
hub = ROOT / 'ibiza-intelligence' / 'index.html'
hub_html = hub.read_text(encoding='utf-8')
if 'phase34-black-book-more' not in hub_html:
    cards = ''.join(
        f'<a class="ivm-book-card" href="/ibiza-intelligence/{slug}/"><span>Planning Note</span><h3>{escape(data["h1"])}</h3><p>{escape(data["intro"])}</p><b>Open the Black Book →</b></a>'
        for slug, data in ARTICLES.items()
    )
    shelf = f'''<section class="ivm-black-book phase34-black-book-more"><div class="ivm-black-book-head"><div><div class="kicker dark">More from the Black Book</div><h2>Operational notes.</h2></div><p class="black-book-intro">Practical Ibiza planning for the moments where transport, access, properties and timings need to work as one.</p></div><div class="ivm-black-book-grid">{cards}</div></section>'''
    hub_html = hub_html.replace('</main>', shelf + '</main>', 1)
    hub.write_text(hub_html, encoding='utf-8')

# Main sitemap: add canonical URLs with current release date.
sitemap = ROOT / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree = ET.parse(sitemap)
root = tree.getroot()
ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
existing = {u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for path in new_paths:
    url = BASE + path
    if url not in existing:
        u = ET.SubElement(root, f'{{{ns}}}url')
        ET.SubElement(u, f'{{{ns}}}loc').text = url
        ET.SubElement(u, f'{{{ns}}}lastmod').text = TODAY
        ET.SubElement(u, f'{{{ns}}}changefreq').text = 'monthly'
        ET.SubElement(u, f'{{{ns}}}priority').text = '0.7'
tree.write(sitemap, encoding='utf-8', xml_declaration=True)

# Image sitemap: add the primary editorial image for each new article.
image_sitemap = ROOT / 'image-sitemap.xml'
if image_sitemap.exists():
    IMG_NS='http://www.google.com/schemas/sitemap-image/1.1'
    SM_NS='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', SM_NS); ET.register_namespace('image', IMG_NS)
    itree=ET.parse(image_sitemap); iroot=itree.getroot()
    iexisting={u.find(f'{{{SM_NS}}}loc').text for u in iroot.findall(f'{{{SM_NS}}}url') if u.find(f'{{{SM_NS}}}loc') is not None}
    for slug,data in ARTICLES.items():
        url=BASE+f'/ibiza-intelligence/{slug}/'
        if url not in iexisting:
            ue=ET.SubElement(iroot,f'{{{SM_NS}}}url'); ET.SubElement(ue,f'{{{SM_NS}}}loc').text=url
            ie=ET.SubElement(ue,f'{{{IMG_NS}}}image'); ET.SubElement(ie,f'{{{IMG_NS}}}loc').text=BASE+data['image']
    itree.write(image_sitemap,encoding='utf-8',xml_declaration=True)

# Extend llms discovery resource.
llms = ROOT / 'llms.txt'
if llms.exists():
    text = llms.read_text(encoding='utf-8')
    additions = '\n'.join(f'- [{data["h1"]}]({BASE}/ibiza-intelligence/{slug}/)' for slug,data in ARTICLES.items())
    if '/ibiza-intelligence/villa-arrival-planning/' not in text:
        text += '\n## Additional Ibiza Black Book planning notes\n' + additions + '\n'
        llms.write_text(text, encoding='utf-8')

# Validation.
for slug,data in ARTICLES.items():
    p=ROOT/'ibiza-intelligence'/slug/'index.html'
    html=p.read_text(encoding='utf-8')
    assert html.count('<h1')==1, slug
    assert BASE+f'/ibiza-intelligence/{slug}/' in html, slug
    assert data['desc'] in html, slug
    assert 'article-shell' in html and 'Speak to Concierge' in html, slug
    assert data['image'] in html, slug
assert 'phase34-black-book-more' in hub.read_text(encoding='utf-8')
sitemap_text=sitemap.read_text(encoding='utf-8')
for path in new_paths: assert BASE+path in sitemap_text
print(f'PASS: Phase 34 Black Book expanded with {len(ARTICLES)} high-intent planning notes')
