(()=>{
  const f=document.getElementById('conciergeForm');
  if(!f)return;

  const WA='https://wa.me/34600703303';
  const lang=(document.documentElement.lang||'en').toLowerCase().split('-')[0];
  const copy={
    en:{
      hello:'Hello Ibiza VIP Move,',
      intro:'I would like to request private concierge assistance in Ibiza.',
      role:'I am',area:'Stay / area',name:'Name',phone:'Phone',arrival:'Arrival',departure:'Departure',guests:'Guests',service:'Service',brief:'Brief',
      tbc:'To be confirmed',fallback:'I would like to discuss the details privately.',close:'Please let me know availability and the next steps. Thank you.'
    },
    es:{
      hello:'Hola Ibiza VIP Move,',
      intro:'Me gustaría solicitar asistencia de concierge privado en Ibiza.',
      role:'Perfil',area:'Estancia / zona',name:'Nombre',phone:'Teléfono',arrival:'Llegada',departure:'Salida',guests:'Huéspedes',service:'Servicio',brief:'Brief',
      tbc:'Por confirmar',fallback:'Me gustaría comentar los detalles de forma privada.',close:'Por favor, indíquenme disponibilidad y próximos pasos. Muchas gracias.'
    },
    fr:{
      hello:'Bonjour Ibiza VIP Move,',
      intro:'Je souhaite demander une assistance de conciergerie privée à Ibiza.',
      role:'Profil',area:'Séjour / zone',name:'Nom',phone:'Téléphone',arrival:'Arrivée',departure:'Départ',guests:'Invités',service:'Service',brief:'Brief',
      tbc:'À confirmer',fallback:'Je souhaite discuter des détails en privé.',close:'Merci de m’indiquer les disponibilités et les prochaines étapes.'
    },
    de:{
      hello:'Hallo Ibiza VIP Move,',
      intro:'Ich möchte private Concierge-Unterstützung auf Ibiza anfragen.',
      role:'Profil',area:'Aufenthalt / Region',name:'Name',phone:'Telefon',arrival:'Anreise',departure:'Abreise',guests:'Gäste',service:'Service',brief:'Brief',
      tbc:'Noch zu bestätigen',fallback:'Ich möchte die Details gerne privat besprechen.',close:'Bitte teilen Sie mir Verfügbarkeit und die nächsten Schritte mit. Vielen Dank.'
    },
    ar:{
      hello:'مرحباً Ibiza VIP Move،',
      intro:'أرغب في طلب مساعدة كونسيرج خاصة في إيبيزا.',
      role:'الصفة',area:'الإقامة / المنطقة',name:'الاسم',phone:'الهاتف',arrival:'الوصول',departure:'المغادرة',guests:'الضيوف',service:'الخدمة',brief:'التفاصيل',
      tbc:'يتم التأكيد لاحقاً',fallback:'أرغب في مناقشة التفاصيل بشكل خاص.',close:'يرجى إبلاغي بالتوفر والخطوات التالية. شكراً.'
    }
  };
  const c=copy[lang]||copy.en;
  const g=id=>document.getElementById(id)?.value||'';
  const selectedText=id=>{
    const el=document.getElementById(id);
    if(!el)return'';
    const option=el.options?.[el.selectedIndex];
    return(option?.textContent||el.value||'').trim();
  };
  const bucketGuests=value=>{
    const n=Number(value||0);
    if(!n)return'unknown';
    if(n<=2)return'1-2';
    if(n<=6)return'3-6';
    if(n<=12)return'7-12';
    return'13+';
  };
  const bucketLeadTime=value=>{
    if(!value)return'unknown';
    const arrival=new Date(value+'T12:00:00');
    const now=new Date();
    const days=Math.ceil((arrival-now)/(1000*60*60*24));
    if(!Number.isFinite(days))return'unknown';
    if(days<=2)return'0-2_days';
    if(days<=7)return'3-7_days';
    if(days<=30)return'8-30_days';
    return'31+_days';
  };
  const attribution=()=>{
    try{return JSON.parse(sessionStorage.getItem('ivm_attribution_v1')||'{}')||{};}catch(_){return{};}
  };

  f.addEventListener('submit',e=>{
    e.preventDefault();
    e.stopImmediatePropagation();
    if(!f.reportValidity())return;

    const role=document.getElementById('fClientType');
    const area=document.getElementById('fArea');
    const roleCode=role?.value||'not_specified';
    const areaCode=area?.value||'not_specified';
    const service=g('fService')||'Full Concierge';

    // ANALYTICS_NO_PII_START
    const payload={
      event:'ivm_qualified_lead',
      page_path:window.location.pathname,
      page_language:document.documentElement.lang||'en',
      lead_role:roleCode,
      stay_area:areaCode,
      service,
      guests_bucket:bucketGuests(g('fGuests')),
      lead_time_bucket:bucketLeadTime(g('fArrival')),
      brief_present:Boolean(g('fBrief').trim()),
      ...attribution()
    };
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push(payload);
    window.dispatchEvent(new CustomEvent('ivm:qualified-lead',{detail:payload}));
    // ANALYTICS_NO_PII_END

    const lines=[
      c.hello,
      '',
      c.intro,
      '',
      `${c.role}: ${selectedText('fClientType')||c.tbc}`,
      `${c.area}: ${selectedText('fArea')||c.tbc}`,
      `${c.name}: ${g('fName')}`,
      `${c.phone}: ${g('fPhone')}`,
      `${c.arrival}: ${g('fArrival')||c.tbc}`,
      `${c.departure}: ${g('fDeparture')||c.tbc}`,
      `${c.guests}: ${g('fGuests')||c.tbc}`,
      `${c.service}: ${service}`,
      '',
      `${c.brief}:`,
      g('fBrief')||c.fallback,
      '',
      c.close
    ];
    window.location.href=WA+'?text='+encodeURIComponent(lines.join('\n'));
  },true);
})();
