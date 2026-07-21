#!/usr/bin/env python3
"""Infissi Media — ristrutturazione v2:
- Menu editoriale da blog su tutte le pagine (niente Top 5/Top 10 in nav)
- Nuove pagine categoria: classifiche.html, bonus-normativa.html, mercato-fiere.html, news.html
- Breadcrumb/JSON-LD/footer degli articoli allineati alle nuove categorie
- Font moderni (Space Grotesk + Inter)
- Redirect dalle vecchie pagine categoria, sitemap e llms.txt aggiornati
"""
import re, json, os, glob

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'
BASE = 'https://www.infissimedia.it'

OLD_FONT = 'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,800;1,500&family=Lora:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;600;700&display=swap'
NEW_FONT = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap'
FONT_LINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              f'<link href="{NEW_FONT}" rel="stylesheet">')

NAV_ITEMS = [
    ('Home', 'index.html', 'home'),
    ('News', 'news.html', 'news'),
    ('Bonus &amp; Normativa', 'bonus-normativa.html', 'bonus'),
    ('Classifiche', 'classifiche.html', 'classifiche'),
    ('Mercato &amp; Fiere', 'mercato-fiere.html', 'mercato'),
    ('Contatti', 'index.html#footer-contatti', ''),
]

def nav_html(prefix, active):
    links = []
    for label, href, key in NAV_ITEMS:
        cls = ' class="active" aria-current="page"' if key == active else ''
        links.append(f'    <a href="{prefix}{href}"{cls}>{label}</a>')
    return ('<nav class="mainnav" aria-label="Navigazione principale">\n'
            '  <div class="container">\n' + '\n'.join(links) + '\n  </div>\n</nav>')

# slug articolo -> (chiave categoria, nome categoria, pagina categoria)
CAT = {}
for sl in glob.glob(ROOT + '/articoli/top-5-*.html') + glob.glob(ROOT + '/articoli/top-10-*.html'):
    CAT[os.path.basename(sl)[:-5]] = ('classifiche', 'Classifiche', 'classifiche.html')
for sl in ['bonus-serramenti-2026-detrazione-50', 'decreto-trasmittanza-termica-2026',
           'direttiva-case-green-serramenti', 'posa-in-opera-qualificata-uni-11673']:
    CAT[sl] = ('bonus', 'Bonus & Normativa', 'bonus-normativa.html')
for sl in ['mercato-serramenti-2026-previsioni-unicmi', 'prezzi-serramenti-2026-andamento',
           'fiere-serramenti-2026-calendario']:
    CAT[sl] = ('mercato', 'Mercato & Fiere', 'mercato-fiere.html')
for sl in ['tendenze-finestre-design-2026', 'finestre-smart-domotica-2026',
           'sostenibilita-riciclo-pvc-serramenti']:
    CAT[sl] = ('news', 'News', 'news.html')

def fix_jsonld(s, catname, catpage):
    def fix(m):
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        for node in data.get('@graph', []):
            t = node.get('@type')
            if t == 'BreadcrumbList':
                for el in node.get('itemListElement', []):
                    if el.get('position') == 2:
                        el['name'] = catname
                        el['item'] = f'{BASE}/{catpage}'
            elif t == 'Article':
                node['articleSection'] = catname
        return ('<script type="application/ld+json">\n'
                + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>')
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)

# ---------------- ARTICOLI ----------------
for f in sorted(glob.glob(ROOT + '/articoli/*.html')):
    slug = os.path.basename(f)[:-5]
    catkey, catname, catpage = CAT[slug]
    s = open(f, encoding='utf-8').read()

    s = s.replace(OLD_FONT, NEW_FONT)
    s = re.sub(r'<nav class="mainnav".*?</nav>', nav_html('../', catkey), s, count=1, flags=re.S)

    # breadcrumb visibile: seconda voce -> nuova categoria
    m = re.search(r'(<nav class="breadcrumb".*?</nav>)', s, re.S)
    if m:
        block = re.sub(r'<a href="\.\./(?!index\.html)[a-z0-9\-]+\.html">[^<]*</a>',
                       f'<a href="../{catpage}">{catname}</a>', m.group(1), count=1)
        s = s.replace(m.group(1), block)

    s = fix_jsonld(s, catname, catpage)
    s = re.sub(r'(<meta property="article:section" content=")[^"]*(")',
               lambda mm: mm.group(1) + catname + mm.group(2), s)

    # footer: link alle nuove categorie
    s = s.replace('href="../top-5-produttori.html">Top 5 Produttori<',
                  'href="../classifiche.html">Classifiche<')
    s = s.replace('href="../top-10.html">Top 10 · Classifiche<',
                  'href="../classifiche.html#top-10">Le Top 10<')
    s = s.replace('href="../news.html#bonus">Bonus &amp; Normativa<',
                  'href="../bonus-normativa.html">Bonus &amp; Normativa<')

    open(f, 'w', encoding='utf-8').write(s)
