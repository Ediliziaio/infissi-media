#!/usr/bin/env python3
"""Infissi Media — genera le pagine istituzionali:
chi-siamo.html, contatti.html, privacy-policy.html, cookie-policy.html, pubblicita.html
"""
import os

ROOT = '/Users/agenteai/Documents/kimi/workspace/infissi-media'
BASE = 'https://www.infissimedia.it'

FONT_LINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">')

NAV = '''<nav class="mainnav" aria-label="Navigazione principale">
  <div class="container">
    <a href="index.html">Home</a>
    <a href="news.html">News</a>
    <a href="bonus-normativa.html">Bonus &amp; Normativa</a>
    <a href="classifiche.html">Classifiche</a>
    <a href="mercato-fiere.html">Mercato &amp; Fiere</a>
    <a href="contatti.html">Contatti</a>
  </div>
</nav>'''

FOOTER = '''<footer>
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
          <li><a href="chi-siamo.html">Chi siamo</a></li>
          <li><a href="pubblicita.html">Pubblicità</a></li>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
          <li><a href="cookie-policy.html">Cookie Policy</a></li>
          <li><a href="#" data-cookie-settings>Impostazioni cookie</a></li>
          <li><a href="sitemap.xml">Mappa del sito</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Infissi Media — Tutti i diritti riservati.</span>
      <span><a href="privacy-policy.html">Privacy</a> · <a href="cookie-policy.html">Cookie</a> · <a href="contatti.html">Contatti</a></span>
    </div>
  </div>
</footer>'''

def page(filename, doc_title, meta_desc, h1, intro, body_html, schema_type='WebPage'):
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
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Infissi Media">
<meta property="og:title" content="{doc_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{BASE}/{filename}">
<meta property="og:image" content="{BASE}/assets/logo.png">
<meta property="og:locale" content="it_IT">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "@id": "{BASE}/{filename}",
  "url": "{BASE}/{filename}",
  "name": "{doc_title}",
  "description": "{meta_desc}",
  "inLanguage": "it-IT",
  "isPartOf": {{ "@id": "{BASE}/#website" }}
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

{NAV}

<main class="container">
  <nav class="breadcrumb" aria-label="Percorso di navigazione">
    <a href="index.html">Home</a><span>›</span>{h1}
  </nav>

  <header class="cat-head">
    <h1>{h1}</h1>
    <p>{intro}</p>
  </header>

  <div class="article-body" style="padding:28px 0 40px;max-width:820px">
{body_html}
  </div>
</main>

{FOOTER}

<div class="ad-slot ad-mobile-sticky" data-format="320×50 · mobile anchor" id="ad-mobile-sticky"></div>
<script src="js/cookie-consent.js" defer></script>

