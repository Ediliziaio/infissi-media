#!/usr/bin/env python3
"""Infissi Media — injection finale:
1. Footer: link reali a chi-siamo/privacy/cookie/pubblicita/contatti + voce 'Impostazioni cookie'
2. Tag <script defer> del cookie banner su tutte le pagine
3. Link outbound ai siti ufficiali dei brand citati negli articoli (prima occorrenza, nel body)
4. Sitemap: aggiunge le pagine istituzionali
"""
import re, os, glob

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'

# brand -> sito ufficiale (domini verificati 200/403 il 21/07/2026)
BRANDS = {
    'Internorm': 'https://www.internorm.com/',
    'Finstral': 'https://www.finstral.com/',
    'Oknoplast': 'https://www.oknoplast.it/',
    'Veka': 'https://www.veka.it/',
    'Schüco': 'https://www.schueco.com/',
    'Ponzio': 'https://www.ponzio.it/',
    'Aluprof': 'https://aluprof.com/',
    'Reynaers': 'https://www.reynaers.com/',
    'Metra': 'https://www.metra.com/',
    'Drutex': 'https://www.drutex.pl/',
    'Dierre': 'https://www.dierre.it/',
    'Oikos': 'https://www.oikos.it/',
    'Vighi': 'https://www.vighi.it/',
    'Bauxt': 'https://www.bauxt.com/',
    'Garofoli': 'https://www.garofoli.com/',
    'FerreroLegno': 'https://www.ferrerolegno.it/',
    'Rimadesio': 'https://www.rimadesio.com/',
    'Bertolotto': 'https://www.bertolotto.com/',
    'Bettio': 'https://www.bettio.it/',
    'Pronema': 'https://www.pronema.it/',
    'Kikau': 'https://www.kikau.it/',
    'Griesser': 'https://www.griesser.com/',
    'Warema': 'https://www.warema.com/',
    'Velux': 'https://www.velux.it/',
    'Fakro': 'https://www.fakro.it/',
    'Roto': 'https://www.roto-frank.com/',
    'Gibus': 'https://www.gibus.it/',
    'Corradi': 'https://www.corradi.eu/',
    'Sky-Frame': 'https://www.sky-frame.com/',
    'Vitrocsa': 'https://www.vitrocsa.com/',
    'Secco Sistemi': 'https://www.seccosistemi.com/',
    'Gaulhofer': 'https://www.gaulhofer.com/',
    'Kneer': 'https://www.kneer-suedfenster.de/',
    'Unilux': 'https://www.unilux.de/',
    'Navello': 'https://www.navello.it/',
    'Gardesa': 'https://www.gardesa.it/',
    'Silvelox': 'https://www.silvelox.it/',
    'Barausse': 'https://www.barausse.com/',
    'Eclisse': 'https://www.eclisse.it/',
    'Ermetika': 'https://www.ermetika.com/',
    'Tempotest': 'https://www.tempotest.it/',
    'Gaviota': 'https://www.gaviota.com/',
    'Parà': 'https://www.para.it/',
    'Zanzar': 'https://www.zanzar.it/',
    'NoFlyStore': 'https://www.noflystore.com/',
    'MV Line': 'https://www.mvline.it/',
    'Punto Persiane': 'https://www.puntopersiane.com/',
    'Dakea': 'https://www.dakea.com/',
    'Keylite': 'https://www.keyliteroofwindows.com/',
    'KE Outdoor': 'https://www.keoutdoordesign.com/',
    'Palagina': 'https://www.palagina.it/',
    'Resstende': 'https://www.resstende.it/',
}