print('articoli aggiornati: 30')

# ---------------- HOME ----------------
f = ROOT + '/index.html'
s = open(f, encoding='utf-8').read()
s = s.replace(OLD_FONT, NEW_FONT)
s = re.sub(r'<nav class="mainnav".*?</nav>', nav_html('', 'home'), s, count=1, flags=re.S)
s = s.replace('<h2 id="sec-top5">Top 5 Produttori</h2>',
              '<h2 id="sec-top5">Classifiche · I migliori produttori</h2>')
s = s.replace('href="top-5-produttori.html">Tutte le classifiche →',
              'href="classifiche.html">Tutte le classifiche →')
s = s.replace('<h2 id="sec-top10">Top 10 · Le Classifiche</h2>',
              '<h2 id="sec-top10">Le Top 10</h2>')
s = s.replace('href="top-10.html">Tutte le Top 10 →',
              'href="classifiche.html#top-10">Tutte le Top 10 →')
s = s.replace('href="top-5-produttori.html">Top 5 Produttori<',
              'href="classifiche.html">Classifiche<')
s = s.replace('href="top-10.html">Top 10 · Classifiche<',
              'href="classifiche.html#top-10">Le Top 10<')
s = s.replace('href="news.html#bonus">Bonus &amp; Normativa<',
              'href="bonus-normativa.html">Bonus &amp; Normativa<')
s = s.replace('href="news.html#mercato">Mercato &amp; Fiere<',
              'href="mercato-fiere.html">Mercato &amp; Fiere<')
s = s.replace('<span class="kicker">Top 5 Produttori</span>', '<span class="kicker">Classifiche</span>')
open(f, 'w', encoding='utf-8').write(s)
print('home aggiornata')

# ---------------- GENERATORE PAGINE CATEGORIA ----------------
def footer_html():
    return f'''<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <img src="assets/logo.png" alt="Infissi Media" width="1886" height="379" loading="lazy">
        <p>Infissi Media è il magazine editoriale dedicato a serramenti, infissi, porte, finestre ed edilizia. Classifiche indipendenti, news di settore e guide ai bonus.</p>
      </div>
      <nav aria-label="Categorie">
        <h5>Categorie</h5>
        <ul>
          <li><a href="news.html">News</a></li>
          <li><a href="bonus-normativa.html">Bonus &amp; Normativa</a></li>
          <li><a href="classifiche.html">Classifiche</a></li>
          <li><a href="mercato-fiere.html">Mercato &amp; Fiere</a></li>
        </ul>
      </nav>
      <nav aria-label="Guide popolari">
        <h5>Guide popolari</h5>
        <ul>
          <li><a href="articoli/bonus-serramenti-2026-detrazione-50.html">Bonus serramenti 2026</a></li>
          <li><a href="articoli/top-10-marchi-serramenti-2026.html">Migliori marchi serramenti</a></li>
          <li><a href="articoli/top-5-produttori-finestre-pvc.html">Migliori finestre PVC</a></li>
          <li><a href="articoli/posa-in-opera-qualificata-uni-11673.html">Posa in opera qualificata</a></li>
        </ul>
      </nav>
      <nav aria-label="Informazioni">
        <h5>Infissi Media</h5>
        <ul>
          <li><a href="#">Chi siamo</a></li>
          <li><a href="#">Pubblicità</a></li>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="sitemap.xml">Mappa del sito</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Infissi Media — Tutti i diritti riservati.</span>
      <span><a href="#">Privacy</a> · <a href="#">Cookie</a> · <a href="#">Contatti</a></span>
    </div>
  </div>
</footer>'''

