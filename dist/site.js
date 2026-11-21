(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduced) {
    document.documentElement.classList.add('js-motion');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.08});
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }
  const dialog = document.querySelector('#offer-dialog');
  let opener;
  document.querySelectorAll('[data-offer]').forEach(button => button.addEventListener('click', () => {
    opener = button;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  }));
  dialog.querySelector('.close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    }
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = '';
    opener?.focus();
  });
  const menu = document.querySelector('.menu-toggle');
  menu.addEventListener('click', () => {
    const open = document.querySelector('.nav').classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  document.querySelectorAll('.nav nav a').forEach(link => link.addEventListener('click', () => {
    document.querySelector('.nav').classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Abrir menú');
  }));
  const booking = document.querySelector('.booking');
  if (booking) {
    const today = new Date();
    const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    const arrival = booking.elements.arrival;
    const departure = booking.elements.departure;
    arrival.min = localToday;
    departure.min = localToday;
    arrival.addEventListener('change', () => {
      departure.min = arrival.value;
      departure.setCustomValidity('');
    });
    departure.addEventListener('change', () => departure.setCustomValidity(''));
    booking.addEventListener('submit', event => {
      event.preventDefault();
      if (departure.value <= arrival.value) {
        departure.setCustomValidity('La salida debe ser posterior a la llegada.');
        departure.reportValidity();
        return;
      }
      const text = `Hola, quisiera consultar disponibilidad del ${arrival.value} al ${departure.value} para ${booking.elements.guests.value} huésped(es).`;
      window.open(booking.dataset.wa + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    });
  }
})();
