#!/usr/bin/env python3
"""Infissi Media — self-hosting font:
- scarica i .woff2 (latin + latin-ext) in fonts/ e genera css/fonts.css
- scarica pochi .ttf in scripts/ttf/ per la generazione delle og:image (PIL)
Niente più richieste a Google Fonts: più veloce e GDPR-compliant.
"""
import re, os, urllib.request

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'
CSS_URL = ('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700'
           '&family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap')
CHROME_UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')

os.makedirs(ROOT + '/fonts', exist_ok=True)
os.makedirs(ROOT + '/scripts/ttf', exist_ok=True)

def fetch(url, ua):
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    return urllib.request.urlopen(req, timeout=40).read()

def parse_blocks(css):
    out = []
    for subset, body in re.findall(r'/\* ([a-z-]+) \*/\s*@font-face\s*\{(.*?)\}', css, re.S):
        out.append({
            'subset': subset,
            'family': re.search(r"font-family:\s*'([^']+)'", body).group(1),
            'style': re.search(r"font-style:\s*(\w+)", body).group(1),
            'weight': re.search(r"font-weight:\s*(\d+)", body).group(1),
            'url': re.search(r"url\((https://[^)]+)\)", body).group(1),
            'range': re.search(r"unicode-range:\s*([^;]+);", body).group(1),
        })
    return out

def fname(b, ext):
    fam = b['family'].lower().replace(' ', '-')
    it = 'i' if b['style'] == 'italic' else ''
    return f"{fam}-{b['weight']}{it}-{b['subset']}.{ext}"

# ---- 1. WOFF2 per il sito ----
css = fetch(CSS_URL, CHROME_UA).decode()
blocks = [b for b in parse_blocks(css) if b['subset'] in ('latin', 'latin-ext')]
print(f'blocchi woff2 trovati: {len(blocks)}')

css_out = ['/* Font self-hosted — Infissi Media (generato da scripts/selfhost_fonts.py) */']
for b in blocks:
    fn = fname(b, 'woff2')
    path = ROOT + '/fonts/' + fn
    if not os.path.exists(path):
        open(path, 'wb').write(fetch(b['url'], CHROME_UA))
    css_out.append(f"""/* {b['subset']} */
@font-face {{
  font-family: '{b['family']}';
  font-style: {b['style']};
  font-weight: {b['weight']};
  font-display: swap;
  src: url('../fonts/{fn}') format('woff2');
  unicode-range: {b['range']};
}}""")
open(ROOT + '/css/fonts.css', 'w', encoding='utf-8').write('\n'.join(css_out) + '\n')
print(f'woff2 scaricati: {len(blocks)} -> fonts/ ; css/fonts.css scritto')

# ---- 2. TTF per PIL (og:image) ----
ttf_css = fetch(CSS_URL, 'curl/8.1.0').decode()
want = {('Space Grotesk', '500', 'normal'), ('Space Grotesk', '700', 'normal'),
        ('Inter', '400', 'normal'), ('Inter', '600', 'normal'), ('Inter', '400', 'italic')}
ttf_blocks = [b for b in parse_blocks(ttf_css)
              if b['subset'] == 'latin' and (b['family'], b['weight'], b['style']) in want]
for b in ttf_blocks:
    fn = fname(b, 'ttf')
    path = ROOT + '/scripts/ttf/' + fn
    if not os.path.exists(path):
        open(path, 'wb').write(fetch(b['url'], 'curl/8.1.0'))
    print('ttf:', fn)
print('fatto')
