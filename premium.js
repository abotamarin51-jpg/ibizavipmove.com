const menuBtn=document.querySelector('.menu-btn');const mobileMenu=document.querySelector('.mobile-menu');if(menuBtn&&mobileMenu){menuBtn.addEventListener('click',()=>{mobileMenu.classList.toggle('open');menuBtn.textContent=mobileMenu.classList.contains('open')?'Close':'Menu';});}

const PHONE_DISPLAY='+34 600 703 303';
const PHONE_TEL='tel:+34600703303';
const WHATSAPP='https://wa.me/34600703303';

const logoUrl='/assets/brand-logo.svg?v=3';
const wordmark=document.querySelector('.wordmark');if(wordmark){wordmark.innerHTML='<img src="'+logoUrl+'" alt="Ibiza VIP Move">';const i=wordmark.querySelector('img');i.style.display='block';i.style.width='auto';i.style.height=window.matchMedia('(max-width:600px)').matches?'38px':'50px';i.style.maxWidth=window.matchMedia('(max-width:600px)').matches?'190px':'245px';i.style.objectFit='contain';}
const footerBrand=document.querySelector('.footer-brand');if(footerBrand){footerBrand.innerHTML='<img src="'+logoUrl+'" alt="Ibiza VIP Move">';const i=footerBrand.querySelector('img');i.style.display='block';i.style.width='auto';i.style.height='52px';i.style.maxWidth='260px';i.style.objectFit='contain';}

document.querySelectorAll('a[href^="tel:+34613756211"]').forEach(a=>{a.href=PHONE_TEL;if(/613\s*75\s*62\s*11/.test(a.textContent))a.textContent=PHONE_DISPLAY;});
document.querySelectorAll('a[href^="https://wa.me/34613756211"]').forEach(a=>{a.href=a.href.replace('https://wa.me/34613756211',WHATSAPP);});
document.querySelectorAll('script[type="application/ld+json"]').forEach(s=>{try{const d=JSON.parse(s.textContent);if(d&&d.telephone)d.telephone=PHONE_DISPLAY;s.textContent=JSON.stringify(d);}catch(e){}});

const f=document.getElementById('conciergeForm');if(f){f.addEventListener('submit',e=>{e.preventDefault();const g=id=>document.getElementById(id)?.value||'';const msg=`Hello Ibiza VIP Move,%0A%0AI would like to request concierge support.%0A%0AName: ${encodeURIComponent(g('fName'))}%0APhone: ${encodeURIComponent(g('fPhone'))}%0AArrival: ${encodeURIComponent(g('fArrival'))}%0ADeparture: ${encodeURIComponent(g('fDeparture'))}%0AGuests: ${encodeURIComponent(g('fGuests'))}%0AService: ${encodeURIComponent(g('fService'))}%0A%0ABrief:%0A${encodeURIComponent(g('fBrief'))}`;window.location.href=WHATSAPP+'?text='+msg;});}
