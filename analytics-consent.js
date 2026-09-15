(() => {
  'use strict';

  const MEASUREMENT_ID = 'G-C21ZKM1V3K';
  const CONSENT_KEY = 'ivm_analytics_consent_v1';
  const SCRIPT_ID = 'ivm-ga4-script';
  let banner = null;
  let analyticsEnabled = false;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };

  const readConsent = () => {
    try { return localStorage.getItem(CONSENT_KEY); } catch (_) { return null; }
  };

  const writeConsent = (value) => {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (_) {}
  };

  const lang = ((document.documentElement.lang || 'en').toLowerCase().split('-')[0]);
  const copy = {
    en: {
      title: 'Analytics cookies',
      text: 'With your permission, we use Google Analytics to understand website usage and improve our private concierge experience. Analytics is not loaded unless you accept.',
      accept: 'Accept analytics',
      reject: 'Reject',
      policy: 'Cookie policy',
      settings: 'Cookie settings'
    },
    es: {
      title: 'Cookies de analítica',
      text: 'Con tu permiso, utilizamos Google Analytics para comprender el uso del sitio y mejorar nuestra experiencia de concierge privado. Analytics no se carga hasta que aceptes.',
      accept: 'Aceptar analítica',
      reject: 'Rechazar',
      policy: 'Política de cookies',
      settings: 'Configurar cookies'
    },
    fr: {
      title: 'Cookies de mesure d’audience',
      text: 'Avec votre accord, nous utilisons Google Analytics pour comprendre l’utilisation du site et améliorer notre service de conciergerie privée. Analytics ne se charge pas sans votre consentement.',
      accept: 'Accepter',
      reject: 'Refuser',
      policy: 'Politique cookies',
      settings: 'Gérer les cookies'
    },
    de: {
      title: 'Analyse-Cookies',
      text: 'Mit Ihrer Zustimmung verwenden wir Google Analytics, um die Nutzung der Website zu verstehen und unseren privaten Concierge-Service zu verbessern. Analytics wird erst nach Ihrer Zustimmung geladen.',
      accept: 'Analyse akzeptieren',
      reject: 'Ablehnen',
      policy: 'Cookie-Richtlinie',
      settings: 'Cookie-Einstellungen'
    },
    ar: {
      title: 'ملفات تعريف الارتباط التحليلية',
      text: 'بموافقتك، نستخدم Google Analytics لفهم استخدام الموقع وتحسين تجربة الكونسيرج الخاصة. لا يتم تحميل Analytics قبل موافقتك.',
      accept: 'قبول التحليلات',
      reject: 'رفض',
      policy: 'سياسة ملفات الارتباط',
      settings: 'إعدادات ملفات الارتباط'
    }
  };
  const t = copy[lang] || copy.en;

  function setConsentAttribute(value){
    document.documentElement.setAttribute('data-analytics-consent', value || 'unset');
  }

  function loadAnalytics(){
    if (analyticsEnabled || document.getElementById(SCRIPT_ID)) return;
    analyticsEnabled = true;
    setConsentAttribute('granted');

    window.gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID, {
      send_page_view: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });

    const script = document.createElement('script');
    script.id = SCRIPT_ID;
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(MEASUREMENT_ID)}`;
    document.head.appendChild(script);
  }

  function sendConversion(detail){
    if (!analyticsEnabled || !detail) return;
    const eventName = String(detail.conversion_type || 'ivm_conversion').replace(/[^a-zA-Z0-9_]/g, '_').slice(0, 40);
    const params = { ...detail };
    delete params.event;
    delete params.conversion_type;
    window.gtag('event', eventName, params);
  }

  window.addEventListener('ivm:conversion', (event) => sendConversion(event.detail));

  function ensureStyles(){
    if (document.getElementById('ivm-consent-styles')) return;
    const style = document.createElement('style');
    style.id = 'ivm-consent-styles';
    style.textContent = `
      .ivm-consent{position:fixed;z-index:2147483000;left:18px;right:18px;bottom:18px;max-width:760px;margin:0 auto;background:#0a0f14;color:#f4efe8;border:1px solid rgba(197,157,94,.42);box-shadow:0 18px 60px rgba(0,0,0,.38);padding:20px 22px;font-family:Manrope,Arial,sans-serif}
      .ivm-consent[hidden]{display:none!important}.ivm-consent h2{margin:0 0 8px;font-family:"Cormorant Garamond",Georgia,serif;font-size:28px;font-weight:500}.ivm-consent p{margin:0;color:#d8d1c7;font-size:13px;line-height:1.65}.ivm-consent-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;align-items:center}.ivm-consent button,.ivm-cookie-settings{appearance:none;border:1px solid #c59d5e;background:transparent;color:inherit;padding:11px 16px;font:500 12px/1 Manrope,Arial,sans-serif;letter-spacing:.04em;cursor:pointer}.ivm-consent .ivm-accept{background:#c59d5e;color:#0a0f14}.ivm-consent a{color:#f4efe8;text-underline-offset:3px;font-size:12px}.ivm-cookie-settings{padding:0;border:0;text-decoration:underline;text-underline-offset:3px;color:inherit;opacity:.8;background:none}.ivm-cookie-settings:hover{opacity:1}@media(max-width:600px){.ivm-consent{left:10px;right:10px;bottom:10px;padding:18px}.ivm-consent-actions{align-items:stretch}.ivm-consent-actions button{flex:1 1 145px}.ivm-consent-actions a{width:100%;padding-top:4px}}`;
    document.head.appendChild(style);
  }

  function closeBanner(){
    if (banner) banner.hidden = true;
  }

  function choose(value){
    writeConsent(value);
    setConsentAttribute(value);
    closeBanner();
    if (value === 'granted') loadAnalytics();
  }

  function buildBanner(){
    if (banner) return banner;
    ensureStyles();
    banner = document.createElement('section');
    banner.className = 'ivm-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-labelledby', 'ivm-consent-title');
    if (lang === 'ar') banner.dir = 'rtl';
    banner.innerHTML = `
      <h2 id="ivm-consent-title"></h2>
      <p class="ivm-consent-copy"></p>
      <div class="ivm-consent-actions">
        <button type="button" class="ivm-accept"></button>
        <button type="button" class="ivm-reject"></button>
        <a href="/cookies/"></a>
      </div>`;
    banner.querySelector('h2').textContent = t.title;
    banner.querySelector('.ivm-consent-copy').textContent = t.text;
    banner.querySelector('.ivm-accept').textContent = t.accept;
    banner.querySelector('.ivm-reject').textContent = t.reject;
    banner.querySelector('a').textContent = t.policy;
    banner.querySelector('.ivm-accept').addEventListener('click', () => choose('granted'));
    banner.querySelector('.ivm-reject').addEventListener('click', () => choose('denied'));
    document.body.appendChild(banner);
    return banner;
  }

  function openBanner(){
    buildBanner().hidden = false;
  }

  function addSettingsControl(){
    if (document.querySelector('.ivm-cookie-settings')) return;
    const footer = document.querySelector('footer');
    if (!footer) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ivm-cookie-settings';
    button.textContent = t.settings;
    button.addEventListener('click', openBanner);
    const target = footer.querySelector('.footer-bottom') || footer;
    target.appendChild(button);
  }

  const initialConsent = readConsent();
  setConsentAttribute(initialConsent);
  addSettingsControl();

  if (initialConsent === 'granted') {
    loadAnalytics();
  } else if (initialConsent !== 'denied') {
    openBanner();
  }

  window.IVMCookieConsent = {
    open: openBanner,
    accept: () => choose('granted'),
    reject: () => choose('denied'),
    status: () => readConsent()
  };
})();
