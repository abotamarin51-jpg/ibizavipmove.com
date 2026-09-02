from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
TEL = '+34600703303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
ORG_ID = BASE + '/#organization'


def set_meta(text, title, desc, path, image='/assets/images/hero-desktop.jpg'):
    text = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', text, count=1, flags=re.I|re.S)
    text = re.sub(r'<meta\s+name="description"\s+content="[^"]*">', f'<meta name="description" content="{desc}">', text, count=1, flags=re.I)
    text = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*">', f'<link rel="canonical" href="{BASE}{path}">', text, count=1, flags=re.I)
    replacements = {
        'og:title': title,
        'og:description': desc,
        'og:url': BASE + path,
        'og:image': BASE + image,
    }
    for prop,val in replacements.items():
        pattern = rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")'
        if re.search(pattern,text,flags=re.I):
            text = re.sub(pattern,lambda m,v=val:m.group(1)+v+m.group(2),text,count=1,flags=re.I)
        else:
            text = text.replace('</head>',f'<meta property="{prop}" content="{val}"></head>',1)
    return text


def replace_main(path, html):
    p = ROOT / path.strip('/') / 'index.html'
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'<main>.*?</main>', f'<main>{html}</main>', text, count=1, flags=re.I|re.S)
    p.write_text(text, encoding='utf-8')
    return p


def add_page_schema(text, page_type, name, url, desc):
    # Remove only prior page schemas that describe this same canonical; the shared Organization graph is preserved.
    scripts=[]
    for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.I|re.S):
        try: data=json.loads(m.group(1))
        except Exception: continue
        if isinstance(data,dict) and data.get('@type') in ('WebPage','AboutPage') and data.get('url')==url:
            scripts.append(m.group(0))
    for s in scripts:
        text=text.replace(s,'')
    schema={
        '@context':'https://schema.org','@type':page_type,'name':name,'url':url,
        'description':desc,'about':{'@id':ORG_ID},'isPartOf':{'@id':BASE+'/#website'},'inLanguage':'en'
    }
    return text.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script></head>',1)


ABOUT_TITLE='About Ibiza VIP Move | Private Concierge Ibiza'
ABOUT_DESC='About Ibiza VIP Move: private concierge and lifestyle coordination in Ibiza for private clients, personal assistants, family offices and luxury travel partners.'
about_main=f'''<section class="page-hero editorial-inner-hero" style="--hero:url('/assets/images/hero-desktop.jpg')"><div><div class="kicker light">About Ibiza VIP Move</div><h1>Local knowledge.<br><em>Private standards.</em></h1><p>Ibiza-based concierge and lifestyle coordination built around discretion, responsiveness and one clear point of contact.</p></div></section>
<section class="editorial"><div><div class="kicker dark">Our role</div><h2>Less friction.<br>More alignment.</h2></div><div><p class="large">Ibiza VIP Move coordinates the people, places and logistics behind a private stay in Ibiza.</p><p>Our work can begin with one request or extend across an entire itinerary: chauffeur movements, villas, yachts, private aviation, dining, nightlife, security, private staffing, wellness, events and bespoke requirements. The objective is not to overwhelm clients with options. It is to understand the brief, clarify what matters and keep the relevant moving parts aligned.</p><a class="text-link" href="/private-office/">Explore Private Office →</a></div></section>
<section class="dark-panel"><div class="kicker light">How we operate</div><h2>Quietly capable.<br>Precisely connected.</h2><div class="trust-grid"><div><b>Discretion</b><p>Private requests and client information are handled with care and only shared where operationally necessary.</p></div><div><b>Responsiveness</b><p>Ibiza changes quickly. Communication stays available when timings, guests or priorities move.</p></div><div><b>Local coordination</b><p>Services are aligned on the island around the confirmed brief rather than managed as isolated bookings.</p></div><div><b>Quality over volume</b><p>The focus is the right solution for the request, not the longest supplier list.</p></div></div></section>
<section class="editorial"><div><div class="kicker dark">Official company facts</div><h2>A clear identity,<br>wherever you find us.</h2></div><div><ul class="premium-list"><li><strong>Official name:</strong> Ibiza VIP Move</li><li><strong>Official website:</strong> ibizavipmove.com</li><li><strong>Primary service area:</strong> Ibiza, Balearic Islands, Spain</li><li><strong>Client support:</strong> Private clients, principals, families, personal assistants and family offices</li><li><strong>Professional partners:</strong> Luxury travel advisors, concierge companies and hospitality partners</li><li><strong>Languages supported online:</strong> English, Spanish, French, German and Arabic</li><li><strong>Phone / WhatsApp:</strong> {PHONE}</li><li><strong>Partnership enquiries:</strong> {EMAIL}</li></ul><p>For journalists, directories, partners and platforms requiring factual brand information, use our official Media & Partner Information page.</p><a class="text-link" href="/media-partners/">Official media & partner facts →</a></div></section>
<section class="closing-simple"><h2>Experience Ibiza with less friction.</h2><p>Share the essentials and continue privately with one Ibiza-based point of coordination.</p><div class="hero-actions" style="justify-content:center"><a class="btn dark" href="/contact/">Request Concierge</a><a class="btn dark" href="{WA}">WhatsApp 24/7</a></div></section>'''

