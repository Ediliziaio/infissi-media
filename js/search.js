/* Infissi Media — ricerca client-side, zero dipendenze */
(function () {
  'use strict';
  var input = document.getElementById('q');
  var results = document.getElementById('results');
  var count = document.getElementById('count');
  var idx = window.IM_INDEX || [];
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function render(list, q) {
    count.textContent = q
      ? list.length + (list.length === 1 ? ' risultato' : ' risultati') + ' per \u201C' + q + '\u201D'
      : 'Ultimi articoli pubblicati';
    results.innerHTML = list.map(function (it) {
      return '<article class="card search-result"><span class="kicker">' + esc(it.c) + '</span>' +
        '<h3><a href="' + it.u + '">' + esc(it.t) + '</a></h3>' +
        '<p>' + esc(it.d) + '</p><p class="byline">' + esc(it.date || '') + '</p></article>';
    }).join('') || '<p class="no-results">Nessun risultato. Prova con parole chiave diverse, es. \u201Cpvc\u201D, \u201Cbonus\u201D, \u201Cblindate\u201D.</p>';
  }
  function search(q) {
    q = (q || '').trim();
    if (!q) { render(idx.filter(function (i) { return i.c !== 'Sezioni'; }).slice(0, 12), ''); return; }
    var terms = norm(q).split(/\s+/).filter(Boolean);
    var scored = idx.map(function (it) {
      var hay = norm(it.t + ' ' + it.d + ' ' + it.c), s = 0;
      terms.forEach(function (t) {
        if (hay.indexOf(t) > -1) s += (norm(it.t).indexOf(t) > -1 ? 3 : 1);
      });
      return [s, it];
    }).filter(function (x) { return x[0] >= terms.length; })
      .sort(function (a, b) { return b[0] - a[0]; })
      .map(function (x) { return x[1]; });
    render(scored, q);
  }
  input.addEventListener('input', function () { search(input.value); });
  var qp = new URLSearchParams(location.search).get('q') || '';
  input.value = qp;
  search(qp);
})();
