(() => {
  const yachtForm = document.querySelector('#yacht-enquiry');
  const dateField = document.querySelector('#yacht-date');
  const guestField = document.querySelector('#yacht-guests');
  const messagePreview = document.querySelector('#yacht-message');
  const whatsappLink = document.querySelector('#yacht-whatsapp');
  const today = new Date();
  const localDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000);
  dateField.min = localDate.toISOString().slice(0, 10);
  yachtForm.hidden = false;
  yachtForm.addEventListener('input', () => {
    messagePreview.hidden = true;
    whatsappLink.removeAttribute('href');
  });
  yachtForm.addEventListener('submit', event => {
    event.preventDefault();
    if (!yachtForm.reportValidity()) return;
    const date = new Intl.DateTimeFormat('fr-FR', {dateStyle:'long'}).format(new Date(dateField.value + 'T12:00:00'));
    const guests = guestField.valueAsNumber;
    const message = `Bonjour Ibiza VIP Move, je souhaite louer un yacht privé au départ d’Ibiza le ${date}, pour ${guests} ${guests === 1 ? 'passager' : 'passagers'}. Pourriez-vous m’indiquer les options disponibles, le tarif et ce qui est inclus ?`;
    document.querySelector('#yacht-message-text').textContent = message;
    whatsappLink.href = `https://wa.me/34600703303?text=${encodeURIComponent(message)}`;
    messagePreview.hidden = false;
    whatsappLink.focus();
  });
})();
