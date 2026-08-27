const menuBtn=document.querySelector('.menu-btn');
const mobileMenu=document.querySelector('.mobile-menu');
if(menuBtn&&mobileMenu){
  menuBtn.addEventListener('click',()=>{
    mobileMenu.classList.toggle('open');
    menuBtn.textContent=mobileMenu.classList.contains('open')?'Close':'Menu';
  });
}

const WHATSAPP='https://wa.me/34600703303';
const f=document.getElementById('conciergeForm');
if(f){
  f.addEventListener('submit',e=>{
    e.preventDefault();
    const g=id=>document.getElementById(id)?.value||'';
    const msg=`Hello Ibiza VIP Move,%0A%0AI would like to request concierge support.%0A%0AName: ${encodeURIComponent(g('fName'))}%0APhone: ${encodeURIComponent(g('fPhone'))}%0AArrival: ${encodeURIComponent(g('fArrival'))}%0ADeparture: ${encodeURIComponent(g('fDeparture'))}%0AGuests: ${encodeURIComponent(g('fGuests'))}%0AService: ${encodeURIComponent(g('fService'))}%0A%0ABrief:%0A${encodeURIComponent(g('fBrief'))}`;
    window.location.href=WHATSAPP+'?text='+msg;
  });
}
