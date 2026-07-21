#!/usr/bin/env python3
"""Infissi Media — pacchetto "pronto per Google":
1. Google Fonts -> css/fonts.css locale su tutte le pagine
2. Voce "Cerca" nel menu di tutte le pagine
3. Pagina di ricerca cerca.html + js/search-index.js + js/search.js
4. 35 og:image 1200x630 generate con PIL (brand Infissi Media)
5. Meta og:image/twitter:image aggiornati
"""
import re, os, glob, json

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'
BASE = 'https://www.infissimedia.it'

# ---------- mappa categorie articoli ----------
CAT = {}
for f in glob.glob(ROOT + '/articoli/top-5-*.html') + glob.glob(ROOT + '/articoli/top-10-*.html'):
    CAT[os.path.basename(f)[:-5]] = 'Classifiche'
for sl in ['bonus-serramenti-2026-detrazione-50', 'decreto-trasmittanza-termica-2026',
           'direttiva-case-green-serramenti', 'posa-in-opera-qualificata-uni-11673']:
    CAT[sl] = 'Bonus & Normativa'
for sl in ['mercato-serramenti-2026-previsioni-unicmi', 'prezzi-serramenti-2026-andamento',
           'fiere-serramenti-2026-calendario']:
    CAT[sl] = 'Mercato & Fiere'
for sl in ['tendenze-finestre-design-2026', 'finestre-smart-domotica-2026',
           'sostenibilita-riciclo-pvc-serramenti']:
    CAT[sl] = 'News'

FONT_RE = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*\n'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*\n'
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet">\n?')

def local_fonts(s, p):
    return FONT_RE.sub(f'<link rel="stylesheet" href="{p}css/fonts.css">\n', s, count=1)

def add_cerca(s, p, active=False):
    if 'cerca.html' in s:
        return s
    cls = ' class="active" aria-current="page"' if active else ''
    ins = f'    <a href="{p}cerca.html"{cls}>Cerca</a>\n'
    for pat in [f'<a href="{p}index.html#footer-contatti">Contatti</a>',
                '<a href="contatti.html">Contatti</a>']:
        if pat in s:
            return s.replace(pat, ins + pat, 1)
    return s

# ---------- 1-2. font locale + voce Cerca su tutte le pagine ----------
redirects = ('top-5-produttori.html', 'top-10.html')
root_html = [f for f in glob.glob(ROOT + '/*.html') if not f.endswith(redirects)]
for f in root_html:
    s = open(f, encoding='utf-8').read()
    s = local_fonts(s, '')
    s = add_cerca(s, '', active=(os.path.basename(f) == 'cerca.html'))
    open(f, 'w', encoding='utf-8').write(s)
for f in glob.glob(ROOT + '/articoli/*.html'):
    s = open(f, encoding='utf-8').read()
    s = local_fonts(s, '../')
    s = add_cerca(s, '../')
    open(f, 'w', encoding='utf-8').write(s)
print(f'font locale + voce Cerca: {len(root_html) + 30} pagine')

# ---------- 3. indice di ricerca ----------
index = []
for f in sorted(glob.glob(ROOT + '/articoli/*.html')):
    s = open(f, encoding='utf-8').read()
    slug = os.path.basename(f)[:-5]
    t = re.search(r'<meta property="og:title" content="([^"]+)"', s).group(1)
    d = re.search(r'<meta name="description" content="([^"]+)"', s).group(1)
    dm = re.search(r'Pubblicato: <strong>([^<]+)</strong>', s)
    index.append({'t': t, 'u': f'articoli/{slug}.html', 'c': CAT.get(slug, 'News'),
                  'd': d, 'date': dm.group(1) if dm else ''})
for t, u, d in [
    ('Classifiche: Top 5 Produttori e Top 10', 'classifiche.html', 'Tutte le classifiche dei migliori produttori di serramenti e le Top 10 di prodotto.'),
    ('Bonus & Normativa', 'bonus-normativa.html', 'Guide su bonus serramenti 2026, decreto trasmittanza, direttiva Case Green e norme tecniche.'),
    ('Mercato & Fiere', 'mercato-fiere.html', 'Analisi del mercato dei serramenti, andamento prezzi e calendario fiere 2026.'),
    ('News', 'news.html', 'Attualità, tendenze di design, domotica e sostenibilità dal settore serramenti.'),
    ('Chi siamo', 'chi-siamo.html', 'Il metodo editoriale indipendente di Infissi Media e la redazione.'),
    ('Pubblicità', 'pubblicita.html', 'Media kit e spazi pubblicitari disponibili su Infissi Media.'),
]:
    index.append({'t': t, 'u': u, 'c': 'Sezioni', 'd': d, 'date': ''})

open(ROOT + '/js/search-index.js', 'w', encoding='utf-8').write(
    'window.IM_INDEX = ' + json.dumps(index, ensure_ascii=False, indent=1) + ';\n')