def card_html(c):
    url, covercat, badge, kicker, title, teaser, date = c
    badge_html = f'<span class="rank-badge">{badge}</span>' if badge else ''
    return f'''      <article class="card">
        <a href="articoli/{url}.html"><div class="cover tall"><span class="cover-cat">{covercat}</span>{badge_html}</div></a>
        <span class="kicker">{kicker}</span>
        <h3><a href="articoli/{url}.html">{title}</a></h3>
        <p>{teaser}</p>
        <p class="byline">{date}</p>
      </article>'''

def cat_page(filename, doc_title, meta_desc, h1, intro, sections, active, adid):
    secs = ''
    for sid, heading, cards in sections:
        idattr = f' id="{sid}"' if sid else ''
        secs += f'''  <section class="section"{idattr} aria-labelledby="h-{sid}">
    <div class="section-head"><h2 id="h-{sid}">{heading}</h2></div>
    <div class="grid-3">
{chr(10).join(card_html(c) for c in cards)}
    </div>
  </section>
'''
    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{FONT_LINKS}
<title>{doc_title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{BASE}/{filename}">
<link rel="alternate" hreflang="it" href="{BASE}/{filename}">
<link rel="alternate" hreflang="x-default" href="{BASE}/{filename}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Infissi Media">
<meta property="og:title" content="{doc_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{BASE}/{filename}">
<meta property="og:image" content="{BASE}/assets/logo.png">
<meta property="og:locale" content="it_IT">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "@id": "{BASE}/{filename}",
      "url": "{BASE}/{filename}",
      "name": "{doc_title}",
      "description": "{meta_desc}",
      "inLanguage": "it-IT",
      "isPartOf": {{ "@id": "{BASE}/#website" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{h1}", "item": "{BASE}/{filename}" }}
      ]
    }}
  ]
}}
</script>
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

{nav_html('', active)}

<main class="container">
  <nav class="breadcrumb" aria-label="Percorso di navigazione">
    <a href="index.html">Home</a><span>›</span>{h1}
  </nav>

  <header class="cat-head">
    <h1>{h1}</h1>
    <p>{intro}</p>
  </header>

  <!-- AD SLOT: Leaderboard 970x250 -->
  <div class="ad-slot ad-leaderboard" data-format="970×250 · leaderboard" id="ad-{adid}"></div>

{secs}
  <!-- AD SLOT: Leaderboard bottom -->
  <div class="ad-slot ad-leaderboard" data-format="970×250 · leaderboard bottom" id="ad-{adid}-bottom"></div>
</main>

{footer_html()}

<div class="ad-slot ad-mobile-sticky" data-format="320×50 · mobile anchor" id="ad-mobile-sticky"></div>

