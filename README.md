# Infissi Media

Magazine editoriale statico su **serramenti, infissi ed edilizia** — ottimizzato per SEO, GEO e AEO.

## Contenuto

- **35+ pagine HTML statiche**: home, 4 categorie editoriali (News, Bonus & Normativa, Classifiche, Mercato & Fiere), 30 articoli da 4.000+ caratteri, pagine istituzionali (Chi siamo, Contatti, Privacy, Cookie, Pubblicità), pagina di ricerca client-side
- **SEO**: meta completi, canonical, hreflang, JSON-LD (Article, BreadcrumbList, FAQPage, ItemList, Speakable), sitemap.xml, robots.txt, llms.txt
- **AEO**: box "Risposta rapida", FAQ strutturate, indice con jump-link in ogni articolo
- **Monetizzazione**: 6 formati di slot pubblicitari già predisposti (leaderboard, half page, box, in-article, in-feed, mobile anchor)
- **GDPR**: cookie banner leggero (~2 KB, zero dipendenze), font self-hosted
- **35 og:image** 1200×630 personalizzate in `assets/og/`

## Sviluppo

```bash
npm run dev        # server statico locale → http://localhost:7100/
npm run dev -- --port 8080   # porta personalizzata
```

Nessuna dipendenza: il dev server è un semplice `node server.js` (zero `node_modules`).

## Script di build (scripts/)

| Script | Funzione |
|---|---|
| `seo_upgrade.py` | TOC + jump-link, speakable, ItemList, hreflang |
| `restructure_v2.py` | menu, categorie, breadcrumb, sitemap |
| `build_infopages.py` | pagine istituzionali |
| `inject_legal_and_brands.py` | footer, cookie banner, link ai siti dei brand |
| `selfhost_fonts.py` | download font woff2 + fonts.css |
| `ready_for_google.py` | ricerca, og:image, font locali |

## Prima della pubblicazione

- Sostituire il dominio segnaposto `https://www.infissimedia.it` con quello reale (canonical, JSON-LD, sitemap, robots.txt, og:image)
- Inserire i codici degli annunci nei commenti `AD SLOT`
- Verificare su Google Search Console + invio sitemap
