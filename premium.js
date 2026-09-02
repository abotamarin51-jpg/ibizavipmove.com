const menuBtn=document.querySelector('.menu-btn');
const mobileMenu=document.querySelector('.mobile-menu');

function setMenu(open){
  if(!menuBtn||!mobileMenu)return;
  mobileMenu.classList.toggle('open',open);
  document.body.classList.toggle('menu-open',open);
  menuBtn.textContent=open?'Close':'Menu';
  menuBtn.setAttribute('aria-expanded',open?'true':'false');
}

if(menuBtn&&mobileMenu){
  menuBtn.setAttribute('aria-expanded','false');
  menuBtn.addEventListener('click',()=>setMenu(!mobileMenu.classList.contains('open')));
  mobileMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false);});
}

// First-party conversion readiness. Nothing below sends data to an analytics
// provider by itself. Events stay in dataLayer / local CustomEvents until a
// future verified GA4/GTM property explicitly consumes them.
window.dataLayer=window.dataLayer||[];
const IVM_ATTR_KEY='ivm_attribution_v1';
const IVM_UTM_KEYS=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];

function ivmReadAttribution(){
  let saved={};
  try{saved=JSON.parse(sessionStorage.getItem(IVM_ATTR_KEY)||'{}')||{};}catch(_){saved={};}
  const params=new URLSearchParams(window.location.search);
  const incoming={};
  IVM_UTM_KEYS.forEach(k=>{if(params.get(k))incoming[k]=params.get(k).slice(0,160);});
  if(params.get('gclid'))incoming.gclid='present';
  if(params.get('gbraid'))incoming.gbraid='present';
  if(params.get('wbraid'))incoming.wbraid='present';
  if(!saved.landing_page)saved.landing_page=window.location.pathname;
  if(!saved.referrer_host&&document.referrer){
    try{
      const ref=new URL(document.referrer);
      if(ref.hostname!==window.location.hostname)saved.referrer_host=ref.hostname.slice(0,160);
    }catch(_){}
  }
  saved={...saved,...incoming};
  try{sessionStorage.setItem(IVM_ATTR_KEY,JSON.stringify(saved));}catch(_){}
  return saved;
}

const ivmAttribution=ivmReadAttribution();

function ivmPlacement(a){
  if(!a)return'unknown';
  if(a.closest('.site-header'))return'header';
  if(a.closest('.mobile-bar'))return'mobile_bar';
  if(a.closest('.hero,.page-hero'))return'hero';
  if(a.closest('.ivm-chapter'))return'service_chapter';
  if(a.closest('.ivm-final-request,.closing-cta,.closing-simple'))return'final_cta';
  if(a.closest('footer'))return'footer';
  return'inline';
}

function ivmTrack(type,detail={}){
  const payload={
    event:'ivm_conversion',
    conversion_type:type,
    page_path:window.location.pathname,
    page_title:document.title.slice(0,160),
    page_language:document.documentElement.lang||'en',
    ...ivmAttribution,
    ...detail
  };
  window.dataLayer.push(payload);
  window.dispatchEvent(new CustomEvent('ivm:conversion',{detail:payload}));
}

function ivmContextLabel(){
  const path=window.location.pathname;
  const labels={
    '/':'Private concierge in Ibiza',
    '/private-concierge-ibiza/':'Private Concierge',
    '/private-chauffeur-ibiza/':'Private Chauffeur & Transportation',
    '/luxury-villas-ibiza/':'Luxury Villas & Private Stays',
    '/yacht-charter-ibiza/':'Yachts & Charters',
    '/private-aviation-ibiza/':'Private Aviation',
    '/restaurants-nightlife-ibiza/':'Dining, Beach Clubs & Nightlife',
    '/private-security-ibiza/':'Security & Close Protection',
    '/private-chef-staffing-ibiza/':'Private Chefs & Villa Staffing',
    '/luxury-car-rental-ibiza/':'Luxury & Supercar Rental',
    '/wellness-ibiza/':'Wellness & Beauty',
    '/private-events-ibiza/':'Private Events & Celebrations',
    '/bespoke-concierge-ibiza/':'Lifestyle & Bespoke Requests',
    '/private-office/':'Private Office',
    '/partners/':'B2B Partnership',
    '/international-clients/':'International Client Support'
  };
  if(labels[path])return labels[path];
  const h1=document.querySelector('h1');
  return(h1?.textContent||'Private concierge in Ibiza').replace(/\s+/g,' ').trim().slice(0,120);
}