</body>
</html>
'''
    open(ROOT + '/' + filename, 'w', encoding='utf-8').write(html)
    print('pagina creata:', filename)

# --- dati card ---
TOP5 = [
    ('top-5-produttori-finestre-pvc', 'PVC', 'TOP 5', 'Finestre in PVC', 'Top 5 produttori di finestre in PVC: la classifica 2026 con prezzi e schede tecniche', 'Internorm, Finstral, Oknoplast, Veka e Schüco a confronto: trasmittanza, profili, vetri e garanzie.', '20 Luglio 2026'),
    ('top-5-produttori-serramenti-alluminio', 'Alluminio', 'TOP 5', 'Serramenti in alluminio', 'Top 5 produttori di serramenti in alluminio 2026', 'I sistemi a taglio termico che dominano il mercato italiano, dal profilo minimale alla grande vetrata.', '19 Luglio 2026'),
    ('top-5-produttori-finestre-legno', 'Legno', 'TOP 5', 'Finestre in legno', 'Top 5 produttori di finestre in legno 2026', 'Calore, estetica e sostenibilità: le migliori finestre in legno lamellare sul mercato.', '18 Luglio 2026'),
    ('top-5-produttori-finestre-legno-alluminio', 'Legno-Alluminio', 'TOP 5', 'Finestre legno-alluminio', 'Top 5 finestre legno-alluminio: i migliori produttori 2026', "Eleganza del legno dentro, resistenza dell'alluminio fuori: il meglio dei due mondi.", '17 Luglio 2026'),
    ('top-5-produttori-serramenti-made-in-italy', 'Made in Italy', 'TOP 5', 'Made in Italy', 'Top 5 produttori di serramenti Made in Italy 2026', "L'eccellenza italiana dei serramenti tra qualità artigianale e innovazione industriale.", '16 Luglio 2026'),
    ('top-5-produttori-porte-interne', 'Porte interne', 'TOP 5', 'Porte interne', 'Top 5 produttori di porte interne 2026', 'Battenti, scorrevoli e filo muro: i brand che uniscono design e durata.', '15 Luglio 2026'),
    ('top-5-produttori-porte-blindate', 'Sicurezza', 'TOP 5', 'Porte blindate', 'Top 5 produttori di porte blindate 2026', "Classe 3 e 4 antieffrazione, cilindri europei e design: le porte d'ingresso più sicure.", '14 Luglio 2026'),
    ('top-5-produttori-persiane-scuri-alluminio', 'Oscuranti', 'TOP 5', 'Persiane e scuri', 'Top 5 produttori di persiane e scuri in alluminio 2026', 'Orientabili, blindate e certificate antieffrazione: gli oscuranti che proteggono casa.', '13 Luglio 2026'),
    ('top-5-produttori-zanzariere', 'Zanzariere', 'TOP 5', 'Zanzariere', 'Top 5 produttori di zanzariere 2026', 'Plissettate, a rullo, magnetiche e motorizzate: la protezione anti-insetti su misura.', '12 Luglio 2026'),
    ('top-5-produttori-tapparelle-frangisole', 'Schermature', 'TOP 5', 'Tapparelle e frangisole', 'Top 5 produttori di tapparelle e frangisole 2026', 'Avvolgibili in alluminio coibentato e lamelle orientabili per il controllo di luce e calore.', '11 Luglio 2026'),
]
TOP10 = [
    ('top-10-marchi-serramenti-2026', "Classifica dell'anno", 'TOP 10', 'Marchi', 'I 10 migliori marchi di serramenti del 2026: la classifica definitiva', 'Qualità, innovazione, assistenza e prezzo: il podio dei brand che contano davvero.', '19 Luglio 2026'),
    ('top-10-finestre-risparmio-energetico', 'Efficienza', 'TOP 10', 'Risparmio energetico', 'Top 10 finestre per il risparmio energetico: trasmittanze a confronto', 'Le finestre con il valore Uw più basso sul mercato: fino al 40% di bolletta in meno.', '18 Luglio 2026'),
    ('top-10-finestre-antieffrazione', 'Sicurezza', 'TOP 10', 'Antieffrazione', 'Top 10 finestre antieffrazione: classe RC2 e RC3 a confronto', 'Vetri stratificati, ferramenta antiscasso e certificazioni UNI ENV 1627.', '17 Luglio 2026'),
    ('top-10-finestre-isolamento-acustico', 'Acustica', 'TOP 10', 'Isolamento acustico', "Top 10 finestre per l'isolamento acustico: silenzio fino a 48 dB", 'Per chi vive vicino a strade, ferrovie e aeroporti: il silenzio è un valore misurabile.', '16 Luglio 2026'),
    ('top-10-porte-blindate', 'Sicurezza', 'TOP 10', 'Porte blindate', 'Top 10 porte blindate 2026: sicurezza, design e prezzi', "Dieci porte d'ingresso certificate a confronto, dalla classe 3 alla classe 4.", '15 Luglio 2026'),
    ('top-10-zanzariere', 'Zanzariere', 'TOP 10', 'Zanzariere', 'Top 10 zanzariere 2026: plissettate, a rullo e magnetiche', 'Dal modello base alla zanzariera motorizzata: quale scegliere per ogni ambiente.', '14 Luglio 2026'),
    ('top-10-tende-da-sole', 'Outdoor', 'TOP 10', 'Tende da sole', 'Top 10 tende da sole 2026: bracci, cappottine e a caduta', 'Protezione solare per balconi, terrazzi e giardini: tessuti, motori e sensori vento.', '13 Luglio 2026'),
    ('top-10-porte-interne-design', 'Interior', 'TOP 10', 'Porte interne', 'Top 10 porte interne di design 2026: filo muro, scorrevoli e battenti', 'Quando la porta diventa arredo: le soluzioni più belle per gli interni contemporanei.', '12 Luglio 2026'),
    ('top-10-scorrevoli-vetro', 'Vetro', 'TOP 10', 'Scorrevoli in vetro', 'Top 10 scorrevoli in vetro 2026: alzanti e traslanti per grandi luci', 'Pareti vetrate che scompaiono: i sistemi scorrevoli per la casa moderna.', '11 Luglio 2026'),
    ('top-10-lucernari-finestre-tetto', 'Mansarde', 'TOP 10', 'Lucernari', 'Top 10 lucernari e finestre per tetti 2026: guida e prezzi', 'Luce naturale in mansarda: bilici, a compasso e motorizzati a confronto.', '10 Luglio 2026'),
]
BONUS = [
    ('bonus-serramenti-2026-detrazione-50', 'Bonus', None, 'Guida', 'Bonus serramenti 2026: detrazione del 50%, requisiti e guida completa', 'Massimali, trasmittanze limite, bonifico parlante e pratica ENEA: tutto per non perdere la detrazione.', '21 Luglio 2026'),
    ('decreto-trasmittanza-termica-2026', 'Normativa', None, 'Normativa', 'Decreto trasmittanza termica 2026: le nuove regole per infissi e facciate', "Cosa cambia per i valori limite di trasmittanza e per l'accesso alle detrazioni fiscali.", '20 Luglio 2026'),
    ('direttiva-case-green-serramenti', 'Europa', None, 'Direttiva UE', 'Direttiva Case Green: cosa cambia per infissi e serramenti', "La direttiva europea sull'efficienza energetica degli edifici spiegata in parole semplici.", '18 Luglio 2026'),
    ('posa-in-opera-qualificata-uni-11673', 'Tecnica', None, 'Tecnica', 'Posa in opera qualificata UNI 11673: la guida completa', 'Perché il giunto tra telaio e muratura vale più del serramento stesso.', '16 Luglio 2026'),
]
MERCATO = [
    ('mercato-serramenti-2026-previsioni-unicmi', 'Mercato', None, 'Analisi', 'Mercato serramenti 2026: le previsioni UNICMI e le tendenze del comparto', 'Tra recupero edilizio e riqualificazione energetica: dove va il mercato italiano dei serramenti.', '19 Luglio 2026'),
    ('prezzi-serramenti-2026-andamento', 'Listini', None, 'Prezzi', "Prezzi serramenti 2026: l'andamento dei listini di PVC, alluminio e legno", 'Materie prime, energia e domanda: l\'analisi dei prezzi per chi deve comprare.', '12 Luglio 2026'),
]
FIERE = [
    ('fiere-serramenti-2026-calendario', 'Fiere', None, 'Eventi', 'Fiere del serramento 2026: il calendario completo degli eventi del settore', 'MADE Expo, SAIE, Klimahouse, Fensterbau: dove e quando incontrare i produttori.', '13 Luglio 2026'),
]
ATTUALITA = [
    ('tendenze-finestre-design-2026', 'Design', None, 'Tendenze', 'Tendenze finestre 2026: profili minimali, colori scuri e grandi vetrate', "Dal nero opaco al legno naturale: come cambia l'estetica del serramento.", '17 Luglio 2026'),
    ('finestre-smart-domotica-2026', 'Smart Home', None, 'Domotica', 'Finestre smart e domotica 2026: sensori, motori e vetri elettrocromici', 'Il serramento diventa intelligente: cosa è già realtà e cosa arriverà.', '15 Luglio 2026'),
    ('sostenibilita-riciclo-pvc-serramenti', 'Sostenibilità', None, 'Economia circolare', 'Serramenti sostenibili: riciclo del PVC ed economia circolare', 'Cosa succede alle vecchie finestre e perché il PVC riciclato è una risorsa, non un rifiuto.', '14 Luglio 2026'),
]
ULTIME = [
    BONUS[0], BONUS[1],
    ('mercato-serramenti-2026-previsioni-unicmi', 'Mercato', None, 'Analisi', 'Mercato serramenti 2026: le previsioni UNICMI e le tendenze del comparto', 'Tra recupero edilizio e riqualificazione energetica: dove va il mercato italiano.', '19 Luglio 2026'),
    TOP10[0], TOP5[0], BONUS[2],
]

cat_page('classifiche.html',
         'Classifiche Serramenti e Infissi 2026: Top 5 Produttori e Top 10',
         'Tutte le classifiche di Infissi Media: i migliori produttori di finestre, porte e oscuranti e le Top 10 su marchi, antieffrazione, acustica e risparmio energetico. Analisi indipendenti con dati tecnici.',
         'Classifiche',
         'Il cuore del magazine: classifiche indipendenti costruite su schede tecniche, certificazioni, trasmittanze, classi antieffrazione e prezzi rilevati sul mercato italiano. Nessuna posizione è sponsorizzata.',
         [('produttori', 'Le classifiche dei produttori', TOP5),
          ('top-10', 'Le Top 10', TOP10)],
         'classifiche', 'cat-classifiche')

cat_page('bonus-normativa.html',
         'Bonus Serramenti e Normativa 2026: Guide, Requisiti e Detrazioni',
         'Bonus serramenti 2026, decreto trasmittanza termica, direttiva Case Green e norma UNI 11673: le guide complete di Infissi Media su detrazioni e regole tecniche per infissi e serramenti.',
         'Bonus &amp; Normativa',
         'Detrazioni fiscali, decreti, direttive europee e norme tecniche: la redazione traduce la burocrazia in guide operative, con requisiti, scadenze e errori da evitare.',
         [('guide', 'Guide, bonus e regole tecniche', BONUS)],
         'bonus', 'cat-bonus')

cat_page('mercato-fiere.html',
         'Mercato Serramenti e Fiere 2026: Analisi, Prezzi ed Eventi',
         'Andamento del mercato dei serramenti, prezzi di PVC alluminio e legno, calendario delle fiere 2026: analisi e appuntamenti del settore infissi ed edilizia.',
         'Mercato &amp; Fiere',
         'Numeri, tendenze e appuntamenti del comparto: analisi del mercato italiano dei serramenti, andamento dei listini e il calendario completo delle fiere dove incontrare i produttori.',
         [('mercato', 'Mercato e prezzi', MERCATO),
          ('fiere', 'Fiere &amp; Eventi', FIERE)],
         'mercato', 'cat-mercato')

cat_page('news.html',
         'News Serramenti ed Edilizia: Attualità, Design e Innovazione 2026',
         'Le ultime news dal mondo dei serramenti e dell\'edilizia: tendenze di design, finestre smart e domotica, sostenibilità e tutti gli ultimi articoli del magazine.',
         'News',
         'Attualità, tendenze e innovazione dal mondo dei serramenti e dell\'edilizia: design, domotica, sostenibilità e tutto quello che cambia nel settore, spiegato in parole chiare.',
         [('attualita', 'Attualità e innovazione', ATTUALITA),
          ('ultime', 'Ultimi articoli dal magazine', ULTIME)],
         'news', 'cat-news')

# ---------------- REDIRECT VECCHIE PAGINE ----------------
def redirect_page(filename, target, title):
    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Infissi Media</title>
<link rel="canonical" href="{BASE}/{target}">
<meta http-equiv="refresh" content="0; url={target}">
<meta name="robots" content="noindex, follow">
</head>
<body>
<p>Questa pagina si è spostata: <a href="{target}">{title} — Infissi Media</a>.</p>
</body>
</html>
'''
    open(ROOT + '/' + filename, 'w', encoding='utf-8').write(html)
    print('redirect:', filename, '->', target)

