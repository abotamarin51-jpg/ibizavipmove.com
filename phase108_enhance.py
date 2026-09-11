from pathlib import Path
from html import escape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'

PAGES={
'private-concierge-ibiza':{
    'key':'whole-stay-concierge',
    'heading':'Choose Private Concierge when the whole stay must stay connected.',
    'fit':'Best for private clients combining several services under one Ibiza brief: transport, villas, yachts, dining, aviation, security, staffing and changing timings.',
    'difference':'This is the broad coordination layer. For ongoing day-by-day lifestyle management across an extended stay, use Luxury Lifestyle Management.',
    'link':'/luxury-lifestyle-management-ibiza/','link_label':'Compare Luxury Lifestyle Management →',
    'audience':'Private clients with multi-service Ibiza stays',
},
'luxury-lifestyle-management-ibiza':{
    'key':'ongoing-lifestyle-management',
    'heading':'Choose Lifestyle Management when the stay evolves day by day.',
    'fit':'Best for longer or higher-touch stays where the schedule keeps moving and several lifestyle requirements need continuous coordination rather than isolated bookings.',
    'difference':'This is ongoing stay management. For a lighter one-to-one brief focused on personal assistance and reservations, use Personal Concierge.',
    'link':'/personal-concierge-ibiza/','link_label':'Compare Personal Concierge →',
    'audience':'Private clients requiring ongoing full-stay lifestyle management',
},
'personal-concierge-ibiza':{
    'key':'direct-personal-assistance',
    'heading':'Choose Personal Concierge when one dedicated contact is supporting you directly.',
    'fit':'Best for individuals, couples and families who want direct help with reservations, transport, experiences and practical requests without building a complex professional operating structure.',
    'difference':'This is direct personal assistance. For a multi-service itinerary with many operational dependencies, use Private Concierge.',
    'link':'/private-concierge-ibiza/','link_label':'Compare Private Concierge →',
    'audience':'Individuals, couples and families seeking direct personal concierge assistance',
},
'luxury-travel-concierge-ibiza':{
    'key':'traveller-prearrival-planning',
    'heading':'Choose Luxury Travel Concierge when planning starts before arrival.',
    'fit':'Best for international travellers who want pre-arrival trip planning connected to on-island delivery, including flights, ground transport, accommodation, sea days, dining and private support.',
    'difference':'This is traveller-led planning. If you are a travel advisor, concierge company or professional partner outsourcing Ibiza execution for your client, use Destination Management.',
    'link':'/destination-management-ibiza/','link_label':'For travel professionals: Destination Management →',
    'audience':'International luxury travellers planning an Ibiza trip',
},
'vip-services-ibiza':{
    'key':'vip-access-hospitality',
    'heading':'Choose VIP Services when access, hospitality and mobility are the priority.',
    'fit':'Best for guest movements around restaurants, beach clubs, nightlife, yachts, private hospitality and selected protection requirements where timing and access requests must work together.',
    'difference':'This is hospitality and access-led support. For broader multi-service stay coordination beyond venues and guest movements, use Private Concierge.',
    'link':'/private-concierge-ibiza/','link_label':'Compare Private Concierge →',
    'audience':'VIP guests and private groups focused on hospitality, access and mobility',
},
'private-client-services-ibiza':{
    'key':'principal-pa-family-office',
    'heading':'Choose Private Client Services when the brief sits behind a principal.',
    'fit':'Best for principals, families, PAs, EAs and family offices where discretion, authorization, communication structure and operational handovers matter as much as the individual bookings.',
    'difference':'This is principal-led support. For a travel-trade brief where an advisor or concierge company owns the client relationship, use Destination Management.',
    'link':'/destination-management-ibiza/','link_label':'Compare Destination Management →',
    'audience':'Principals, personal assistants, executive assistants and family offices',
},
'destination-management-ibiza':{
    'key':'b2b-local-execution',
    'heading':'Choose Destination Management when you own the client relationship and need Ibiza execution.',
    'fit':'Best for luxury travel advisors, concierge companies, private offices and hospitality partners requiring one local Ibiza operator to execute a professional client brief.',
    'difference':'This is B2B local execution. If you are the traveller planning your own private trip, use Luxury Travel Concierge.',
    'link':'/luxury-travel-concierge-ibiza/','link_label':'For private travellers: Luxury Travel Concierge →',
    'audience':'Luxury travel advisors, concierge companies and professional hospitality partners',
},
'bespoke-concierge-ibiza':{
    'key':'one-off-bespoke-request',
    'heading':'Choose Bespoke Concierge for an unusual or highly specific request.',
    'fit':'Best for one-off sourcing, personal shopping, special arrangements and requests that do not fit neatly into a standard service category.',
    'difference':'This is request-led support. If several services need to stay connected across an itinerary, use Private Concierge instead.',
    'link':'/private-concierge-ibiza/','link_label':'For multi-service stays: Private Concierge →',
    'audience':'Private clients with unusual, one-off or highly specific Ibiza requests',
},
}

SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)


def section(d):
    return f'''<section class="editorial ivm-phase108-intent" data-intent-key="{escape(d['key'],quote=True)}"><div><div class="kicker dark">Choose the right service model</div><h2>{escape(d['heading'])}</h2></div><div><p class="large">{escape(d['fit'])}</p><p><strong>Different from:</strong> {escape(d['difference'])}</p><a class="text-link" href="{escape(d['link'],quote=True)}">{escape(d['link_label'])}</a></div></section>'''


def enhance_schema(html,url,d):
    changed=0
    def repl(m):
        nonlocal changed
        try:data=json.loads(m.group(1))
        except Exception:return m.group(0)
        nodes=data.get('@graph') if isinstance(data,dict) and isinstance(data.get('@graph'),list) else [data]
        for node in nodes:
            if not isinstance(node,dict) or node.get('@type')!='Service':
                continue
            node_url=node.get('url')
            node_id=node.get('@id','')
            if node_url==url or str(node_id).startswith(url) or (not node_url and changed==0):
                node['disambiguatingDescription']=d['fit']+' '+d['difference']
                node['audience']={'@type':'Audience','audienceType':d['audience']}
                changed+=1
                break
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script>'
    html=SCRIPT_RE.sub(repl,html)
    if changed!=1:
        raise SystemExit(f'Phase 108 expected one Service schema for {url}, changed={changed}')
    return html


for slug,d in PAGES.items():
    target=ROOT/slug/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 108 page missing: /{slug}/')
    html=target.read_text(encoding='utf-8')
    if 'ivm-phase108-intent' in html:
        raise SystemExit(f'Phase 108 duplicate intent section before enhancement: /{slug}/')
    block=section(d)
    inserted=False
    for marker in ('<section class="closing-simple">','<section class="closing-cta"'):
        if marker in html:
            html=html.replace(marker,block+marker,1)
            inserted=True
            break
    if not inserted:
        if '</main>' not in html: raise SystemExit(f'Phase 108 main closing tag missing: /{slug}/')
        html=html.replace('</main>',block+'</main>',1)
    url=f'{BASE}/{slug}/'
    html=enhance_schema(html,url,d)
    target.write_text(html,encoding='utf-8')

print('PASS: Phase 108 search-intent separation — eight overlapping concierge pathways now explain distinct buyer fit, adjacent alternatives and schema disambiguation without adding URLs')
