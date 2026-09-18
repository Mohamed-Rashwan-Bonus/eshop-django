// E-Shop micro-interactions
document.addEventListener('DOMContentLoaded', () => {
  // Bootstrap toasts for Django messages
  document.querySelectorAll('.toast').forEach(el => {
    try { new bootstrap.Toast(el, { delay: 3500 }).show(); } catch (e) { /* no bootstrap */ }
  });

  // bump cart badge after add-to-cart clicks
  document.querySelectorAll('a[href*="/cart/add/"]').forEach(a => {
    a.addEventListener('click', () => {
      const b = document.querySelector('.cart-count-badge');
      if (b) { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); }
    });
  });

  // confirm destructive actions
  document.querySelectorAll('[data-confirm]').forEach(a => {
    a.addEventListener('click', e => {
      if (!confirm(a.getAttribute('data-confirm'))) e.preventDefault();
    });
  });

  // quantity steppers on detail page
  document.querySelectorAll('[data-qty-plus],[data-qty-minus]').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.querySelector(btn.getAttribute('data-target'));
      if (!input) return;
      const max = parseInt(input.max || '99', 10);
      let v = parseInt(input.value || '1', 10);
      if (btn.hasAttribute('data-qty-plus')) v = Math.min(max, v + 1);
      else v = Math.max(1, v - 1);
      input.value = v;
    });
  });

  // press "/" to focus search
  document.addEventListener('keydown', e => {
    if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)) {
      const s = document.querySelector('input[name="q"]');
      if (s) { e.preventDefault(); s.focus(); }
    }
  });
});