PARTNERS_TITLE='Ibiza Concierge Partner for Travel Advisors & Family Offices | Ibiza VIP Move'
PARTNERS_DESC='Ibiza-based concierge partner for personal assistants, family offices, luxury travel advisors, concierge companies and hospitality teams requiring discreet local execution.'
partners_main=f'''<section class="page-hero editorial-inner-hero" style="--hero:url('/assets/images/private-office.jpg')"><div><div class="kicker light">Travel Trade · Private Offices</div><h1>Your Ibiza operator,<br><em>on the ground.</em></h1><p>Private local execution for personal assistants, family offices, luxury travel advisors, concierge companies and hospitality partners.</p></div></section>
<section class="editorial"><div><div class="kicker dark">One local contact</div><h2>Complex briefs.<br>Clear communication.</h2></div><div><p class="large">International partners should not have to coordinate every Ibiza supplier separately.</p><p>Ibiza VIP Move can support client-facing or discreet behind-the-scenes execution across mobility, villas, yachts, aviation, dining, nightlife, security, staffing and bespoke requirements. The partner retains the client relationship and communication structure appropriate to the brief.</p><ul class="premium-list"><li>Direct or discreet behind-the-scenes support</li><li>One Ibiza contact across multiple services</li><li>Principal, guest and itinerary details handled carefully</li><li>Responsive communication when schedules change</li><li>Clear escalation when a request requires further clarification</li></ul></div></section>
<section class="process"><div class="section-head"><div class="kicker dark">Partner workflow</div><h2>A clean handover.</h2><p>Simple communication before arrival, during the stay and when plans move.</p></div><div class="process-grid"><article><span>01</span><h3>Brief</h3><p>Share dates, guest profile, priorities, confirmed elements and the preferred communication structure.</p></article><article><span>02</span><h3>Clarify</h3><p>We identify the operational details needed before services or options are coordinated.</p></article><article><span>03</span><h3>Execute</h3><p>Relevant services are aligned around the itinerary and the partner’s instructions.</p></article><article><span>04</span><h3>Stay connected</h3><p>Communication remains available as timings, guests or requests evolve.</p></article></div></section>
<section class="dark-panel"><div class="kicker light">Built for professional briefs</div><h2>Support behind the client.</h2><div class="trust-grid"><div><b>Personal Assistants</b><p>Direct Ibiza coordination around the principal, guests and changing priorities.</p></div><div><b>Family Offices</b><p>Discreet local execution across connected hospitality and lifestyle requirements.</p></div><div><b>Travel Advisors</b><p>On-the-ground support for high-value client itineraries requiring local follow-through.</p></div><div><b>Concierge & Hospitality</b><p>A dependable Ibiza execution layer when your client needs more than one service.</p></div></div></section>
<section class="editorial"><div><div class="kicker dark">Partnership contact</div><h2>Send the brief<br>to the right desk.</h2></div><div><p class="large">For partnership introductions, recurring client requirements or professional collaboration, use the dedicated partnership email.</p><ul class="premium-list"><li><strong>Email:</strong> {EMAIL}</li><li><strong>WhatsApp:</strong> {PHONE}</li><li><strong>Service area:</strong> Ibiza, Spain</li><li><strong>International client support:</strong> English, Spanish, French, German and Arabic online</li></ul><div class="hero-actions"><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a><a class="btn dark" href="{WA}">WhatsApp</a></div></div></section>'''

