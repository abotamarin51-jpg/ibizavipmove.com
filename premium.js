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
      `Service: ${g('fService')||'Full Concierge'}`,
      '',
      'Brief:',
      g('fBrief')||'I would like to discuss the details privately.',
      '',
      'Please let me know availability and the next steps. Thank you.'
    ];
    window.location.href=WHATSAPP+'?text='+encodeURIComponent(lines.join('\n'));
  });
}
