/* Infissi Media — data dinamica nella topbar (locale it-IT, iniziali maiuscole) */
(function () {
  'use strict';
  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
  function render() {
    try {
      var d = new Date();
      var fmt = new Intl.DateTimeFormat('it-IT', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
      });
      var p = {};
      fmt.formatToParts(d).forEach(function (x) { p[x.type] = x.value; });
      var txt = cap(p.weekday) + ' ' + p.day + ' ' + cap(p.month) + ' ' + p.year;
      var els = document.querySelectorAll('.topbar .date, span.date');
      for (var i = 0; i < els.length; i++) {
        els[i].textContent = txt;
        els[i].setAttribute('datetime', d.getFullYear() + '-' +
          ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2));
      }
    } catch (e) {}
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
