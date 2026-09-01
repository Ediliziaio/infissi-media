/* Infissi Media — comparatore materiali per serramenti.
   I dati provengono dalle rilevazioni pubblicate negli articoli di questo sito
   (prezzi 2026 per materiale e classifiche dei produttori). Valori indicativi. */
(function () {
  'use strict';
  var M = {
    pvc: { nome: 'PVC', uw: [0.62, 0.80], prezzo: [280, 1000],
      forte: 'Miglior rapporto tra isolamento e prezzo', debole: 'Meno adatto a grandi luci e look minimale',
      manutenzione: 'Molto bassa', durata: '30-40 anni', estetica: 'Buona (effetto legno disponibile)' },
    alluminio: { nome: 'Alluminio', uw: [0.80, 0.87], prezzo: [400, 1400],
      forte: 'Profili sottili, grandi vetrate e alzanti scorrevoli', debole: 'Isolamento inferiore a parità di prezzo',
      manutenzione: 'Bassa', durata: '40+ anni', estetica: 'Ottima, design minimale' },
    legno: { nome: 'Legno', uw: [0.75, 0.80], prezzo: [450, 1500],
      forte: 'Estetica calda e materiale rinnovabile', debole: 'Richiede manutenzione periodica delle finiture',
      manutenzione: 'Media (riverniciatura ciclica)', durata: '30-50 anni con manutenzione', estetica: 'Eccellente' },
    'legno-alluminio': { nome: 'Legno-alluminio', uw: [0.62, 0.74], prezzo: [650, 1600],
      forte: 'Legno all’interno, alluminio all’esterno: zero manutenzione fuori', debole: 'Il più costoso',
      manutenzione: 'Molto bassa all’esterno', durata: '40+ anni', estetica: 'Eccellente' }
  };
  function el(id) { return document.getElementById(id); }
  function eur(n) { return n.toLocaleString('it-IT') + ' €/m²'; }

  function consiglia() {
    var pri = el('priorita').value, budget = parseFloat(el('budget').value);
    var out = el('consiglio');
    if (!pri || !isFinite(budget)) { out.innerHTML = '<p class="calc-hint">Scegli una priorità e un budget per vedere il suggerimento.</p>'; return; }

    var lista = Object.keys(M).map(function (k) {
      var m = M[k], punti = 0, motivi = [];
      // compatibilità di budget: il materiale entra se il budget raggiunge almeno la fascia base
      var accessibile = budget >= m.prezzo[0];
      if (accessibile) { punti += 2; motivi.push('rientra nel budget (da ' + eur(m.prezzo[0]) + ')'); }
      else motivi.push('fuori budget: parte da ' + eur(m.prezzo[0]));
      if (pri === 'isolamento') { punti += (1.0 - m.uw[0]) * 10; motivi.push('trasmittanza da ' + m.uw[0].toLocaleString('it-IT') + ' W/m²K'); }
      if (pri === 'prezzo') { punti += (1600 - m.prezzo[0]) / 200; motivi.push('fascia d’ingresso ' + eur(m.prezzo[0])); }
      if (pri === 'manutenzione') { punti += /Molto bassa/.test(m.manutenzione) ? 4 : (/Bassa/.test(m.manutenzione) ? 3 : 1); motivi.push('manutenzione: ' + m.manutenzione.toLowerCase()); }
      if (pri === 'estetica') { punti += /Eccellente/.test(m.estetica) ? 4 : (/Ottima/.test(m.estetica) ? 3 : 2); motivi.push('estetica: ' + m.estetica.toLowerCase()); }
      return { k: k, m: m, punti: accessibile ? punti : punti - 5, motivi: motivi };
    }).sort(function (a, b) { return b.punti - a.punti; });

    var top = lista[0], sec = lista[1];
    out.innerHTML =
      '<div class="cmp-result"><p class="cmp-win">Scelta consigliata: <strong>' + top.m.nome + '</strong></p>' +
      '<p>' + top.m.forte + '. Nel tuo caso: ' + top.motivi.join('; ') + '.</p>' +
      '<p class="calc-note">Da valutare: ' + top.m.debole.toLowerCase() + '. ' +
      'Alternativa: <strong>' + sec.m.nome + '</strong> (' + sec.m.forte.toLowerCase() + ').</p></div>';
  }

  function init() {
    var p = el('priorita'), b = el('budget');
    if (!p || !b) return;
    p.addEventListener('change', consiglia);
    b.addEventListener('input', consiglia);
    consiglia();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
