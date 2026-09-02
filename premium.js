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

// First-party conversion readiness. These events stay local unless a future
// GA4/GTM setup explicitly consumes window.dataLayer. No analytics endpoint is
// loaded here, so this does not introduce third-party tracking by itself.
window.dataLayer=window.dataLayer||[];
function ivmTrack(type,detail={}){
  const payload={
    event:'ivm_conversion',
    conversion_type:type,
    page_path:window.location.pathname,
    page_language:document.documentElement.lang||'en',
    ...detail
  };
  window.dataLayer.push(payload);
  window.dispatchEvent(new CustomEvent('ivm:conversion',{detail:payload}));
}

document.addEventListener('click',e=>{
  const a=e.target.closest('a');
  if(!a)return;
  const href=(a.getAttribute('href')||'').trim();
  if(href.startsWith('https://wa.me/')){
    ivmTrack('whatsapp_click',{link_text:(a.textContent||'').trim().slice(0,80)});
  }else if(href.startsWith('tel:')){
    ivmTrack('phone_click',{link_text:(a.textContent||'').trim().slice(0,80)});
  }else if(href.startsWith('mailto:')){
    ivmTrack('email_click',{link_text:(a.textContent||'').trim().slice(0,80)});
  }
});

const WHATSAPP='https://wa.me/34600703303';
const f=document.getElementById('conciergeForm');
if(f){
  const arrival=document.getElementById('fArrival');
  const departure=document.getElementById('fDeparture');
  const today=new Date();
  const localToday=new Date(today.getTime()-today.getTimezoneOffset()*60000).toISOString().slice(0,10);

  if(arrival){
    arrival.min=localToday;
  }
  if(departure){
    departure.min=localToday;
  }
  if(arrival&&departure){
    const syncDepartureMin=()=>{
      departure.min=arrival.value||localToday;
      if(departure.value&&arrival.value&&departure.value<arrival.value){
        departure.value='';
      }
    };
    arrival.addEventListener('change',syncDepartureMin);
    syncDepartureMin();
  }

  f.addEventListener('submit',e=>{
    e.preventDefault();
    if(!f.reportValidity())return;
    const g=id=>document.getElementById(id)?.value||'';
    const service=g('fService')||'Full Concierge';
    ivmTrack('private_brief_submit',{service});
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
