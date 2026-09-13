/* The Polycrafted: navigation, reveal, forms */
(function () {
  // mobile nav
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  // current page marker
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav ul a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === here || (here === '' && href === 'index.html')) a.setAttribute('aria-current', 'page');
  });

  // reveal on scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // forms: post to the endpoint in data-endpoint, show status inline
  document.querySelectorAll('form[data-endpoint]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (form.querySelector('.honey input') && form.querySelector('.honey input').value) return;
      var btn = form.querySelector('[type=submit]');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending'; }
      if (status) { status.textContent = ''; status.className = 'form-status'; }
      fetch(form.dataset.endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error('bad'); return r.json ? r.json().catch(function () { return {}; }) : {}; })
        .then(function () {
          form.reset();
          if (status) { status.textContent = form.dataset.success || 'Received. We reply within one business day.'; status.className = 'form-status ok'; }
          if (form.dataset.download) { window.location.href = form.dataset.download; }
        })
        .catch(function () {
          if (status) { status.textContent = 'Something went wrong. Email info@thepolycrafted.com and we will take it from there.'; status.className = 'form-status err'; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || 'Send'; } });
    });
  });

  // year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
