/* Map existing static-site CMP choices to EICAnalytics. No tracker IDs here. */
(function (w, d) {
  'use strict';
  if (w.__EIC_STATIC_CONSENT_ADAPTER__) return;
  w.__EIC_STATIC_CONSENT_ADAPTER__ = true;
  var config = w.EIC_STATIC_CONSENT_CONFIG || {};
  var kind = config.kind;
  var memoryDenied = false;

  function stored() {
    var raw;
    try { raw = w.localStorage.getItem(config.storageKey); } catch (_) { return null; }
    if (kind === 'ge' || kind === 'im') {
      try { return JSON.parse(raw || 'null'); } catch (_) { return null; }
    }
    return raw;
  }

  function normalize(value) {
    if (kind === 'ge') return value && typeof value.analytics === 'boolean' && typeof value.marketing === 'boolean' ? { analytics: value.analytics, marketing: value.marketing } : null;
    if (kind === 'im') return value && (value.v === 'all' || value.v === 'necessary') ? { analytics: value.v === 'all', marketing: false } : null;
    if (kind === 'rc') return value === 'all' || value === 'necessary' ? { analytics: value === 'all', marketing: false } : null;
    if (value !== 'accepted' && value !== 'rejected') return null;
    return { analytics: value === 'accepted', marketing: kind === 'ie' && value === 'accepted' };
  }

  function sync(event) {
    if (!w.EICAnalytics) return;
    var saved = normalize(stored());
    var detail = event && event.detail;
    var selected = detail && typeof detail.analytics === 'boolean' ? { analytics: detail.analytics, marketing: detail.marketing === true } : kind === 'im' && typeof detail === 'string' ? normalize({ v: detail }) : null;
    if (selected && (!selected.analytics && (!saved || saved.analytics) || kind === 'ie' && !selected.marketing && (!saved || saved.marketing))) {
      memoryDenied = true;
      w.EICAnalytics.configure(Object.assign({}, w.EIC_ANALYTICS_CONFIG, { reloadOnRevoke: false }));
    }
    w.EICAnalytics.updateConsent(memoryDenied ? { analytics: false, marketing: false } : selected || saved || { analytics: false, marketing: false });
  }

  var events = { gs: 'gs:consent', ic: 'ic:consent', ie: 'ie:consent', ge: 'ge:consent', im: 'im:consent', rc: 'rc:consent' };
  (kind === 'im' ? d : w).addEventListener(events[kind], sync);
  w.addEventListener('storage', function (event) { if (event.key === config.storageKey || event.key === null) sync(); });

  function fallbackRistoroBanner() {
    var box = d.getElementById('cookieBanner');
    if (box) { box.classList.add('show'); return; }
    if (d.getElementById('eic-cookie-fallback')) return;
    box = d.createElement('div');
    box.id = 'eic-cookie-fallback';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Preferenze cookie');
    box.style.cssText = 'position:fixed;left:16px;right:16px;bottom:70px;z-index:10000;max-width:760px;margin:auto;padding:20px;background:#fff;color:#17212e;border:1px solid #c7ced8;border-radius:12px;box-shadow:0 8px 36px #0002;font:15px/1.5 system-ui';
    box.innerHTML = '<p>Usiamo cookie tecnici e, con il tuo consenso, strumenti Google Analytics per le statistiche di utilizzo. <a href="/cookie.html">Informativa cookie</a>.</p><div style="display:flex;gap:12px;flex-wrap:wrap"><button type="button" data-eic-choice="necessary">Rifiuta</button><button type="button" data-eic-choice="all">Accetta</button></div>';
    box.addEventListener('click', function (event) {
      var button = event.target.closest('[data-eic-choice]');
      if (!button) return;
      var accepted = button.getAttribute('data-eic-choice') === 'all';
      try { w.localStorage.setItem(config.storageKey, accepted ? 'all' : 'necessary'); }
      catch (_) { sync({ detail: { analytics: false, marketing: false } }); return; }
      sync({ detail: { analytics: accepted, marketing: false } });
      box.remove();
    });
    d.body.appendChild(box);
  }

  function reopen() {
    if (kind === 'gs') { var banner = d.querySelector('.cookie-banner'); if (banner) banner.hidden = false; }
    if (kind === 'ic' && w.icCookieSettings) w.icCookieSettings();
    if (kind === 'ie' && w.IECookieSettings) w.IECookieSettings();
    if (kind === 'rc') fallbackRistoroBanner();
  }

  function addSettingsButton() {
    if (!['gs', 'ic', 'ie', 'rc'].includes(kind) || d.getElementById('eic-analytics-cookie-settings')) return;
    var button = d.createElement('button');
    button.type = 'button';
    button.id = 'eic-analytics-cookie-settings';
    button.textContent = 'Cookie';
    button.setAttribute('aria-label', 'Gestisci preferenze cookie');
    button.style.cssText = 'position:fixed;left:10px;bottom:10px;z-index:9900;border:1px solid #bcc5d0;border-radius:6px;padding:7px 10px;background:#fff;color:#17212e;font:13px/1.3 system-ui;cursor:pointer';
    button.addEventListener('click', reopen);
    d.body.appendChild(button);
    if (kind === 'rc' && !stored()) fallbackRistoroBanner();
  }

  sync();
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', function () { sync(); addSettingsButton(); });
  else addSettingsButton();
})(window, document);
