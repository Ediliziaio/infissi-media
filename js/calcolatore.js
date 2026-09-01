/* Infissi Media — calcolatore detrazione serramenti + trasmittanza per zona climatica.
   Zero dipendenze. I valori Uw sono indicativi: vanno verificati sul decreto vigente. */
(function () {
  'use strict';
  var ZONE = {
    A: { uw: 2.60, citta: 'Lampedusa, Porto Empedocle, Linosa' },
    B: { uw: 2.20, citta: 'Catania, Agrigento, Reggio Calabria, Palermo, Messina' },
    C: { uw: 1.80, citta: 'Roma, Napoli, Bari, Cagliari, Taranto' },
    D: { uw: 1.40, citta: 'Firenze, Genova, Perugia, Ancona, Pescara' },
    E: { uw: 1.00, citta: 'Milano, Torino, Bologna, Venezia, Verona' },
    F: { uw: 1.00, citta: 'Trento, Belluno, Aosta, Cuneo' }
  };
  var MASSIMALE = 60000, ALIQUOTA = 0.5, RATE = 10;

  function eur(n) {
    return n.toLocaleString('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0, useGrouping: true });
  }
  function el(id) { return document.getElementById(id); }

  function calcola() {
    var raw = parseFloat((el('spesa').value || '').toString().replace(/\./g, '').replace(',', '.'));
    var out = el('risultato');
    if (!isFinite(raw) || raw <= 0) {
      out.innerHTML = '<p class="calc-hint">Inserisci l’importo della spesa per vedere il calcolo.</p>';
      return;
    }
    var ammessa = Math.min(raw, MASSIMALE);
    var detrazione = ammessa * ALIQUOTA;
    var rata = detrazione / RATE;
    var eccedenza = raw > MASSIMALE ? raw - MASSIMALE : 0;
    var html =
      '<table class="calc-table"><caption>Esito del calcolo sulla spesa di ' + eur(raw) + '</caption><tbody>' +
      '<tr><th scope="row">Spesa ammessa (massimale ' + eur(MASSIMALE) + ')</th><td>' + eur(ammessa) + '</td></tr>' +
      '<tr><th scope="row">Detrazione totale (50%)</th><td><strong>' + eur(detrazione) + '</strong></td></tr>' +
      '<tr><th scope="row">Rata annua per ' + RATE + ' anni</th><td>' + eur(rata) + '</td></tr>' +
      '<tr><th scope="row">Spesa oltre il massimale (non detraibile)</th><td>' + eur(eccedenza) + '</td></tr>' +
      '</tbody></table>';
    if (eccedenza > 0) {
      html += '<p class="calc-note">La spesa supera il massimale di ' + eur(MASSIMALE) +
        ' per unità immobiliare: l’eccedenza di ' + eur(eccedenza) + ' non genera detrazione.</p>';
    }
    html += '<p class="calc-note">Per fruire della detrazione servono il pagamento con bonifico parlante e ' +
      'la trasmissione della pratica ENEA entro 90 giorni dalla fine dei lavori.</p>';
    out.innerHTML = html;
  }

  function mostraZona() {
    var z = el('zona').value, out = el('zona-out');
    if (!z || !ZONE[z]) { out.innerHTML = ''; return; }
    var d = ZONE[z];
    out.innerHTML =
      '<table class="calc-table"><caption>Zona climatica ' + z + '</caption><tbody>' +
      '<tr><th scope="row">Trasmittanza Uw limite (indicativa)</th><td><strong>' +
      d.uw.toLocaleString('it-IT', { minimumFractionDigits: 2 }) + ' W/m²K</strong></td></tr>' +
      '<tr><th scope="row">Comuni di esempio</th><td>' + d.citta + '</td></tr>' +
      '</tbody></table>' +
      '<p class="calc-note">Valore indicativo da verificare sul decreto requisiti minimi vigente. ' +
      'Conta la trasmittanza della <strong>finestra completa</strong> (telaio + vetro) secondo UNI EN 14351-1, non quella del solo vetro.</p>';
  }

  function init() {
    var s = el('spesa'), z = el('zona');
    if (s) { s.addEventListener('input', calcola); calcola(); }
    if (z) { z.addEventListener('change', mostraZona); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
