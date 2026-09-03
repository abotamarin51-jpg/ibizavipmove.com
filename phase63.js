(()=>{
  const path=window.location.pathname;
  const CONTACT={en:'/contact/',es:'/es/contacto/',fr:'/fr/contact/',de:'/de/kontakt/',ar:'/ar/contact/'};
  const lang=(document.documentElement.lang||'en').toLowerCase().split('-')[0];
  const SERVICE_BY_PATH={
    '/private-chauffeur-ibiza/':'chauffeur','/es/chauffeur-privado-ibiza/':'chauffeur','/fr/chauffeur-prive-ibiza/':'chauffeur','/de/privater-chauffeur-ibiza/':'chauffeur','/ar/private-chauffeur-ibiza/':'chauffeur',
    '/luxury-villas-ibiza/':'villas','/es/villas-lujo-ibiza/':'villas','/fr/villas-luxe-ibiza/':'villas','/de/luxusvillen-ibiza/':'villas','/ar/luxury-villas-ibiza/':'villas',
    '/yacht-charter-ibiza/':'yacht','/es/yate-privado-ibiza/':'yacht','/fr/location-yacht-ibiza/':'yacht','/de/yachtcharter-ibiza/':'yacht','/ar/yacht-charter-ibiza/':'yacht',
    '/private-aviation-ibiza/':'aviation','/es/aviacion-privada-ibiza/':'aviation','/fr/aviation-privee-ibiza/':'aviation','/de/private-aviation-ibiza/':'aviation','/ar/private-aviation-ibiza/':'aviation',
    '/restaurants-nightlife-ibiza/':'access','/es/restaurantes-nightlife-ibiza/':'access','/fr/restaurants-nightlife-ibiza/':'access','/de/restaurants-nightlife-ibiza/':'access','/ar/restaurants-nightlife-ibiza/':'access',
    '/private-security-ibiza/':'security','/es/seguridad-privada-ibiza/':'security','/fr/securite-privee-ibiza/':'security','/de/private-sicherheit-ibiza/':'security','/ar/private-security-ibiza/':'security',
    '/private-chef-staffing-ibiza/':'chef','/es/chef-privado-staffing-ibiza/':'chef','/fr/chef-prive-personnel-villa-ibiza/':'chef','/de/privatkoch-villa-staff-ibiza/':'chef','/ar/private-chef-staffing-ibiza/':'chef',
    '/luxury-car-rental-ibiza/':'car','/es/alquiler-coches-lujo-ibiza/':'car','/fr/location-voiture-luxe-ibiza/':'car','/de/luxusauto-mieten-ibiza/':'car','/ar/luxury-car-rental-ibiza/':'car',
    '/wellness-ibiza/':'wellness','/es/wellness-ibiza/':'wellness','/fr/wellness-ibiza/':'wellness','/de/wellness-ibiza/':'wellness','/ar/wellness-ibiza/':'wellness',
    '/private-events-ibiza/':'events','/es/eventos-privados-ibiza/':'events','/fr/evenements-prives-ibiza/':'events','/de/private-events-ibiza/':'events','/ar/private-events-ibiza/':'events',
    '/bespoke-concierge-ibiza/':'bespoke','/es/concierge-a-medida-ibiza/':'bespoke','/fr/conciergerie-sur-mesure-ibiza/':'bespoke','/de/bespoke-concierge-ibiza/':'bespoke','/ar/bespoke-concierge-ibiza/':'bespoke'
  };
  const LABELS={
    en:{chauffeur:'Private Chauffeur & Transportation',villas:'Luxury Villas & Private Stays',yacht:'Yachts & Charters',aviation:'Private Aviation',access:'Restaurants, Beach Clubs & Nightlife',security:'Security & Close Protection',chef:'Private Chefs & Villa Staffing',car:'Luxury & Supercar Rental',wellness:'Wellness & Beauty',events:'Private Events & Celebrations',bespoke:'Lifestyle & Bespoke Requests'},
    es:{chauffeur:'Chófer privado',villas:'Villa privada',yacht:'Yate / Charter',aviation:'Aviación privada',access:'Restaurantes / Nightlife',security:'Seguridad privada',chef:'Chef / Staffing',car:'Alquiler de coche de lujo',wellness:'Wellness',events:'Evento privado',bespoke:'Solicitud a medida'},
    fr:{chauffeur:'Chauffeur privé',villas:'Villa privée',yacht:'Yacht / Charter',aviation:'Aviation privée',access:'Restaurants / Nightlife',security:'Sécurité privée',chef:'Chef / Personnel de villa',car:'Location de voiture de luxe',wellness:'Wellness',events:'Événement privé',bespoke:'Demande sur mesure'},
    de:{chauffeur:'Privater Chauffeur',villas:'Private Villa',yacht:'Yacht / Charter',aviation:'Private Aviation',access:'Restaurants / Nightlife',security:'Private Security',chef:'Private Chef / Villa Staff',car:'Luxusauto / Supercar Rental',wellness:'Wellness',events:'Private Event',bespoke:'Bespoke Request'},
    ar:{chauffeur:'سائق خاص',villas:'فيلا خاصة',yacht:'يخت / تشارتر',aviation:'طيران خاص',access:'مطاعم / حياة ليلية',security:'أمن خاص',chef:'شيف / طاقم فيلا',car:'تأجير سيارة فاخرة',wellness:'عافية وجمال',events:'فعالية خاصة',bespoke:'طلب مخصص'}
  };
  const templates={
    en:s=>`Hello Ibiza VIP Move,\n\nI would like to enquire about ${s} for an upcoming stay in Ibiza.\n\nPlease let me know the best way to share my dates, guests and requirements.\n\nThank you.`,
    es:s=>`Hola Ibiza VIP Move,\n\nMe gustaría consultar sobre ${s} para una próxima estancia en Ibiza.\n\nPor favor, indíquenme la mejor forma de compartir fechas, huéspedes y necesidades.\n\nMuchas gracias.`,
    fr:s=>`Bonjour Ibiza VIP Move,\n\nJe souhaite vous consulter au sujet de ${s} pour un prochain séjour à Ibiza.\n\nMerci de m’indiquer la meilleure façon de partager mes dates, le nombre d’invités et mes besoins.\n\nMerci.`,
    de:s=>`Hallo Ibiza VIP Move,\n\nich möchte ${s} für einen bevorstehenden Aufenthalt auf Ibiza anfragen.\n\nBitte teilen Sie mir mit, wie ich Reisedaten, Gästezahl und Anforderungen am besten übermitteln kann.\n\nVielen Dank.`,
    ar:s=>`مرحباً Ibiza VIP Move،\n\nأرغب في الاستفسار عن ${s} لإقامة قادمة في إيبيزا.\n\nيرجى إخباري بأفضل طريقة لمشاركة التواريخ وعدد الضيوف والمتطلبات.\n\nشكراً.`
  };
  const labels=LABELS[lang]||LABELS.en;
  const contact=CONTACT[lang]||CONTACT.en;
  const service=SERVICE_BY_PATH[path];

  if(service){
    const label=labels[service]||service;
    const target=contact+'?service='+encodeURIComponent(service);
    document.querySelectorAll('a').forEach(a=>{
      const href=(a.getAttribute('href')||'').trim();
      if(Object.values(CONTACT).includes(href))a.setAttribute('href',target);
    });
    const msg=(templates[lang]||templates.en)(label);
    document.querySelectorAll('a[href^="https://wa.me/34600703303"]').forEach(a=>{
      a.href='https://wa.me/34600703303?text='+encodeURIComponent(msg);
      a.dataset.ivmService=service;
    });
    document.body.dataset.ivmServiceContext=service;
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