MEDIA_TITLE='Official Brand, Media & Partner Information | Ibiza VIP Move'
MEDIA_DESC='Official Ibiza VIP Move brand facts, service descriptions, logo assets and contact information for media, directories and luxury travel partners.'
service_rows=''.join(f'<li><a href="{url}">{label}</a></li>' for label,url in [
('Private Concierge','/private-concierge-ibiza/'),('Private Chauffeur','/private-chauffeur-ibiza/'),('Luxury Villas','/luxury-villas-ibiza/'),('Yachts & Charters','/yacht-charter-ibiza/'),('Private Aviation','/private-aviation-ibiza/'),('Dining & Nightlife','/restaurants-nightlife-ibiza/'),('Security & Close Protection','/private-security-ibiza/'),('Private Chefs & Villa Staffing','/private-chef-staffing-ibiza/'),('Luxury & Supercar Rental','/luxury-car-rental-ibiza/'),('Wellness & Beauty','/wellness-ibiza/'),('Private Events','/private-events-ibiza/'),('Bespoke Requests','/bespoke-concierge-ibiza/')])
media_main=f'''<section class="page-hero editorial-inner-hero" style="--hero:url('/assets/images/aviation.jpg')"><div><div class="kicker light">Official Brand Resource</div><h1>Media, trade &<br><em>official facts.</em></h1><p>A single source of factual Ibiza VIP Move information for journalists, directories, travel professionals, concierge companies and commercial partners.</p></div></section>
<section class="editorial"><div><div class="kicker dark">Official identity</div><h2>One source<br>of truth.</h2></div><div><p class="large"><strong>Ibiza VIP Move</strong> is a private concierge and luxury lifestyle coordination service based around client requirements in Ibiza, Spain.</p><ul class="premium-list"><li><strong>Official business name:</strong> Ibiza VIP Move</li><li><strong>Official website:</strong> https://ibizavipmove.com/</li><li><strong>Positioning:</strong> Private Concierge & Luxury Lifestyle Management in Ibiza</li><li><strong>Primary service area:</strong> Ibiza, Balearic Islands, Spain</li><li><strong>Phone / WhatsApp:</strong> {PHONE}</li><li><strong>Partnership / media email:</strong> {EMAIL}</li><li><strong>Online languages:</strong> English, Spanish, French, German and Arabic</li></ul></div></section>
<section class="dark-panel"><div class="kicker light">Approved descriptions</div><h2>Easy to quote.<br>Easy to verify.</h2><div class="authority-copy-grid"><article><span>Short description</span><p>Ibiza VIP Move is a private concierge and luxury lifestyle management service coordinating high-level stays in Ibiza through one dedicated local point of contact.</p></article><article><span>Extended description</span><p>Ibiza VIP Move coordinates private chauffeur transportation, luxury villas, yachts, private aviation, dining and nightlife, security, private staffing, wellness, events and bespoke requests for private clients and professional travel partners in Ibiza.</p></article></div></section>
<section class="editorial"><div><div class="kicker dark">Official assets</div><h2>Brand files<br>and references.</h2></div><div><ul class="premium-list"><li><a href="/assets/brand-logo.svg"><strong>Primary logo · SVG</strong></a></li><li><a href="/assets/brand-logo.jpg"><strong>Primary logo · JPG</strong></a></li><li><a href="/assets/brand-mark.svg"><strong>Brand mark · SVG</strong></a></li></ul><p>These files are provided for factual/editorial reference to Ibiza VIP Move. Do not alter the name, imply endorsement, or attribute services that are not confirmed by the company.</p></div></section>
<section class="editorial"><div><div class="kicker dark">Official service pages</div><h2>Link to the<br>specific service.</h2></div><div><ul class="premium-list authority-services">{service_rows}</ul><p>For general brand references, link to the homepage. For editorial or partner references to a specific service, use the relevant official service URL above.</p></div></section>
<section class="dark-panel"><div class="kicker light">What not to infer</div><h2>Factual by design.</h2><div class="trust-grid"><div><b>No invented address</b><p>Use only an address confirmed directly by the company for the specific platform or legal purpose.</p></div><div><b>No guaranteed access</b><p>Reservations, inventory, entry and supplier availability remain subject to confirmation.</p></div><div><b>No implied endorsements</b><p>Do not imply celebrity, hotel, venue or partner endorsement without explicit authorization.</p></div><div><b>No unofficial profiles</b><p>Use the official website and contact details above when verifying the brand.</p></div></div></section>
<section class="closing-simple"><h2>Media or partnership enquiry?</h2><p>For factual brand verification, editorial requests or commercial introductions, contact the partnerships desk.</p><div class="hero-actions" style="justify-content:center"><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a><a class="btn dark" href="{WA}">WhatsApp</a></div></section>'''