const WHATSAPP='https://wa.me/34600703303';
function ivmWhatsAppMessage(){
  const lang=(document.documentElement.lang||'en').toLowerCase().split('-')[0];
  const templates={
    en:`Hello Ibiza VIP Move,\n\nI would like to arrange private concierge assistance for an upcoming stay in Ibiza.\n\nPlease let me know the best way to share my dates and requirements.\n\nThank you.`,
    es:`Hola Ibiza VIP Move,\n\nMe gustaría organizar asistencia de concierge privado para una próxima estancia en Ibiza.\n\nPor favor, indíquenme la mejor forma de compartir mis fechas y necesidades.\n\nMuchas gracias.`,
    fr:`Bonjour Ibiza VIP Move,\n\nJe souhaite organiser une assistance de conciergerie privée pour un prochain séjour à Ibiza.\n\nMerci de m’indiquer la meilleure façon de vous communiquer mes dates et mes besoins.\n\nMerci.`,
    de:`Hallo Ibiza VIP Move,\n\nich möchte für einen bevorstehenden Aufenthalt auf Ibiza einen privaten Concierge-Service anfragen.\n\nBitte teilen Sie mir mit, wie ich Ihnen meine Reisedaten und Anforderungen am besten übermitteln kann.\n\nVielen Dank.`,
    ar:`مرحباً Ibiza VIP Move،\n\nأرغب في ترتيب خدمة كونسيرج خاصة لإقامة قادمة في إيبيزا.\n\nيرجى إخباري بأفضل طريقة لمشاركة التواريخ والمتطلبات الخاصة بي.\n\nشكراً.`
  };
  return templates[lang]||templates.en;
}

// Keep generic WhatsApp CTAs polished and neutral. Deliberately prefilled
// form submissions remain untouched and may include details supplied by the client.
document.querySelectorAll('a[href^="https://wa.me/34600703303"]').forEach(a=>{
  try{
    const u=new URL(a.href);
    if(!u.searchParams.get('text'))a.href=WHATSAPP+'?text='+encodeURIComponent(ivmWhatsAppMessage());
  }catch(_){}
});

document.addEventListener('click',e=>{
  const a=e.target.closest('a');
  if(!a)return;
  const href=(a.getAttribute('href')||'').trim();
  const common={link_text:(a.textContent||'').replace(/\s+/g,' ').trim().slice(0,80),cta_placement:ivmPlacement(a)};
  if(href.startsWith('https://wa.me/')){
    ivmTrack('whatsapp_click',{...common,service_context:ivmContextLabel()});
  }else if(href.startsWith('tel:')){
    ivmTrack('phone_click',common);
  }else if(href.startsWith('mailto:')){
    ivmTrack('email_click',common);
  }else if(href==='/contact/'||href==='https://ibizavipmove.com/contact/'){
    ivmTrack('request_concierge_click',common);
  }else if(href==='/partners/'||href==='https://ibizavipmove.com/partners/'){
    ivmTrack('partner_interest_click',common);
  }
});

const f=document.getElementById('conciergeForm');
if(f){
  const arrival=document.getElementById('fArrival');
  const departure=document.getElementById('fDeparture');
  const today=new Date();
  const localToday=new Date(today.getTime()-today.getTimezoneOffset()*60000).toISOString().slice(0,10);

  if(arrival)arrival.min=localToday;
  if(departure)departure.min=localToday;
  if(arrival&&departure){
    const syncDepartureMin=()=>{
      departure.min=arrival.value||localToday;
      if(departure.value&&arrival.value&&departure.value<arrival.value)departure.value='';
    };
    arrival.addEventListener('change',syncDepartureMin);
    syncDepartureMin();
  }

  f.addEventListener('submit',e=>{
    e.preventDefault();
    if(!f.reportValidity())return;
    const g=id=>document.getElementById(id)?.value||'';
    const service=g('fService')||'Full Concierge';
    ivmTrack('private_brief_submit',{service,cta_placement:'contact_form'});
    const lines=[
      'Hello Ibiza VIP Move,',
      '',
      'I would like to request private concierge assistance in Ibiza.',
      '',
      `Name: ${g('fName')}`,
      `Phone: ${g('fPhone')}`,
      `Arrival: ${g('fArrival')||'To be confirmed'}`,
      `Departure: ${g('fDeparture')||'To be confirmed'}`,
      `Guests: ${g('fGuests')||'To be confirmed'}`,
      `Service: ${service}`,
      '',
      'Brief:',
      g('fBrief')||'I would like to discuss the details privately.',
      '',
      'Please let me know availability and the next steps. Thank you.'
    ];
    window.location.href=WHATSAPP+'?text='+encodeURIComponent(lines.join('\n'));
  });
}

// Phase 22 — lightweight premium interaction layer.
const ivmReduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const ivmHeader=document.querySelector('.site-header');
if(ivmHeader){
  const syncHeader=()=>ivmHeader.classList.toggle('is-scrolled',window.scrollY>36);
  syncHeader();
  window.addEventListener('scroll',syncHeader,{passive:true});
}

if(!ivmReduceMotion&&'IntersectionObserver' in window){
  document.documentElement.classList.add('ivm-motion-ready');
  const revealSelector=[
    '.ivm-manifesto-inner',
    '.ivm-chapter-copy',
    '.ivm-private-office-inner',
    '.ivm-black-book-head',
    '.ivm-book-card',
    '.ivm-final-request-inner',
    'body.ivm-editorial-inner .editorial > *',
    'body.ivm-editorial-inner .process-grid > *',
    'body.ivm-black-book-article .article-body > section',
    'body.ivm-black-book-article .article-cta'
  ].join(',');
  const revealEls=[...document.querySelectorAll(revealSelector)];
  revealEls.forEach((el,i)=>{
    el.classList.add('ivm-reveal');
    el.style.setProperty('--ivm-delay',`${Math.min(i%4,3)*55}ms`);
  });
  const io=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  },{threshold:.08,rootMargin:'0px 0px -7% 0px'});
  revealEls.forEach(el=>io.observe(el));
}
