(()=>{
  const path=window.location.pathname;
  const SERVICE_BY_PATH={
    '/private-chauffeur-ibiza/':'chauffeur','/luxury-villas-ibiza/':'villas','/yacht-charter-ibiza/':'yacht','/private-aviation-ibiza/':'aviation','/restaurants-nightlife-ibiza/':'access','/private-security-ibiza/':'security',
    '/es/chauffeur-privado-ibiza/':'chauffeur','/es/villas-lujo-ibiza/':'villas','/es/yate-privado-ibiza/':'yacht','/es/aviacion-privada-ibiza/':'aviation','/es/seguridad-privada-ibiza/':'security',
    '/fr/chauffeur-prive-ibiza/':'chauffeur','/fr/villas-luxe-ibiza/':'villas','/fr/location-yacht-ibiza/':'yacht','/fr/aviation-privee-ibiza/':'aviation','/fr/securite-privee-ibiza/':'security',
    '/de/privater-chauffeur-ibiza/':'chauffeur','/de/luxusvillen-ibiza/':'villas','/de/yachtcharter-ibiza/':'yacht','/de/private-aviation-ibiza/':'aviation','/de/private-sicherheit-ibiza/':'security',
    '/ar/private-chauffeur-ibiza/':'chauffeur','/ar/luxury-villas-ibiza/':'villas','/ar/yacht-charter-ibiza/':'yacht','/ar/private-aviation-ibiza/':'aviation','/ar/private-security-ibiza/':'security'
  };
  const CONTACT_BY_LANG={en:'/contact/',es:'/es/contacto/',fr:'/fr/contact/',de:'/de/kontakt/',ar:'/ar/contact/'};
  const LABELS={
    en:{chauffeur:'Private Chauffeur & Transportation',villas:'Luxury Villas & Private Stays',yacht:'Yachts & Charters',aviation:'Private Aviation',access:'Restaurants, Beach Clubs & Nightlife',security:'Security & Close Protection'},
    es:{chauffeur:'Chófer privado',villas:'Villa privada',yacht:'Yate / Charter',aviation:'Aviación privada',access:'Restaurantes / Nightlife',security:'Seguridad privada'},
    fr:{chauffeur:'Chauffeur privé',villas:'Villa privée',yacht:'Yacht / Charter',aviation:'Aviation privée',access:'Restaurants / Nightlife',security:'Sécurité privée'},
    de:{chauffeur:'Privater Chauffeur',villas:'Private Villa',yacht:'Yacht / Charter',aviation:'Private Aviation',access:'Restaurants / Nightlife',security:'Private Security'},
    ar:{chauffeur:'سائق خاص',villas:'فيلا خاصة',yacht:'يخت / تشارتر',aviation:'طيران خاص',access:'مطاعم / حياة ليلية',security:'أمن خاص'}
  };
  const lang=(document.documentElement.lang||'en').toLowerCase().split('-')[0];
  const service=SERVICE_BY_PATH[path];
  const labels=LABELS[lang]||LABELS.en;
  const contact=CONTACT_BY_LANG[lang]||CONTACT_BY_LANG.en;

  if(service){
    const target=contact+'?service='+encodeURIComponent(service);
    document.querySelectorAll('a').forEach(a=>{
      const href=(a.getAttribute('href')||'').trim();
      if(href==='/contact/'||href==='/es/contacto/'||href==='/fr/contact/'||href==='/de/kontakt/'||href==='/ar/contact/')a.setAttribute('href',target);
    });
    const serviceLabel=labels[service]||service;
    const waText=`Hello Ibiza VIP Move,\n\nI would like to enquire about ${serviceLabel} for an upcoming stay in Ibiza.\n\nPlease let me know the best way to share my dates and requirements.\n\nThank you.`;
    document.querySelectorAll('a[href^="https://wa.me/34600703303"]').forEach(a=>{
      a.href='https://wa.me/34600703303?text='+encodeURIComponent(waText);
    });
  }

  const params=new URLSearchParams(window.location.search);
  const requested=params.get('service');
  if(requested&&labels[requested]){
    const select=document.getElementById('fService');
    if(select){
      const wanted=labels[requested];
      const option=[...select.options].find(o=>o.value===wanted||o.textContent.trim()===wanted);
      if(option){select.value=option.value;select.dispatchEvent(new Event('change',{bubbles:true}));}
    }
    document.body.dataset.ivmRequestedService=requested;
  }
})();