pages=[
    ('about',ABOUT_TITLE,ABOUT_DESC,'/about/',about_main,'AboutPage','/assets/images/hero-desktop.jpg'),
    ('partners',PARTNERS_TITLE,PARTNERS_DESC,'/partners/',partners_main,'WebPage','/assets/images/private-office.jpg'),
    ('media-partners',MEDIA_TITLE,MEDIA_DESC,'/media-partners/',media_main,'WebPage','/assets/images/aviation.jpg'),
]
for folder,title,desc,url,main,ptype,img in pages:
    p=ROOT/folder/'index.html'
    text=p.read_text(encoding='utf-8')
    text=set_meta(text,title,desc,url,img)
    text=re.sub(r'<main>.*?</main>',f'<main>{main}</main>',text,count=1,flags=re.I|re.S)
    text=add_page_schema(text,ptype,title,BASE+url,desc)
    p.write_text(text,encoding='utf-8')

# Link the authority resource from the three key institutional pages where useful.
for rel in ['about/index.html','partners/index.html','international-clients/index.html']:
    p=ROOT/rel
    if not p.exists(): continue
    txt=p.read_text(encoding='utf-8')
    if '/media-partners/' not in txt:
        txt=txt.replace('</main>','<section class="authority-reference"><a href="/media-partners/">Official Brand & Media Information →</a></section></main>',1)
    p.write_text(txt,encoding='utf-8')

