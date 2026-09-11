/* eic-lead.js — invio dei contatti del sito al CRM di Edilizia in Cloud.
 *
 * Da includere su TUTTE le pagine (salva UTM / gclid / fbclid all'atterraggio,
 * anche se il form è su un'altra pagina). Poi:
 *
 *   <script src="/eic-lead.js" data-form-id="<id del form>" defer></script>
 *
 * Ogni <form data-eic="contatto|newsletter|pubblicita"> viene inviato al CRM:
 * i campi con name nome, email, telefono, azienda, messaggio passano così come
 * sono; dopo l'invio compare l'elemento [data-eic-ok] dentro il form (o un
 * messaggio al posto del form), in caso di errore [data-eic-errore].
 * In JS: window.EicLead.invia({ email: "...", tipo: "newsletter" }) → Promise.
 */
(function () {
  "use strict";
  var ENDPOINT = "https://rsbrguhkodgnqfomrevo.supabase.co/functions/v1/form-submit";
  var CHIAVI = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "gclid", "wbraid", "gbraid", "fbclid", "ttclid", "msclkid", "li_fat_id"];
  var STORAGE = "eic_parametri_campagna";
  var DURATA_MS = 30 * 24 * 60 * 60 * 1000;
  var script = document.currentScript;
  var FORM_ID = script && script.getAttribute("data-form-id");

  function salva() {
    try {
      var qs = new URLSearchParams(location.search), p = {}, n = 0;
      CHIAVI.forEach(function (k) { var v = qs.get(k); if (v) { p[k] = v.slice(0, 300); n++; } });
      if (n) localStorage.setItem(STORAGE, JSON.stringify({ t: Date.now(), p: p }));
    } catch (e) { /* storage bloccato */ }
  }
  function parametri() {
    try {
      var d = JSON.parse(localStorage.getItem(STORAGE) || "null");
      return d && d.t && Date.now() - d.t < DURATA_MS ? d.p || {} : {};
    } catch (e) { return {}; }
  }
  function invia(data) {
    if (!FORM_ID) return Promise.reject(new Error("data-form-id mancante"));
    var pulito = {};
    Object.keys(data || {}).forEach(function (k) {
      var v = data[k];
      if (v != null && String(v).trim() !== "") pulito[k] = String(v).trim();
    });
    var body = { form_id: FORM_ID, data: pulito, page_url: location.href, referrer: document.referrer || null };
    var p = parametri();
    Object.keys(p).forEach(function (k) { body[k] = p[k]; });
    return fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (!r.ok || j.error) throw new Error(j.error || "Invio non riuscito (" + r.status + ")");
          return j;
        });
      });
  }
  function aggancia(form) {
    if (form.__eic) return;
    form.__eic = true;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.__inviando) return;
      var data = {};
      new FormData(form).forEach(function (v, k) { if (typeof v === "string") data[k] = v; });
      data.tipo = data.tipo || form.getAttribute("data-eic") || "contatto";
      var btn = form.querySelector('[type="submit"], button:not([type])');
      var testo = btn ? btn.textContent : "";
      form.__inviando = true;
      if (btn) { btn.disabled = true; btn.textContent = "Invio…"; }
      var ok = form.querySelector("[data-eic-ok]"), ko = form.querySelector("[data-eic-errore]");
      if (ko) ko.hidden = true;
      invia(data).then(function () {
        form.reset();
        if (ok) { ok.hidden = false; }
        else {
          var m = document.createElement("p");
          m.setAttribute("role", "status");
          m.textContent = data.tipo === "newsletter" ? "Iscrizione ricevuta, grazie!" : "Messaggio ricevuto, grazie! Ti rispondiamo a breve.";
          form.replaceWith(m);
        }
      }).catch(function () {
        if (ko) ko.hidden = false;
        else alert("Invio non riuscito. Riprova tra poco.");
      }).then(function () {
        form.__inviando = false;
        if (btn) { btn.disabled = false; btn.textContent = testo; }
      });
    });
  }
  salva();
  window.EicLead = { invia: invia, parametri: parametri };
  function avvia() { Array.prototype.forEach.call(document.querySelectorAll("form[data-eic]"), aggancia); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", avvia);
  else avvia();
})();