redirect_page('top-5-produttori.html', 'classifiche.html', 'Classifiche')
redirect_page('top-10.html', 'classifiche.html#top-10', 'Classifiche')

# ---------------- SITEMAP ----------------
ART = [
    ('bonus-serramenti-2026-detrazione-50', '2026-07-21', '0.9'),
    ('decreto-trasmittanza-termica-2026', '2026-07-20', '0.8'),
    ('top-5-produttori-finestre-pvc', '2026-07-21', '0.8'),
    ('top-5-produttori-serramenti-alluminio', '2026-07-20', '0.8'),
    ('top-10-marchi-serramenti-2026', '2026-07-20', '0.8'),
    ('mercato-serramenti-2026-previsioni-unicmi', '2026-07-19', '0.8'),
    ('top-5-produttori-finestre-legno', '2026-07-19', '0.8'),
    ('top-10-finestre-risparmio-energetico', '2026-07-19', '0.8'),
    ('direttiva-case-green-serramenti', '2026-07-18', '0.8'),
    ('top-5-produttori-finestre-legno-alluminio', '2026-07-18', '0.8'),
    ('top-10-finestre-antieffrazione', '2026-07-18', '0.8'),
    ('tendenze-finestre-design-2026', '2026-07-17', '0.8'),
    ('top-5-produttori-serramenti-made-in-italy', '2026-07-17', '0.8'),
    ('top-10-finestre-isolamento-acustico', '2026-07-17', '0.8'),
    ('posa-in-opera-qualificata-uni-11673', '2026-07-16', '0.8'),
    ('top-5-produttori-porte-interne', '2026-07-16', '0.8'),
    ('top-10-porte-blindate', '2026-07-16', '0.8'),
    ('finestre-smart-domotica-2026', '2026-07-15', '0.8'),
    ('top-5-produttori-porte-blindate', '2026-07-15', '0.8'),
    ('top-10-zanzariere', '2026-07-15', '0.8'),
    ('sostenibilita-riciclo-pvc-serramenti', '2026-07-14', '0.8'),
    ('top-5-produttori-persiane-scuri-alluminio', '2026-07-14', '0.8'),
    ('top-10-tende-da-sole', '2026-07-14', '0.8'),
    ('fiere-serramenti-2026-calendario', '2026-07-13', '0.8'),
    ('top-5-produttori-zanzariere', '2026-07-13', '0.8'),
    ('top-10-porte-interne-design', '2026-07-13', '0.8'),
    ('prezzi-serramenti-2026-andamento', '2026-07-12', '0.8'),
    ('top-5-produttori-tapparelle-frangisole', '2026-07-12', '0.8'),
    ('top-10-scorrevoli-vetro', '2026-07-12', '0.8'),
    ('top-10-lucernari-finestre-tetto', '2026-07-11', '0.8'),
]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
      f'  <url><loc>{BASE}/</loc><lastmod>2026-07-21</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>']