# Lightweight styles for fact-sheet components, appended to the existing editorial inner CSS asset.
css=ROOT/'assets'/'editorial-inner.css'
ct=css.read_text(encoding='utf-8')
extra='''\n/* Phase 25 — authority / press-trade facts */\n.authority-copy-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(255,255,255,.14);margin-top:52px}.authority-copy-grid article{background:#11110f;padding:36px 34px;min-height:250px}.authority-copy-grid span{display:block;font-size:8px;text-transform:uppercase;letter-spacing:.24em;color:#c3a47d;margin-bottom:20px}.authority-copy-grid p{font-family:"Cormorant Garamond",Georgia,serif;font-size:27px;line-height:1.25;color:rgba(255,255,255,.78);margin:0}.authority-services a{text-decoration:none}.authority-reference{background:#0b0b0a;text-align:center;padding:18px 20px}.authority-reference a{color:#d8c4a7;text-transform:uppercase;letter-spacing:.18em;font-size:8px}@media(max-width:700px){.authority-copy-grid{grid-template-columns:1fr}.authority-copy-grid article{min-height:0;padding:28px 24px}}\n'''
if 'Phase 25 — authority / press-trade facts' not in ct:
    css.write_text(ct+extra,encoding='utf-8')

# Operational copy pack: intentionally kept out of public HTML.
ops=ROOT.parent/'PHASE25_EXTERNAL_PROFILE_COPY.md'
ops.write_text(f'''# Ibiza VIP Move — External Profile Copy Pack\n\n## Canonical identity\nOfficial name: Ibiza VIP Move\nWebsite: https://ibizavipmove.com/\nPhone / WhatsApp: {PHONE}\nPartnership email: {EMAIL}\nPrimary service area: Ibiza, Balearic Islands, Spain\n\n## Google Business Profile — proposed description\nIbiza VIP Move provides private concierge and luxury lifestyle coordination in Ibiza for private clients, personal assistants, family offices and luxury travel partners. Services include private chauffeur transportation, luxury villas, yachts, private aviation coordination, restaurants and nightlife, security, private staffing, wellness, events and bespoke requests. One dedicated local point of contact coordinates the relevant moving parts around each confirmed brief.\n\nUse only categories available in the actual Google Business Profile interface and choose the category that best describes what the company is. Do not add an unverified public address.\n\n## TripAdvisor — proposed updated About copy\nIbiza VIP Move is a private concierge and lifestyle management service in Ibiza, coordinating chauffeur transportation, luxury villas, yachts, private aviation, dining and nightlife, security, private staffing, wellness, events and bespoke requests through one dedicated local point of contact.\n\nUpdate the existing profile rather than creating a duplicate. Confirm current phone, website and operating hours directly before publishing them on the platform.\n\n## Neutral public response framework for the old negative review\nThank you for sharing your feedback. We take concerns regarding service and professional relationships seriously. Because the points raised involve matters we cannot appropriately discuss in a public review, we will not share personal or private details here. We remain available through our official contact channels to address any legitimate outstanding matter directly.\n\n## Authority outreach order\n1. Ibiza Luxury Destination / Fomento del Turismo — evaluate legitimate membership eligibility.\n2. Ibiza Travel official tourism directory — request correct inclusion if eligible.\n3. Ibiza Spotlight — evaluate a durable service profile or relevant editorial opportunity.\n4. Real hotels, villa managers, yacht/aviation partners, luxury travel advisors and concierge companies — pursue factual partner mentions where a genuine commercial relationship exists.\n\nAvoid mass directories, paid backlink bundles, fake press, fake reviews and unverified social-profile links.\n''',encoding='utf-8')

# Validate the three authority pages.
for folder,_,_,url,_,_,_ in pages:
    txt=(ROOT/folder/'index.html').read_text(encoding='utf-8')
    assert txt.count('<h1')==1, folder+': exactly one H1 required'
    assert f'<link rel="canonical" href="{BASE}{url}">' in txt, folder+': canonical missing'
    assert PHONE in txt, folder+': current phone missing'
    assert ORG_ID in txt, folder+': Organization reference missing'
assert 'Short description' in (ROOT/'media-partners'/'index.html').read_text(encoding='utf-8')
assert 'Official company facts' in (ROOT/'about'/'index.html').read_text(encoding='utf-8')
assert 'Partnership contact' in (ROOT/'partners'/'index.html').read_text(encoding='utf-8')
print('PASS: Phase 25 brand authority pages + official media facts + external profile copy pack')
