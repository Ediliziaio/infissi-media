/* Infissi Media — Cookie consent GDPR, zero dipendenze, ~2KB, caricato con defer */
(function () {
  'use strict';
  var KEY = 'im_cookie_consent';
  var PREFIX = location.pathname.indexOf('/articoli/') > -1 ? '../' : '';
  var POLICY = PREFIX + 'cookie-policy.html';

  function get() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  }
  function store(v) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: v, ts: Date.now() })); } catch (e) {}
    window.imConsent = v;
    document.dispatchEvent(new CustomEvent('im:consent', { detail: v }));
  }
  function hide() {
    var b = document.getElementById('im-cookie-banner');
    if (!b) return;
    b.classList.add('cb-hide');
    setTimeout(function () { b.remove(); }, 400);
  }
  function show() {
    if (document.getElementById('im-cookie-banner')) return;
    var b = document.createElement('div');
    b.id = 'im-cookie-banner';
    b.className = 'cookie-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-live', 'polite');
    b.setAttribute('aria-label', 'Informativa sui cookie');
    b.innerHTML =
      '<div class="cb-inner">' +
        '<p class="cb-text"><strong>Questo sito utilizza i cookie.</strong> ' +
        'Usiamo cookie tecnici necessari al funzionamento e, previo tuo consenso, cookie di terze parti per analisi e pubblicità personalizzata. ' +
        '<a href="' + POLICY + '">Leggi la Cookie Policy</a>.</p>' +
        '<div class="cb-actions">' +
          '<button type="button" class="cb-btn cb-accept" id="cb-accept">Accetta tutto</button>' +
          '<button type="button" class="cb-btn cb-reject" id="cb-reject">Rifiuta</button>' +
          '<a class="cb-link" href="' + POLICY + '">Personalizza</a>' +
        '</div>' +
      '</div>';
    document.body.appendChild(b);
    requestAnimationFrame(function () { b.classList.add('cb-show'); });
    document.getElementById('cb-accept').addEventListener('click', function () { store('all'); hide(); });
    document.getElementById('cb-reject').addEventListener('click', function () { store('necessary'); hide(); });
  }

  window.imCookieSettings = show;
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-cookie-settings]');
    if (t) { e.preventDefault(); show(); }
  });

  var consent = get();
  if (consent && consent.v) {
    window.imConsent = consent.v;
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', show);
  } else {
    show();
  }
})();