print(f'js/search-index.js: {len(index)} voci')

# ---------- 3b. search.js ----------
open(ROOT + '/js/search.js', 'w', encoding='utf-8').write('''/* Infissi Media — ricerca client-side, zero dipendenze */
(function () {
  'use strict';
  var input = document.getElementById('q');
  var results = document.getElementById('results');
  var count = document.getElementById('count');
  var idx = window.IM_INDEX || [];
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function render(list, q) {
    count.textContent = q
      ? list.length + (list.length === 1 ? ' risultato' : ' risultati') + ' per \\u201C' + q + '\\u201D'
      : 'Ultimi articoli pubblicati';
    results.innerHTML = list.map(function (it) {
      return '<article class="card search-result"><span class="kicker">' + esc(it.c) + '</span>' +
        '<h3><a href="' + it.u + '">' + esc(it.t) + '</a></h3>' +
        '<p>' + esc(it.d) + '</p><p class="byline">' + esc(it.date || '') + '</p></article>';
    }).join('') || '<p class="no-results">Nessun risultato. Prova con parole chiave diverse, es. \\u201Cpvc\\u201D, \\u201Cbonus\\u201D, \\u201Cblindate\\u201D.</p>';
  }
  function search(q) {
    q = (q || '').trim();
    if (!q) { render(idx.filter(function (i) { return i.c !== 'Sezioni'; }).slice(0, 12), ''); return; }
    var terms = norm(q).split(/\\s+/).filter(Boolean);
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
''')
print('js/search.js scritto')

# ---------- 3c. cerca.html ----------
NAV = '''<nav class="mainnav" aria-label="Navigazione principale">
  <div class="container">
    <a href="index.html">Home</a>
    <a href="news.html">News</a>
    <a href="bonus-normativa.html">Bonus &amp; Normativa</a>
    <a href="classifiche.html">Classifiche</a>
    <a href="mercato-fiere.html">Mercato &amp; Fiere</a>
    <a href="cerca.html" class="active" aria-current="page">Cerca</a>
    <a href="contatti.html">Contatti</a>
  </div>
</nav>'''
FOOTER = open(ROOT + '/chi-siamo.html', encoding='utf-8').read()
FOOTER = FOOTER[FOOTER.index('<footer>'):FOOTER.index('</footer>') + len('</footer>')]

cerca = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="css/fonts.css">
<title>Cerca nel sito — Infissi Media</title>
<meta name="description" content="Cerca tra tutti gli articoli, le classifiche e le guide di Infissi Media: serramenti, finestre, bonus, normativa e mercato.">
<link rel="canonical" href="{BASE}/cerca.html">
<meta name="robots" content="noindex, follow">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="topbar">
  <div class="container">
    <span class="tagline">Il magazine dei serramenti e dell'edilizia</span>
    <span class="date">Martedì 21 Luglio 2026</span>
  </div>
</div>

<header class="masthead">
  <div class="container">
    <a href="index.html" title="Infissi Media — Home">
      <img src="assets/logo.png" alt="Infissi Media — magazine su serramenti, infissi ed edilizia" width="1886" height="379">
    </a>
  </div>
</header>

{NAV}

<main class="container">
  <nav class="breadcrumb" aria-label="Percorso di navigazione">
    <a href="index.html">Home</a><span>›</span>Cerca
  </nav>

  <header class="cat-head">
    <h1>Cerca nel sito</h1>
    <p>Trova articoli, classifiche e guide tra tutti i contenuti di Infissi Media.</p>
  </header>

  <div class="search-box">
    <label for="q" style="position:absolute;left:-9999px">Cerca nel sito</label>
    <input type="search" id="q" placeholder="Cerca: pvc, bonus 2026, porte blindate, antieffrazione…" autocomplete="off" autofocus>
  </div>

  <p id="count" class="search-count"></p>
  <div id="results" class="grid-3 search-results"></div>
</main>

{FOOTER}

<div class="ad-slot ad-mobile-sticky" data-format="320×50 · mobile anchor" id="ad-mobile-sticky"></div>
<script src="js/cookie-consent.js" defer></script>
<script src="js/search-index.js" defer></script>
<script src="js/search.js" defer></script>

</body>
</html>
'''
open(ROOT + '/cerca.html', 'w', encoding='utf-8').write(cerca)
print('cerca.html scritta')

# ---------- 3d. CSS ricerca ----------
css_path = ROOT + '/css/style.css'
css = open(css_path, encoding='utf-8').read()
if '.search-box' not in css:
    css += '''