def footer_fix(s, p):
    pairs = [
        ('<li><a href="#">Chi siamo</a></li>', f'<li><a href="{p}chi-siamo.html">Chi siamo</a></li>'),
        ('<li><a href="#">Redazione</a></li>', f'<li><a href="{p}chi-siamo.html#redazione">Redazione</a></li>'),
        ('<li><a href="#">Pubblicità</a></li>', f'<li><a href="{p}pubblicita.html">Pubblicità</a></li>'),
        ('<li><a href="#">Privacy Policy</a></li>', f'<li><a href="{p}privacy-policy.html">Privacy Policy</a></li>'),
        ('<li><a href="#">Cookie Policy</a></li>',
         f'<li><a href="{p}cookie-policy.html">Cookie Policy</a></li>\n          <li><a href="#" data-cookie-settings>Impostazioni cookie</a></li>'),
        ('<a href="#">Privacy</a>', f'<a href="{p}privacy-policy.html">Privacy</a>'),
        ('<a href="#">Cookie</a>', f'<a href="{p}cookie-policy.html">Cookie</a>'),
        ('<a href="#">Contatti</a>', f'<a href="{p}contatti.html">Contatti</a>'),
    ]
    for old, new in pairs:
        s = s.replace(old, new)
    return s

def add_banner_script(s, p):
    if 'cookie-consent.js' in s:
        return s
    return s.replace('</body>', f'<script src="{p}js/cookie-consent.js" defer></script>\n</body>', 1)

def link_brands(body):
    """Prima occorrenza di ogni brand nei nodi di testo (fuori da <a>) -> link al sito ufficiale."""
    parts = re.split(r'(<[^>]+>)', body)
    depth = 0
    linked = []
    out = []
    for part in parts:
        if part.startswith('<'):
            low = part.lower()
            if low.startswith('<a ') or low.startswith('<a>'):
                depth += 1
            elif low.startswith('</a'):
                depth = max(0, depth - 1)
            out.append(part)
            continue
        if depth == 0 and part.strip():
            for brand, url in BRANDS.items():
                if brand in linked:
                    continue
                m = re.search(r'(?<![\w&])' + re.escape(brand) + r'(?![\w;])', part)
                if m:
                    anchor = (f'<a href="{url}" target="_blank" rel="noopener" '
                              f'title="Sito ufficiale {brand}">{brand}</a>')
                    part = part[:m.start()] + anchor + part[m.end():]
                    linked.append(brand)
        out.append(part)
    return ''.join(out), linked

# ---------- pagine root (esclusi i redirect) + articoli ----------
root_pages = [f for f in glob.glob(ROOT + '/*.html')
              if not f.endswith(('top-5-produttori.html', 'top-10.html',
                                 'chi-siamo.html', 'contatti.html', 'privacy-policy.html',
                                 'cookie-policy.html', 'pubblicita.html'))]
total_brand_links = 0

for f in sorted(root_pages):
    s = open(f, encoding='utf-8').read()
    s = footer_fix(s, '')
    s = add_banner_script(s, '')
    open(f, 'w', encoding='utf-8').write(s)
print(f'pagine root aggiornate: {len(root_pages)}')

for f in sorted(glob.glob(ROOT + '/articoli/*.html')):
    s = open(f, encoding='utf-8').read()
    s = footer_fix(s, '../')
    s = add_banner_script(s, '../')
    m = re.search(r'(<article class="article-body">)(.*)(</article>)', s, re.S)
    body, linked = link_brands(m.group(2))
    if linked:
        s = s[:m.start()] + m.group(1) + body + m.group(3) + s[m.end():]
        total_brand_links += len(linked)
        print(f'  {os.path.basename(f):50s} brand linkati: {len(linked):2d}  ({", ".join(linked[:6])}{"…" if len(linked) > 6 else ""})')
    open(f, 'w', encoding='utf-8').write(s)

print(f'TOTALE link outbound ai brand: {total_brand_links}')

# ---------- sitemap: pagine istituzionali ----------
sm_path = ROOT + '/sitemap.xml'
sm = open(sm_path, encoding='utf-8').read()
add = ''
for p in ['chi-siamo.html', 'contatti.html', 'pubblicita.html', 'privacy-policy.html', 'cookie-policy.html']:
    if f'/{p}<' not in sm:
        add += f'  <url><loc>https://www.infissimedia.it/{p}</loc><lastmod>2026-07-21</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n'
if add:
    sm = sm.replace('</urlset>', add + '</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)
print('sitemap aggiornata con le pagine istituzionali')
