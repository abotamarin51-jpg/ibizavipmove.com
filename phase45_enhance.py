from pathlib import Path
import json
import re

ROOT = Path('_site')
STYLE = '/assets/phase45.css?v=45'

PAGES = {
    '/private-chauffeur-ibiza/': [
        ('What information is useful when requesting a private chauffeur in Ibiza?', 'Share the dates, passenger count, pickup points, expected schedule and any luggage or multi-vehicle requirements. If the itinerary is still evolving, confirmed anchors are enough to start the brief.'),
        ('Can chauffeur service be coordinated around several stops in one day?', 'Yes. A private chauffeur brief can be built around multiple confirmed movements such as villa, marina, restaurant and nightlife stops, with the schedule kept under one line of communication.'),
        ('What happens if the timing changes?', 'The affected movements are reviewed around the updated timing. The useful approach is to identify which parts of the itinerary are fixed and which can move if plans change.'),
        ('Can several vehicles be coordinated together?', 'When the guest count, luggage or schedule requires it, multiple vehicles can be planned around the same itinerary so that movements and communication remain aligned.')],
    '/luxury-villas-ibiza/': [
        ('What should be included in a private villa brief?', 'Dates, guest count, preferred area, privacy priorities and any known requirements such as staffing, transport, security or access needs help define the brief.'),
        ('Can villa arrangements be coordinated with the rest of the stay?', 'Yes. The value is in connecting the property with arrival timing, chauffeur movements, yacht days, dining and other confirmed services rather than treating the villa as an isolated booking.'),
        ('How should arrival access be planned?', 'Confirm who controls property access, the expected arrival window and who can resolve a change. That information should sit beside the transport plan so both teams work from the same timing.'),
        ('What if the final itinerary is not ready yet?', 'The stay can be structured from the confirmed essentials first. Additional services can be clarified as the itinerary develops without requiring every detail to be fixed at the beginning.')],
    '/yacht-charter-ibiza/': [
        ('What information helps when planning a yacht day from Ibiza?', 'Share the date, guest count, preferred style of day and any known marina, dining or Formentera priorities. Transport to and from the marina should be considered at the same time.'),
        ('Can the yacht day be connected with villa transport and evening plans?', 'Yes. Marina timing, chauffeur movements, lunch and the evening that follows can be aligned as one itinerary so the day does not operate in separate supplier threads.'),
        ('How are timing changes handled?', 'Weather, marina operations and guest preferences can affect the schedule. The connected services are reviewed around the updated timing when a change affects the wider plan.'),
        ('Do we need the full day planned before enquiring?', 'No. A useful first brief can start with the date, guests and priorities. The operational pieces can then be clarified around availability and the rest of the stay.')],
    '/restaurants-nightlife-ibiza/': [
        ('What should we send for restaurant or nightlife planning?', 'Share the date, number of guests, preferred atmosphere, known venues and the broader evening plan. Transport and timing matter because the reservation is only one part of the movement.'),
        ('Can dining, nightlife and transport be coordinated together?', 'Yes. Dinner, venue access, chauffeur timing and the return can be handled as one sequence, which is especially useful when guest movements may change during the evening.'),
        ('What if guests leave at different times?', 'If split departures are likely, that should be identified in the brief so vehicle logic and communication can be planned before the evening rather than improvised later.'),
        ('Can a request start without a confirmed venue?', 'Yes. Share the date, guest profile and preferences. Suitable options can then be discussed around availability and the rest of the itinerary.')],
    '/private-aviation-ibiza/': [
        ('What information is useful for private aviation ground coordination?', 'Flight timing, passenger count, luggage profile, onward destination and the contact authorised to communicate schedule changes are the essential starting points.'),
        ('Can aircraft arrival be coordinated with chauffeur and villa access?', 'Yes. The ground movement is strongest when flight timing, luggage, vehicle capacity and property readiness are treated as one connected handoff.'),
        ('What happens if the ETA changes?', 'The downstream services affected by the new arrival time are reviewed around the updated ETA. A clear communication line helps avoid different teams working to different schedules.'),
        ('How is vehicle capacity decided?', 'Passenger count is only part of the brief. Luggage, equipment, security needs and separate guest movements can change the number or type of vehicles required.')],
    '/private-security-ibiza/': [
        ('What should be included in a private security brief?', 'Share the dates, principal or guest profile, relevant locations, movement schedule and any known privacy or close-protection requirements. Sensitive details can be clarified through the private conversation.'),
        ('Can security be coordinated with chauffeur and venue movements?', 'Yes. Security requirements should be considered alongside transport, property access and venue timing so the operational plan follows the same itinerary.'),
        ('Does every stay require the same security structure?', 'No. The appropriate setup depends on the principal, locations, schedule and specific requirements. The brief should define the need before determining the operational structure.'),
        ('Can requirements change during the stay?', 'When the itinerary changes, the security elements connected to those movements can be reviewed as well. The goal is to keep the operational picture aligned rather than separate.')]
}

css_src=Path('phase45.css')
if not css_src.exists():raise SystemExit('phase45.css missing')
css_dest=ROOT/'assets'/'phase45.css';css_dest.write_text(css_src.read_text(encoding='utf-8'),encoding='utf-8')


def faq_schema(items):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}

for path,items in PAGES.items():
    file=ROOT/path.strip('/')/'index.html'
    if not file.exists():raise SystemExit(f'Core service page missing: {path}')
    html=file.read_text(encoding='utf-8')
    if STYLE not in html:html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
    if 'ivm-service-faq' not in html:
        details=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
        section=f'''<section class="ivm-service-faq" aria-label="Service planning questions"><div class="ivm-service-faq-inner"><div class="ivm-service-faq-head"><div class="eyebrow">Before the private brief</div><h2>What clients usually need to know.</h2><p>Short operational answers to the questions that most often shape the first conversation.</p></div><div class="ivm-faq-list">{details}</div></div></section>'''
        html=html.replace('</main>',section+'</main>',1)
    pattern=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
    kept=[];cursor=0
    for m in pattern.finditer(html):
        kept.append(html[cursor:m.start()])
        try:obj=json.loads(m.group(1))
        except Exception:obj=None
        if not (isinstance(obj,dict) and obj.get('@type')=='FAQPage'):kept.append(m.group(0))
        cursor=m.end()
    kept.append(html[cursor:]);html=''.join(kept)
    schema=json.dumps(faq_schema(items),ensure_ascii=False)
    html=html.replace('</head>',f'<script type="application/ld+json">{schema}</script></head>',1)
    file.write_text(html,encoding='utf-8')

for path,items in PAGES.items():
    html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    faq=re.search(r'<section class="ivm-service-faq".*?</section>',html,re.I|re.S)
    assert faq and faq.group(0).count('<details>')==4,path
    schemas=[]
    for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>',html,re.I|re.S):
        try:obj=json.loads(m.group(1))
        except Exception:continue
        if isinstance(obj,dict) and obj.get('@type')=='FAQPage':schemas.append(obj)
    assert len(schemas)==1 and len(schemas[0].get('mainEntity',[]))==4,path
    assert STYLE in html,path
    assert html.count('<h1')==1,path
assert css_dest.exists() and css_dest.stat().st_size>1000
print(f'PASS: Phase 45 decision FAQs added to {len(PAGES)} core service pages with valid FAQPage schema')