/* ---------- RICERCA ---------- */
.search-box{margin:26px 0 8px}
.search-box input{
  width:100%;max-width:720px;padding:16px 20px;font-size:17px;font-family:var(--sans);
  border:2px solid var(--ink);border-radius:10px;outline:none;
}
.search-box input:focus{border-color:var(--accent);box-shadow:0 0 0 4px var(--accent-soft)}
.search-count{font-size:13px;color:var(--mute);text-transform:uppercase;letter-spacing:.08em;margin:14px 0 20px}
.search-results{padding-bottom:30px}
.search-result h3{font-size:19px}
.no-results{font-size:17px;color:var(--ink-soft);padding:30px 0}
'''
    open(css_path, 'w', encoding='utf-8').write(css)
    print('CSS ricerca aggiunto')

# ---------- 4. og:image con PIL ----------
from PIL import Image, ImageDraw, ImageFont

SG = ROOT + '/scripts/ttf/SpaceGrotesk-var.ttf'
INTER = ROOT + '/scripts/ttf/Inter-var.ttf'
os.makedirs(ROOT + '/assets/og', exist_ok=True)

def fnt(path, size, wght):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([wght])
    return f

W, H = 1200, 630

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def og_image(out, title, cat):
    img = Image.new('RGB', (W, H), '#101418')
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([760, -180, 1400, 460], fill=(88, 184, 230, 38))
    od.ellipse([900, 240, 1500, 840], fill=(29, 127, 169, 50))
    img = Image.alpha_composite(img.convert('RGBA'), ov)
    d = ImageDraw.Draw(img)
    # wordmark
    f_wm = fnt(SG, 44, 700)
    x, y = 64, 52
    d.text((x, y), 'Infissi', font=f_wm, fill='#ffffff')
    w1 = d.textlength('Infissi', font=f_wm)
    d.text((x + w1 + 4, y), 'Media', font=f_wm, fill='#58b8e6')
    # chip categoria
    f_chip = fnt(INTER, 24, 600)
    ct = cat.upper()
    tw = d.textlength(ct, font=f_chip)
    cy = 140
    d.rounded_rectangle([64, cy, 64 + tw + 36, cy + 46], radius=8, fill='#58b8e6')
    d.text((64 + 18, cy + 9), ct, font=f_chip, fill='#101418')
    # titolo
    size = 64
    while size > 40:
        f_t = fnt(SG, size, 700)
        lines = wrap(d, title, f_t, 1020)
        if len(lines) <= 5:
            break
        size -= 6
    ty = cy + 46 + 38
    for ln in lines[:5]:
        d.text((64, ty), ln, font=f_t, fill='#ffffff')
        ty += int(size * 1.16)
    # footer brand
    d.rectangle([64, 548, 204, 556], fill='#58b8e6')
    f_b = fnt(INTER, 24, 600)
    d.text((64, 572), 'INFISSIMEDIA.IT · SERRAMENTI & EDILIZIA', font=f_b, fill='#9aa7b0')
    img.convert('RGB').save(out, 'PNG', optimize=True)

# articoli
og_map = {}  # file html relativo -> slug immagine
for f in sorted(glob.glob(ROOT + '/articoli/*.html')):
    s = open(f, encoding='utf-8').read()
    slug = os.path.basename(f)[:-5]
    title = re.search(r'<meta property="og:title" content="([^"]+)"', s).group(1)
    og_image(ROOT + f'/assets/og/{slug}.png', title, CAT.get(slug, 'News'))
    og_map['articoli/' + slug + '.html'] = slug
# pagine principali
PAGES_OG = [
    ('index.html', 'home', 'News, classifiche e guide su serramenti, finestre ed edilizia', 'Magazine'),
    ('news.html', 'news', 'Attualità, design e innovazione dal mondo dei serramenti', 'News'),
    ('classifiche.html', 'classifiche', 'Le classifiche dei migliori produttori e le Top 10', 'Classifiche'),
    ('bonus-normativa.html', 'bonus-normativa', 'Bonus serramenti 2026, decreti e guide tecniche', 'Bonus & Normativa'),
    ('mercato-fiere.html', 'mercato-fiere', 'Analisi di mercato, prezzi e fiere del settore 2026', 'Mercato & Fiere'),
]
for fname, slug, title, cat in PAGES_OG:
    og_image(ROOT + f'/assets/og/{slug}.png', title, cat)
    og_map[fname] = slug
print(f'og:image generate: {len(og_map)}')

# ---------- 5. meta og:image ----------
for rel, slug in og_map.items():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding='utf-8').read()
    new_img = f'{BASE}/assets/og/{slug}.png'
    s = s.replace(f'<meta property="og:image" content="{BASE}/assets/logo.png">',
                  f'<meta property="og:image" content="{new_img}">\n'
                  f'<meta property="og:image:width" content="1200">\n'
                  f'<meta property="og:image:height" content="630">', 1)
    s = s.replace(f'<meta name="twitter:image" content="{BASE}/assets/logo.png">',
                  f'<meta name="twitter:image" content="{new_img}">', 1)
    open(f, 'w', encoding='utf-8').write(s)
print('meta og:image aggiornati su', len(og_map), 'pagine')
print('FATTO ✓')
