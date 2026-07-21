#!/usr/bin/env python3
"""Infissi Media — SEO/AEO upgrade su tutti gli articoli:
1. id agli H2 + blocco "Indice dell'articolo" (jump links in SERP)
2. schema speakable (AEO/voice)
3. schema ItemList per gli articoli-classifica (rich results)
4. hreflang it / x-default su tutte le pagine
5. aria-label descrittive sulle cover
6. refresh dateModified (21 luglio 2026) in JSON-LD, meta e byline
7. sitemap: lastmod aggiornato
"""
import re, json, html, os, glob, unicodedata

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'
MOD_ISO = '2026-07-21T17:00:00+02:00'
MOD_HUMAN = '21 Luglio 2026'
NEW_LASTMOD = '2026-07-21'

def slugify(t):
    t = html.unescape(t)
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def add_hreflang(s):
    if 'hreflang="it"' in s:
        return s
    m = re.search(r'(<link rel="canonical" href="([^"]+)">)', s)
    if not m:
        return s
    url = m.group(2)
    ins = (f'{m.group(1)}\n'
           f'<link rel="alternate" hreflang="it" href="{url}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{url}">')
    return s.replace(m.group(1), ins, 1)

def process_article(path):
    s = open(path, encoding='utf-8').read()
    fname = os.path.basename(path)
    report = {'file': fname}

    # --- 1. id answer-box (target speakable/AEO) ---
    if 'id="risposta-rapida"' not in s:
        s = s.replace('<div class="answer-box">', '<div class="answer-box" id="risposta-rapida">', 1)

    # --- 2. cover con aria-label descrittiva ---
    def cover_fix(m):
        block = m.group(0)
        if 'role="img"' in block:
            return block
        tm = re.search(r'<span class="cover-title">(.*?)</span>', block, re.S)
        label = html.unescape(re.sub(r'<[^>]+>', '', tm.group(1))).strip() if tm else 'Copertina articolo'
        label = label.replace('"', '')
        return block.replace('<div class="cover">',
                             f'<div class="cover" role="img" aria-label="{label}">', 1)
    s = re.sub(r'<div class="cover">.*?</div>', cover_fix, s, flags=re.S)

    # --- 3. H2 ids + raccolta voci indice (dentro article-body) ---
    m = re.search(r'(<article class="article-body">)(.*)(</article>)', s, re.S)
    head_a, body, tail_a = m.group(1), m.group(2), m.group(3)

    # zona "Articoli correlati" da escludere
    rel = re.search(r'<nav class="related".*?</nav>', body, re.S)
    rel_span = rel.span() if rel else None

    toc = []
    used = set()
    def h2_fix(mm):
        nonlocal body
        attrs, text = mm.group(1), mm.group(2)
        plain = re.sub(r'<[^>]+>', '', text).strip()
        if plain.lower() in ('in sintesi', 'articoli correlati'):
            return mm.group(0)
        pos = mm.start()
        if rel_span and rel_span[0] <= pos < rel_span[1]:
            return mm.group(0)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(plain)
        base, i = hid, 2
        while hid in used:
            hid = f'{base}-{i}'; i += 1
        used.add(hid)
        toc.append((hid, plain))
        if idm:
            return mm.group(0)
        return f'<h2{attrs} id="{hid}">{text}</h2>'

    body = re.sub(r'<h2([^>]*)>(.*?)</h2>', h2_fix, body, flags=re.S)
    report['toc'] = len(toc)

    # --- 4. inserimento blocco Indice dopo keypoints ---
    if '<nav class="toc"' not in body and toc:
        toc_html = ('\n      <nav class="toc" aria-label="Indice dell\'articolo">\n'
                    '        <p class="toc-title">Indice dell\'articolo</p>\n'
                    '        <ol>\n')
        for hid, label in toc:
            toc_html += f'          <li><a href="#{hid}">{label}</a></li>\n'
        toc_html += '        </ol>\n      </nav>\n'
        kp = body.find('<div class="keypoints">')
        if kp > -1:
            ul_end = body.find('</ul>', kp)
            div_end = body.find('</div>', ul_end)
            body = body[:div_end + 6] + toc_html + body[div_end + 6:]
        else:
            # fallback: prima del primo h2
            h2pos = body.find('<h2')
            body = body[:h2pos] + toc_html + body[h2pos:]

    s = s[:m.start()] + head_a + body + tail_a + s[m.end():]

    # --- 5. JSON-LD: speakable, dateModified, ItemList ---
    rank_names = [re.sub(r'<[^>]+>', '', t).strip()
                  for t in re.findall(r'<div class="rank-item-head">.*?<h3[^>]*>(.*?)</h3>', body, re.S)]
    report['rank_items'] = len(rank_names)

    def jsonld_fix(mm):
        try:
            data = json.loads(mm.group(1))
        except Exception:
            return mm.group(0)
        graph = data.get('@graph', [])
        headline = ''
        for node in graph:
            if node.get('@type') == 'Article':
                headline = node.get('headline', '')
                node['dateModified'] = MOD_ISO
                node['speakable'] = {
                    '@type': 'SpeakableSpecification',
                    'cssSelector': ['.article-hero h1', '#risposta-rapida p']
                }
        if rank_names and not any(n.get('@type') == 'ItemList' for n in graph):
            graph.append({
                '@type': 'ItemList',
                'name': headline,
                'itemListOrder': 'https://schema.org/ItemListOrderAscending',
                'numberOfItems': len(rank_names),
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1, 'name': n}
                    for i, n in enumerate(rank_names)
                ]
            })
        return ('<script type="application/ld+json">\n'
                + json.dumps(data, ensure_ascii=False, indent=2)
                + '\n</script>')

    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', jsonld_fix, s, flags=re.S)

    # --- 6. dateModified in meta e byline ---
    s = re.sub(r'(<meta property="article:modified_time" content=")[^"]+(")',
               r'\g<1>' + MOD_ISO + r'\g<2>', s)
    s = re.sub(r'Aggiornato: <strong>[^<]+</strong>',
               f'Aggiornato: <strong>{MOD_HUMAN}</strong>', s)

    # --- 7. hreflang ---
    s = add_hreflang(s)

    open(path, 'w', encoding='utf-8').write(s)
    return report

def main():
    arts = sorted(glob.glob(ROOT + '/articoli/*.html'))
    print(f'Aggiorno {len(arts)} articoli...')
    for f in arts:
        r = process_article(f)
        print(f"  ok  {r['file']:50s} indice:{r['toc']:2d} voci  classifica:{r['rank_items']:2d}")

    # hreflang anche su home e categorie
    for p in ['index.html', 'top-5-produttori.html', 'top-10.html', 'news.html']:
        fp = os.path.join(ROOT, p)
        s = open(fp, encoding='utf-8').read()
        s2 = add_hreflang(s)
        if s2 != s:
            open(fp, 'w', encoding='utf-8').write(s2)
            print(f'  ok  {p}: hreflang aggiunto')

    # sitemap: lastmod aggiornato
    sm = os.path.join(ROOT, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    s = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{NEW_LASTMOD}</lastmod>', s)
    open(sm, 'w', encoding='utf-8').write(s)
    print('  ok  sitemap.xml: lastmod -> ' + NEW_LASTMOD)

if __name__ == '__main__':
    main()