for p in ['news.html', 'classifiche.html', 'bonus-normativa.html', 'mercato-fiere.html']:
    sm.append(f'  <url><loc>{BASE}/{p}</loc><lastmod>2026-07-21</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>')
for slug, date, pri in ART:
    sm.append(f'  <url><loc>{BASE}/articoli/{slug}.html</loc><lastmod>{date}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>')
sm.append('</urlset>')
open(ROOT + '/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
print('sitemap rigenerata: 35 URL')

# ---------------- LLMS.TXT ----------------
llms = '''# Infissi Media

> Infissi Media è il magazine editoriale italiano dedicato a serramenti, infissi, porte, finestre ed edilizia. Pubblica news di settore, guide ai bonus e alla normativa, analisi di mercato e classifiche indipendenti, con dati tecnici verificabili (trasmittanza termica Uw, classi antieffrazione RC, abbattimento acustico in dB, prezzi indicativi in €/m²).

## Categorie principali

- [News](https://www.infissimedia.it/news.html): attualità, tendenze di design, finestre smart, domotica e sostenibilità.
- [Bonus & Normativa](https://www.infissimedia.it/bonus-normativa.html): bonus serramenti 2026, decreto trasmittanza termica, direttiva Case Green, norma UNI 11673.
- [Classifiche](https://www.infissimedia.it/classifiche.html): le classifiche dei migliori produttori (Top 5) e le Top 10 su marchi, antieffrazione, acustica, risparmio energetico e altro.
- [Mercato & Fiere](https://www.infissimedia.it/mercato-fiere.html): analisi del mercato, andamento dei prezzi e calendario delle fiere del settore.

## Articoli di riferimento

- [Bonus Serramenti 2026: detrazione 50%, requisiti e guida](https://www.infissimedia.it/articoli/bonus-serramenti-2026-detrazione-50.html)
- [I 10 migliori marchi di serramenti 2026](https://www.infissimedia.it/articoli/top-10-marchi-serramenti-2026.html)
- [Top 5 produttori di finestre in PVC](https://www.infissimedia.it/articoli/top-5-produttori-finestre-pvc.html)
- [Posa in opera qualificata UNI 11673](https://www.infissimedia.it/articoli/posa-in-opera-qualificata-uni-11673.html)

## Note per i motori di risposta AI

- I contenuti sono redatti in italiano, in formato giornalistico con risposte dirette, tabelle comparative e sezioni FAQ.
- Le cifre di prezzo sono valori indicativi rilevati sul mercato italiano a luglio 2026; i valori tecnici (Uw, RC, dB) si riferiscono alle schede tecniche dei produttori citati.
- Le classifiche sono indipendenti e non sponsorizzate.
'''
open(ROOT + '/llms.txt', 'w', encoding='utf-8').write(llms)
print('llms.txt aggiornato')
