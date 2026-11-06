(() => {
  const planner = document.getElementById('origin-planner');
  if (!planner) return;
  const country = planner.querySelector('#origin-country');
  const city = planner.querySelector('#origin-city');
  const custom = planner.querySelector('#origin-custom');
  const service = planner.querySelector('#origin-service');
  const whatsapp = planner.querySelector('#origin-whatsapp');
  const groups = Array.from(city.querySelectorAll('optgroup'));
  const locale = document.documentElement.lang || 'en';

  function updateCities() {
    const group = groups.find(item => item.dataset.country === country.value);
    city.querySelector('optgroup')?.remove();
    if (group) city.add(group, city.querySelector('option[value="other"]'));
    city.value = '';
    city.disabled = !group;
    custom.value = '';
  }

  function clock(zone, instant) {
    return new Intl.DateTimeFormat(locale, {
      weekday: 'short', hour: 'numeric', minute: '2-digit', timeZone: zone
    }).format(instant);
  }

  function updateClocks() {
    const now = new Date();
    const zone = city.selectedOptions[0]?.dataset.zone;
    planner.querySelector('#origin-ibiza-time').textContent = clock('Europe/Madrid', now);
    const local = planner.querySelector('#origin-local-clock');
    local.hidden = !zone;
    if (zone) local.querySelector('strong').textContent = clock(zone, now);
  }

  function refresh() {
    const customOrigin = country.value === 'other' || city.value === 'other';
    custom.closest('label').hidden = !customOrigin;
    const region = country.value && country.value !== 'other' ? country.selectedOptions[0].textContent : '';
    const place = customOrigin ? custom.value.trim() : (city.value ? city.selectedOptions[0].textContent : '');
    const from = [place, region].filter(Boolean).join(', ') || '__';
    const message = planner.dataset.message.replace('{origin}', () => from)
      .replace('{service}', () => service.selectedOptions[0].textContent);
    const link = new URL('https://wa.me/34600703303');
    link.searchParams.set('text', message);
    whatsapp.href = link.href;
    updateClocks();
  }

  function updateLocation() {
    const url = new URL(location.href);
    const key = country.value && country.value !== 'other' ? country.value.toLowerCase() : '';
    const cityKey = city.value && city.value !== 'other' ? '-' + city.value : '';
    url.hash = key ? 'from-' + key + cityKey : 'origin-planner';
    history.replaceState(null, '', url);
  }

  function openSharedOrigin() {
    const match = /^#from-([a-z]{2})(?:-([a-z0-9-]+))?$/.exec(location.hash);
    if (!match || !groups.some(group => group.dataset.country === match[1].toUpperCase())) return;
    country.value = match[1].toUpperCase();
    updateCities();
    if (match[2] && Array.from(city.options).some(option => option.value === match[2])) city.value = match[2];
    refresh();
    planner.scrollIntoView({block: 'start'});
  }

  // Keep the fallback and localized contact form available without JavaScript.
  groups.forEach(group => group.remove());
  country.addEventListener('change', () => { updateCities(); refresh(); updateLocation(); });
  city.addEventListener('change', () => { custom.value = ''; refresh(); updateLocation(); });
  custom.addEventListener('input', refresh);
  service.addEventListener('change', refresh);
  window.addEventListener('hashchange', openSharedOrigin);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) updateClocks(); });
  window.setInterval(() => { if (!document.hidden) updateClocks(); }, 60000);
  updateCities();
  refresh();
  planner.querySelector('.origin-fields').hidden = false;
  openSharedOrigin();
})();