</body>
</html>
'''
    open(os.path.join(ROOT, filename), 'w', encoding='utf-8').write(html)
    print('pagina creata:', filename)

# ---------------- CHI SIAMO ----------------
page('chi-siamo.html',
     'Chi Siamo — Infissi Media: il magazine dei serramenti e dell\'edilizia',
     'Infissi Media è il magazine indipendente su serramenti, infissi ed edilizia: chi siamo, il metodo delle nostre classifiche e la redazione.',
     'Chi siamo',
     'Il punto di riferimento indipendente per chi sceglie, vende o installa serramenti in Italia.',
     '''    <p><strong>Infissi Media</strong> è un magazine editoriale nato con un obiettivo preciso: portare chiarezza nel mondo dei serramenti, degli infissi e dell'edilizia. Parliamo a tre pubblichi diversi — le <strong>famiglie</strong> che devono sostituire le finestre di casa, i <strong>professionisti</strong> (serramentisti, posatori, progettisti) e le <strong>aziende</strong> del comparto — con lo stesso linguaggio: dati tecnici verificabili, prezzi reali e guide pratiche.</p>

    <h2>Il nostro metodo: classifiche indipendenti</h2>
    <p>Le classifiche di Infissi Media (le Top 5 dei produttori e le Top 10 di prodotto) nascono dall'analisi di <strong>schede tecniche, certificazioni e valori misurabili</strong>: trasmittanza termica Uw, classi antieffrazione RC secondo la norma UNI ENV 1627, abbattimento acustico in decibel, dotazione vetraria, garanzie e rete di assistenza sul territorio italiano. I prezzi indicati sono rilevazioni di listino aggiornate e presentate sempre come valori indicativi. <strong>Nessuna posizione è sponsorizzata</strong>: i produttori non possono acquistare un posto in classifica.</p>

    <h2>Cosa pubblichiamo</h2>
    <ul class="bullets">
      <li><strong>News</strong>: attualità, tendenze di design, domotica e sostenibilità del settore.</li>
      <li><strong>Bonus &amp; Normativa</strong>: guide operative su detrazioni fiscali, decreti e norme tecniche.</li>
      <li><strong>Classifiche</strong>: i migliori produttori e i migliori prodotti, con dati alla mano.</li>
      <li><strong>Mercato &amp; Fiere</strong>: analisi del comparto, prezzi e calendario degli eventi.</li>
    </ul>

    <h2 id="redazione">La redazione</h2>
    <p>La redazione di Infissi Media è composta da giornalisti e tecnici che seguono il comparto serramenti-edilizia: schede prodotto, normativa UNI/EN, mercato e fiere. Ogni articolo passa attraverso una revisione tecnica prima della pubblicazione e viene aggiornato quando cambiano prezzi, norme o gamme di prodotto — la data di ultimo aggiornamento è sempre visibile in apertura dell'articolo.</p>
    <p><strong>Direttore responsabile</strong>: in fase di nomina — la testata è in corso di registrazione presso il Tribunale competente.</p>

    <h2>Contatti</h2>
    <p>Per segnalazioni, comunicati stampa, correzioni o proposte di collaborazione scrivici dalla pagina <a href="contatti.html">Contatti</a>. Per le proposte commerciali e gli spazi pubblicitari visita la pagina <a href="pubblicita.html">Pubblicità</a>.</p>''',
     'AboutPage')

# ---------------- CONTATTI ----------------
page('contatti.html',
     'Contatti — Infissi Media',
     'Contatta la redazione di Infissi Media: segnalazioni, comunicati stampa, correzioni, proposte commerciali e pubblicità.',
     'Contatti',
     'Redazione, ufficio commerciale e segnalazioni: ecco come raggiungerci.',
     '''    <p>Per qualsiasi richiesta puoi scriverci via email o compilare il modulo in questa pagina: rispondiamo in genere entro 2 giorni lavorativi.</p>

    <h2>Email dirette</h2>
    <table>
      <caption>I recapiti di Infissi Media</caption>
      <thead><tr><th>Ufficio</th><th>Email</th><th>Per cosa</th></tr></thead>
      <tbody>
        <tr><td><strong>Redazione</strong></td><td><a href="mailto:redazione@infissimedia.it">redazione@infissimedia.it</a></td><td>Comunicati stampa, segnalazioni, correzioni</td></tr>
        <tr><td><strong>Pubblicità</strong></td><td><a href="mailto:pubblicita@infissimedia.it">pubblicita@infissimedia.it</a></td><td>Spazi adv, branded content, media kit</td></tr>
        <tr><td><strong>Privacy</strong></td><td><a href="mailto:privacy@infissimedia.it">privacy@infissimedia.it</a></td><td>Diritti GDPR e richieste sui dati personali</td></tr>
      </tbody>
    </table>

    <h2>Modulo di contatto</h2>
    <form action="#" method="post" style="display:grid;gap:14px;max-width:560px">
      <label style="font-size:14px;font-weight:600">Nome e cognome
        <input type="text" name="nome" required style="width:100%;padding:11px 12px;border:1px solid var(--rule);border-radius:6px;margin-top:6px;font-size:15px"></label>
      <label style="font-size:14px;font-weight:600">Email
        <input type="email" name="email" required style="width:100%;padding:11px 12px;border:1px solid var(--rule);border-radius:6px;margin-top:6px;font-size:15px"></label>
      <label style="font-size:14px;font-weight:600">Messaggio
        <textarea name="messaggio" rows="6" required style="width:100%;padding:11px 12px;border:1px solid var(--rule);border-radius:6px;margin-top:6px;font-size:15px;font-family:var(--sans)"></textarea></label>
      <label style="font-size:13px;display:flex;gap:8px;align-items:flex-start">
        <input type="checkbox" required style="margin-top:3px">
        <span>Ho letto la <a href="privacy-policy.html">Privacy Policy</a> e acconsento al trattamento dei dati per essere ricontattato.</span></label>
      <button type="submit" style="background:var(--accent-dark);color:#fff;border:0;border-radius:8px;padding:13px;font-weight:700;font-size:14px;cursor:pointer">Invia il messaggio</button>
    </form>''',
     'ContactPage')

# ---------------- PRIVACY POLICY ----------------
page('privacy-policy.html',
     'Privacy Policy — Infissi Media',
     'Informativa privacy di Infissi Media ai sensi del GDPR (Reg. UE 2016/679): dati raccolti, finalità, basi giuridiche, diritti degli utenti e contatti.',
     'Privacy Policy',
     'Informativa sul trattamento dei dati personali ai sensi del Regolamento (UE) 2016/679 (GDPR). Ultimo aggiornamento: 21 luglio 2026.',
     '''    <h2>1. Titolare del trattamento</h2>
    <p>Il Titolare del trattamento dei dati personali raccolti tramite il sito www.infissimedia.it è <strong>Infissi Media</strong> (dati societari in fase di registrazione), contattabile all'indirizzo email <a href="mailto:privacy@infissimedia.it">privacy@infissimedia.it</a>.</p>

    <h2>2. Tipologie di dati raccolti</h2>
    <ul class="bullets">
      <li><strong>Dati di navigazione</strong>: indirizzo IP, tipo di browser, pagine visitate, orari di accesso — raccolti in forma aggregata e anonima per finalità statistiche e di sicurezza.</li>
      <li><strong>Dati forniti volontariamente</strong>: nome, indirizzo email e contenuto dei messaggi inviati tramite il modulo contatti o l'iscrizione alla newsletter.</li>
      <li><strong>Cookie e strumenti analoghi</strong>: per i dettagli consulta la <a href="cookie-policy.html">Cookie Policy</a>.</li>
    </ul>

    <h2>3. Finalità e base giuridica del trattamento</h2>
    <table>
      <caption>Finalità e basi giuridiche</caption>
      <thead><tr><th>Finalità</th><th>Base giuridica</th></tr></thead>
      <tbody>
        <tr><td>Rispondere alle richieste inviate via modulo o email</td><td>Esecuzione di misure precontrattuali (art. 6.1.b GDPR)</td></tr>
        <tr><td>Invio della newsletter richiesta</td><td>Consenso (art. 6.1.a GDPR), revocabile in ogni momento</td></tr>
        <tr><td>Statistiche aggregate di accesso e sicurezza del sito</td><td>Legittimo interesse (art. 6.1.f GDPR)</td></tr>
        <tr><td>Pubblicità personalizzata di terze parti</td><td>Consenso (art. 6.1.a GDPR), raccolto tramite il cookie banner</td></tr>
      </tbody>
    </table>

    <h2>4. Conservazione dei dati</h2>
    <p>I dati di contatto sono conservati per il tempo necessario a gestire la richiesta e comunque non oltre 24 mesi; i dati della newsletter fino a revoca del consenso; i dati di navigazione in forma aggregata per un massimo di 14 mesi.</p>

    <h2>5. Comunicazione a terzi</h2>
    <p>I dati non sono venduti né ceduti a terzi. Possono essere trattati da fornitori tecnici (hosting, piattaforme di invio email, network pubblicitari) nominati responsabili del trattamento ai sensi dell'art. 28 GDPR, anche con server ubicati fuori dall'UE nel rispetto delle garanzie previste dagli artt. 44 e ss. GDPR.</p>

    <h2>6. I tuoi diritti</h2>
    <p>In qualità di interessato puoi esercitare in qualsiasi momento i diritti previsti dagli artt. 15-22 GDPR: <strong>accesso, rettifica, cancellazione, limitazione, portabilità, opposizione</strong> e revoca del consenso. Per esercitarli scrivi a <a href="mailto:privacy@infissimedia.it">privacy@infissimedia.it</a>. Hai inoltre diritto di reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>

    <h2>7. Modifiche a questa informativa</h2>
    <p>Questa informativa può essere aggiornata periodicamente; la data di ultimo aggiornamento è indicata in cima alla pagina. Ti invitiamo a consultarla regolarmente.</p>''',
     'WebPage')

# ---------------- COOKIE POLICY ----------------
page('cookie-policy.html',
     'Cookie Policy — Infissi Media',
     'Cookie Policy di Infissi Media: cookie tecnici, analitici e pubblicitari, come gestire o revocare il consenso e come disattivare i cookie dal browser.',
     'Cookie Policy',
     'Quali cookie usiamo, perché, e come gestire le tue preferenze. Ultimo aggiornamento: 21 luglio 2026.',
     '''    <h2>1. Cosa sono i cookie</h2>
    <p>I cookie sono piccoli file di testo che i siti visitati salvano sul tuo dispositivo per ricordare preferenze, sessioni e impostazioni. Su questo sito usiamo anche il <em>local storage</em> del browser, che ha una funzione analoga.</p>

    <h2>2. Cookie utilizzati da questo sito</h2>
    <table>
      <caption>Elenco dei cookie e strumenti di memorizzazione</caption>
      <thead><tr><th>Nome</th><th>Tipo</th><th>Durata</th><th>Finalità</th></tr></thead>
      <tbody>
        <tr><td><code>im_cookie_consent</code></td><td>Tecnico (local storage)</td><td>12 mesi</td><td>Memorizza la tua scelta sul consenso cookie</td></tr>
        <tr><td>Cookie analitici di terze parti</td><td>Analitici</td><td>Fino a 14 mesi</td><td>Statistiche aggregate di visita — installati solo con il consenso</td></tr>
        <tr><td>Cookie pubblicitari di terze parti</td><td>Profilazione</td><td>Variabile</td><td>Annunci personalizzati — installati solo con il consenso</td></tr>
      </tbody>
    </table>

    <h2>3. Cookie tecnici (sempre attivi)</h2>
    <p>I cookie tecnici sono necessari al funzionamento del sito e non richiedono consenso. Questo sito ne usa uno solo: quello che ricorda la tua scelta nel banner cookie, così da non mostrartelo a ogni visita.</p>

    <h2>4. Cookie di terze parti (solo con il tuo consenso)</h2>
    <p>Gli spazi pubblicitari del sito possono ospitare network di terze parti (es. Google AdSense) che, <strong>solo dopo il tuo "Accetta tutto"</strong>, possono installare cookie per mostrarti annunci personalizzati in base ai tuoi interessi. Scegliendo "Rifiuta" navighi il sito con i soli cookie tecnici.</p>

    <h2>5. Come modificare o revocare il consenso</h2>
    <p>Puoi cambiare la tua scelta in qualsiasi momento: <a href="#" data-cookie-settings><strong>clicca qui per riaprire il pannello delle preferenze cookie</strong></a>. La revoca ha effetto da quel momento in poi.</p>

    <h2>6. Come disattivare i cookie dal browser</h2>
    <ul class="bullets">
      <li><strong>Chrome</strong>: Impostazioni → Privacy e sicurezza → Cookie e altri dati dei siti</li>
      <li><strong>Safari</strong>: Preferenze → Privacy → Cookie e dati di siti web</li>
      <li><strong>Firefox</strong>: Impostazioni → Privacy e sicurezza → Cookie e dati dei siti web</li>
      <li><strong>Edge</strong>: Impostazioni → Cookie e autorizzazioni sito → Cookie</li>
    </ul>
    <p>La disattivazione completa dei cookie tecnici può compromettere alcune funzionalità del sito.</p>

    <h2>7. Maggiori informazioni</h2>
    <p>Per il trattamento dei dati personali consulta la <a href="privacy-policy.html">Privacy Policy</a>. Per richieste specifiche: <a href="mailto:privacy@infissimedia.it">privacy@infissimedia.it</a>.</p>''',
     'WebPage')

# ---------------- PUBBLICITÀ ----------------
page('pubblicita.html',
     'Pubblicità su Infissi Media — Spazi adv e branded content',
     'Media kit di Infissi Media: formati pubblicitari disponibili (leaderboard, half page, in-article, mobile anchor), branded content e contatti commerciali.',
     'Pubblicità',
     'Raggiungi lettori che stanno davvero scegliendo finestre, porte e serramenti: famiglie in ristrutturazione e professionisti del comparto.',
     '''    <p>Infissi Media intercetta un pubblico ad altissima intenzione d'acquisto: chi cerca "migliori finestre in PVC", "bonus serramenti 2026" o "porte blindate classifica" sta per spendere migliaia di euro. I nostri spazi pubblicitari sono progettati per essere visibili senza rovinare l'esperienza di lettura.</p>

    <h2>Formati disponibili</h2>
    <table>
      <caption>Spazi pubblicitari su Infissi Media</caption>
      <thead><tr><th>Formato</th><th>Dimensioni</th><th>Posizione</th></tr></thead>
      <tbody>
        <tr><td><strong>Leaderboard</strong></td><td>970×250</td><td>Testata home e categorie, sopra la piega</td></tr>
        <tr><td><strong>Half Page</strong></td><td>300×600</td><td>Sidebar di home e articoli, sticky</td></tr>
        <tr><td><strong>Box</strong></td><td>300×250</td><td>Sidebar, primo impatto</td></tr>
        <tr><td><strong>In-Article</strong></td><td>336×280</td><td>Dentro il testo di tutti gli articoli</td></tr>
        <tr><td><strong>In-Feed</strong></td><td>728×90</td><td>Tra le sezioni della home</td></tr>
        <tr><td><strong>Mobile Anchor</strong></td><td>320×50</td><td>Fisso in basso su mobile</td></tr>
      </tbody>
    </table>

    <h2>Branded content e partnership</h2>
    <p>Per le aziende del settore sono disponibili <strong>articoli sponsorizzati</strong> (sempre contrassegnati come tali e sempre fuori dalle classifiche, che restano indipendenti), <strong>scedule prodotto</strong> e presenza nelle guide di settore. Le posizioni editoriali delle classifiche non sono in vendita.</p>

    <h2>Contatti commerciali</h2>
    <p>Per listini, disponibilità e media kit: <a href="mailto:pubblicita@infissimedia.it"><strong>pubblicita@infissimedia.it</strong></a> oppure il modulo nella pagina <a href="contatti.html">Contatti</a>.</p>''',
     'WebPage')

print('fatto: 5 pagine istituzionali')
