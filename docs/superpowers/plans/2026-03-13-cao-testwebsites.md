# CAO Monitor Testwebsites Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zeven statische testwebsites bouwen die dagelijks automatisch nep-content genereren via de Claude API, gehost op GitHub Pages, om de CAO-URL-monitor te testen met bewuste edge cases.

**Architecture:** Één GitHub-repo met een map per site onder `sites/`. Een Python-script (`generator/generate.py`) draait dagelijks via GitHub Actions, roept de Claude API aan om nep-artikelen/PDFs/paginawijzigingen te genereren, en commit het resultaat. GitHub Pages serveert de statische bestanden publiek.

**Tech Stack:** Python 3.11+, Anthropic Python SDK (`anthropic`), GitHub Actions (ubuntu-latest), GitHub Pages, HTML/CSS (geen frameworks)

---

## Chunk 1: Git-repo, GitHub Pages en projectskeleton

### Task 1: Git installeren en GitHub-account klaarzetten

**Files:** geen

- [ ] **Stap 1: Controleer of git geïnstalleerd is**

  Open PowerShell en run:
  ```
  git --version
  ```
  Als je een versienummer ziet (bijv. `git version 2.43.0.windows.1`), sla stap 2 over.

- [ ] **Stap 2: Installeer git (alleen als stap 1 niets gaf)**

  Download van https://git-scm.com/download/win en installeer met standaardinstellingen.

- [ ] **Stap 3: Stel je naam en e-mail in voor git**

  ```bash
  git config --global user.name "Jouw Naam"
  git config --global user.email "jouw@email.com"
  ```

- [ ] **Stap 4: Zorg dat je een GitHub-account hebt**

  Ga naar https://github.com en log in (of maak een account aan).

---

### Task 2: Nieuwe GitHub-repo aanmaken

**Files:** geen

- [ ] **Stap 1: Maak een nieuwe repo aan op GitHub**

  Ga naar https://github.com/new en vul in:
  - Repository name: `cao-testwebsites`
  - Visibility: **Public** (vereist voor gratis GitHub Pages)
  - Vink NIETS aan bij "Initialize this repository"
  - Klik "Create repository"

- [ ] **Stap 2: Onthoud je GitHub-gebruikersnaam**

  Die heb je nodig voor de URLs straks. Het patroon wordt:
  `https://<jouw-gebruikersnaam>.github.io/cao-testwebsites/sites/<site-naam>/`

---

### Task 3: Lokale repo initialiseren en koppelen

**Files:** `C:/Users/vansc/Documents/Test websites/`

- [ ] **Stap 1: Open terminal in de projectmap**

  Open PowerShell en navigeer naar de map:
  ```bash
  cd "C:/Users/vansc/Documents/Test websites"
  ```

- [ ] **Stap 2: Initialiseer de git-repo**

  ```bash
  git init
  git branch -M main
  ```

- [ ] **Stap 3: Koppel aan GitHub**

  Vervang `<gebruikersnaam>` door jouw GitHub-gebruikersnaam:
  ```bash
  git remote add origin https://github.com/<gebruikersnaam>/cao-testwebsites.git
  ```

---

### Task 4: .gitignore aanmaken

**Files:**
- Create: `.gitignore`

- [ ] **Stap 1: Maak .gitignore aan**

  Maak het bestand `C:/Users/vansc/Documents/Test websites/.gitignore` met deze inhoud:
  ```
  __pycache__/
  *.py[cod]
  .env
  .venv/
  venv/
  *.egg-info/
  .DS_Store
  Thumbs.db
  ```

---

### Task 5: Projectskeleton aanmaken

**Files:**
- Create: `index.html` (root)
- Create: `generator/sites.json`
- Create: `generator/state.json`
- Create: `sites/vakbond-nieuws/index.html`
- Create: `sites/vakbond-nieuws/artikelen/.gitkeep`
- Create: `sites/overheid-arbeidsmarkt/index.html`
- Create: `sites/overheid-arbeidsmarkt/artikelen/.gitkeep`
- Create: `sites/hr-magazine/index.html`
- Create: `sites/hr-magazine/artikelen/.gitkeep`
- Create: `sites/sector-zorg/index.html`
- Create: `sites/sector-zorg/docs/.gitkeep`
- Create: `sites/werkgevers-platform/index.html`
- Create: `sites/werkgevers-platform/docs/.gitkeep`
- Create: `sites/arbeidsrecht-updates/index.html`
- Create: `sites/loondienst-nieuws/index.html`
- Create: `generator/archive/vakbond-nieuws/.gitkeep`
- Create: `generator/archive/overheid-arbeidsmarkt/.gitkeep`
- Create: `generator/archive/hr-magazine/.gitkeep`

- [ ] **Stap 1: Maak de mappenstructuur aan**

  ```bash
  mkdir -p .github/workflows
  mkdir -p generator/templates
  mkdir -p generator/archive/vakbond-nieuws
  mkdir -p generator/archive/overheid-arbeidsmarkt
  mkdir -p generator/archive/hr-magazine
  mkdir -p sites/vakbond-nieuws/artikelen
  mkdir -p sites/overheid-arbeidsmarkt/artikelen
  mkdir -p sites/hr-magazine/artikelen
  mkdir -p sites/sector-zorg/docs
  mkdir -p sites/werkgevers-platform/docs
  mkdir -p sites/arbeidsrecht-updates
  mkdir -p sites/loondienst-nieuws
  ```

- [ ] **Stap 2: Maak .gitkeep bestanden aan**

  ```bash
  touch generator/archive/vakbond-nieuws/.gitkeep
  touch generator/archive/overheid-arbeidsmarkt/.gitkeep
  touch generator/archive/hr-magazine/.gitkeep
  touch sites/vakbond-nieuws/artikelen/.gitkeep
  touch sites/overheid-arbeidsmarkt/artikelen/.gitkeep
  touch sites/hr-magazine/artikelen/.gitkeep
  touch sites/sector-zorg/docs/.gitkeep
  touch sites/werkgevers-platform/docs/.gitkeep
  ```

- [ ] **Stap 3: Maak root index.html aan**

  Inhoud van `index.html`:
  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>CAO Monitor Testwebsites</title>
  </head>
  <body>
    <h1>CAO Monitor Testwebsites</h1>
    <ul>
      <li><a href="sites/vakbond-nieuws/">Vakbond Nieuws</a></li>
      <li><a href="sites/overheid-arbeidsmarkt/">Overheid Arbeidsmarkt</a></li>
      <li><a href="sites/hr-magazine/">HR Magazine</a></li>
      <li><a href="sites/sector-zorg/">Sector Zorg</a></li>
      <li><a href="sites/werkgevers-platform/">Werkgevers Platform</a></li>
      <li><a href="sites/arbeidsrecht-updates/">Arbeidsrecht Updates</a></li>
      <li><a href="sites/loondienst-nieuws/">Loondienst Nieuws</a></li>
    </ul>
  </body>
  </html>
  ```

- [ ] **Stap 4: Maak generator/sites.json aan**

  Vervang `<gebruikersnaam>` door jouw GitHub-gebruikersnaam:
  ```json
  {
    "vakbond-nieuws": {
      "type": "artikel",
      "stijl": "vakbond",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/vakbond-nieuws/",
      "relevantie_kans": 0.6,
      "edge_cases": ["korte_slug", "anker_url", "cacao_false_positive"]
    },
    "overheid-arbeidsmarkt": {
      "type": "artikel",
      "stijl": "overheid",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/overheid-arbeidsmarkt/",
      "relevantie_kans": 0.5,
      "edge_cases": ["pagina_url", "relevant_zonder_cao_woord", "noindex_tag"]
    },
    "hr-magazine": {
      "type": "artikel",
      "stijl": "hr-magazine",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/hr-magazine/",
      "relevantie_kans": 0.4,
      "edge_cases": ["teruggedateerd", "oud_nieuws_herplaatst", "artikel_verdwijnt"]
    },
    "sector-zorg": {
      "type": "pdf",
      "stijl": "sector",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/sector-zorg/",
      "edge_cases": ["zelfde_url_nieuwe_inhoud", "diep_verstopt"]
    },
    "werkgevers-platform": {
      "type": "pdf",
      "stijl": "werkgevers",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/werkgevers-platform/",
      "edge_cases": ["korte_pdf_naam", "pdf_verdwijnt_nieuwe_naam"]
    },
    "arbeidsrecht-updates": {
      "type": "pagina",
      "stijl": "juridisch",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/arbeidsrecht-updates/",
      "edge_cases": ["alleen_footer", "typofout", "grote_redesign"]
    },
    "loondienst-nieuws": {
      "type": "pagina",
      "stijl": "nieuws",
      "monitor_url": "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/loondienst-nieuws/",
      "edge_cases": ["cookiebanner_wissel", "content_zonder_url"]
    }
  }
  ```

- [ ] **Stap 5: Maak generator/state.json aan**

  ```json
  {
    "vakbond-nieuws": {},
    "overheid-arbeidsmarkt": {},
    "hr-magazine": {
      "verdwenen_slug": null,
      "dag": null,
      "actieve_template": null
    },
    "sector-zorg": {},
    "werkgevers-platform": {},
    "arbeidsrecht-updates": {
      "actieve_template": "a"
    },
    "loondienst-nieuws": {}
  }
  ```

- [ ] **Stap 6: Eerste commit en push**

  ```bash
  git add .
  git commit -m "chore: initial project skeleton"
  git push -u origin main
  ```

  Als git om inloggegevens vraagt: gebruik je GitHub-gebruikersnaam en een Personal Access Token (niet je wachtwoord). Maak een token aan via https://github.com/settings/tokens/new — kies "repo" scope, vul een naam in, klik "Generate token", kopieer de waarde.

---

### Task 6: GitHub Pages inschakelen

**Files:** geen

- [ ] **Stap 1: Ga naar de repo-instellingen op GitHub**

  Ga naar `https://github.com/<gebruikersnaam>/cao-testwebsites/settings/pages`

- [ ] **Stap 2: Stel GitHub Pages in**

  - Source: **Deploy from a branch**
  - Branch: `main`
  - Folder: `/ (root)`
  - Klik "Save"

- [ ] **Stap 3: Verifieer na ~1 minuut**

  Bezoek `https://<gebruikersnaam>.github.io/cao-testwebsites/` — je zou de root index.html moeten zien.

---

## Chunk 2: HTML-templates en initiële site-pagina's

### Task 7: HTML-templates aanmaken (7 stijlen)

**Files:**
- Create: `generator/templates/vakbond.html`
- Create: `generator/templates/overheid.html`
- Create: `generator/templates/hr-magazine.html`
- Create: `generator/templates/sector.html`
- Create: `generator/templates/werkgevers.html`
- Create: `generator/templates/juridisch_a.html`
- Create: `generator/templates/juridisch_b.html`
- Create: `generator/templates/nieuws.html`

De templates gebruiken placeholders `{{TITLE}}`, `{{BODY}}`, `{{FOOTER_YEAR}}`, `{{ARTICLES_LIST}}` die door `generate.py` worden ingevuld.

- [ ] **Stap 1: Maak `generator/templates/vakbond.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | VakbondNieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f4f4f4; }
      header { background: #c00; color: white; padding: 15px 20px; }
      header h1 { margin: 0; font-size: 1.6em; }
      nav a { color: white; margin-right: 15px; text-decoration: none; font-size: 0.9em; }
      main { background: white; padding: 20px; margin-top: 10px; }
      .artikel-lijst a { display: block; padding: 8px 0; border-bottom: 1px solid #eee; color: #c00; }
      footer { font-size: 0.8em; color: #666; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ccc; }
    </style>
  </head>
  <body>
    <header>
      <h1>VakbondNieuws</h1>
      <nav><a href="../">Home</a> <a href="#">CAO</a> <a href="#">Leden</a> <a href="#">Contact</a></nav>
    </header>
    <main>
      <h2>{{TITLE}}</h2>
      {{BODY}}
      <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
    </main>
    <footer>
      <p>&copy; {{FOOTER_YEAR}} VakbondNieuws. Alle rechten voorbehouden.</p>
    </footer>
  </body>
  </html>
  ```

- [ ] **Stap 2: Maak `generator/templates/overheid.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Overheid Arbeidsmarkt</title>
    <style>
      body { font-family: "Rijksoverheid Serif", Georgia, serif; max-width: 960px; margin: 0 auto; padding: 0; background: white; }
      header { background: #154273; color: white; padding: 12px 20px; display: flex; align-items: center; gap: 15px; }
      header h1 { margin: 0; font-size: 1.3em; font-weight: normal; }
      .lint { height: 4px; background: linear-gradient(to right, #AE1C28 33%, white 33%, white 66%, #21468B 66%); }
      nav { background: #f0f0f0; padding: 8px 20px; }
      nav a { color: #154273; margin-right: 20px; text-decoration: none; font-size: 0.9em; }
      main { padding: 20px; }
      .artikel-lijst a { display: block; padding: 6px 0; border-bottom: 1px solid #ddd; color: #154273; }
      footer { background: #154273; color: #ccc; font-size: 0.8em; padding: 15px 20px; margin-top: 30px; }
    </style>
  </head>
  <body>
    <div class="lint"></div>
    <header><h1>Overheid.nl | Arbeidsmarkt</h1></header>
    <nav><a href="#">Home</a> <a href="#">Arbeidsmarkt</a> <a href="#">CAO-register</a> <a href="#">Contact</a></nav>
    <main>
      <h1>{{TITLE}}</h1>
      {{BODY}}
      <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
    </main>
    <footer>&copy; {{FOOTER_YEAR}} Rijksoverheid</footer>
  </body>
  </html>
  ```

- [ ] **Stap 3: Maak `generator/templates/hr-magazine.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | HR Magazine</title>
    <style>
      body { font-family: "Helvetica Neue", Helvetica, sans-serif; max-width: 880px; margin: 0 auto; padding: 20px; }
      header { border-bottom: 3px solid #2d6a9f; padding-bottom: 10px; margin-bottom: 20px; }
      header h1 { color: #2d6a9f; font-size: 2em; margin: 0; }
      header span { font-size: 0.85em; color: #888; }
      .artikel-lijst a { display: block; padding: 10px 0; border-bottom: 1px solid #eee; color: #2d6a9f; font-weight: bold; }
      footer { margin-top: 40px; font-size: 0.75em; color: #aaa; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
  </head>
  <body>
    <header>
      <h1>HR Magazine</h1>
      <span>Voor HR-professionals</span>
    </header>
    <main>
      <h2>{{TITLE}}</h2>
      {{BODY}}
      <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
    </main>
    <footer>&copy; {{FOOTER_YEAR}} HR Magazine Nederland</footer>
  </body>
  </html>
  ```

- [ ] **Stap 4: Maak `generator/templates/sector.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | Zorg & Welzijn Nieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
      header { background: #00857c; color: white; padding: 15px 20px; border-radius: 4px 4px 0 0; }
      header h1 { margin: 0; }
      main { background: white; padding: 20px; border: 1px solid #ddd; }
      .pdf-sectie { margin-top: 20px; padding: 15px; background: #f0faf9; border-left: 4px solid #00857c; }
      .pdf-sectie a { color: #00857c; }
      footer { font-size: 0.8em; color: #888; margin-top: 15px; }
      details { margin-top: 30px; padding: 10px; background: #fafafa; border: 1px solid #eee; }
      details summary { cursor: pointer; color: #666; font-size: 0.9em; }
    </style>
  </head>
  <body>
    <header><h1>Zorg &amp; Welzijn Nieuws</h1></header>
    <main>
      <h2>{{TITLE}}</h2>
      {{BODY}}
      {{ARTICLES_LIST}}
    </main>
    <footer>&copy; {{FOOTER_YEAR}} Zorg &amp; Welzijn Nieuws</footer>
  </body>
  </html>
  ```

- [ ] **Stap 5: Maak `generator/templates/werkgevers.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | Werkgevers Platform NL</title>
    <style>
      body { font-family: "Trebuchet MS", sans-serif; max-width: 920px; margin: 0 auto; padding: 20px; }
      header { background: #1a3c5e; color: white; padding: 15px 25px; }
      header h1 { margin: 0; font-size: 1.5em; }
      nav a { color: #ccc; margin-right: 15px; text-decoration: none; font-size: 0.85em; }
      .content { padding: 20px 0; }
      .documenten { margin-top: 20px; background: #f5f8fb; padding: 15px; border: 1px solid #d0dce8; }
      .documenten a { color: #1a3c5e; display: block; padding: 4px 0; }
      footer { font-size: 0.8em; color: #777; border-top: 1px solid #ddd; margin-top: 30px; padding-top: 10px; }
    </style>
  </head>
  <body>
    <header>
      <h1>Werkgevers Platform NL</h1>
      <nav><a href="#">Home</a> <a href="#">CAO-tools</a> <a href="#">Documenten</a> <a href="#">Contact</a></nav>
    </header>
    <div class="content">
      <h2>{{TITLE}}</h2>
      {{BODY}}
      {{ARTICLES_LIST}}
    </div>
    <footer>&copy; {{FOOTER_YEAR}} Werkgevers Platform NL</footer>
  </body>
  </html>
  ```

- [ ] **Stap 6: Maak `generator/templates/juridisch_a.html` (template variant A)**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | Arbeidsrecht Updates</title>
    <style>
      body { font-family: Georgia, serif; max-width: 860px; margin: 0 auto; padding: 20px; background: white; }
      header { border-bottom: 2px solid #333; padding-bottom: 10px; }
      header h1 { font-size: 1.8em; color: #333; }
      nav a { color: #555; margin-right: 20px; font-size: 0.9em; }
      article { margin: 20px 0; }
      .artikel-lijst a { display: block; padding: 5px 0; border-bottom: 1px dotted #ccc; color: #333; }
      footer { margin-top: 40px; font-size: 0.75em; color: #999; border-top: 1px solid #ddd; padding-top: 8px; }
    </style>
  </head>
  <body>
    <header>
      <h1>Arbeidsrecht Updates</h1>
      <nav><a href="#">Jurisprudentie</a> <a href="#">Wetgeving</a> <a href="#">CAO-recht</a></nav>
    </header>
    <article>
      <h2>{{TITLE}}</h2>
      {{BODY}}
      <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
    </article>
    <footer>&copy; {{FOOTER_YEAR}} Arbeidsrecht Updates. Alle informatie onder voorbehoud.</footer>
  </body>
  </html>
  ```

- [ ] **Stap 7: Maak `generator/templates/juridisch_b.html` (template variant B — redesign)**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | Arbeidsrecht Updates</title>
    <style>
      * { box-sizing: border-box; }
      body { font-family: "Segoe UI", Tahoma, sans-serif; margin: 0; background: #1e2a3a; color: #eee; }
      header { background: #2c3e50; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; }
      header h1 { margin: 0; font-size: 1.4em; color: #f1c40f; }
      nav a { color: #aaa; margin-left: 20px; text-decoration: none; font-size: 0.85em; }
      main { max-width: 900px; margin: 30px auto; padding: 0 20px; }
      .card { background: #2c3e50; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
      .card h2 { color: #f1c40f; margin-top: 0; }
      .artikel-lijst a { display: block; padding: 6px 0; border-bottom: 1px solid #3d5166; color: #7fb3d3; }
      footer { text-align: center; padding: 20px; font-size: 0.75em; color: #555; }
    </style>
  </head>
  <body>
    <header>
      <h1>Arbeidsrecht Updates</h1>
      <nav><a href="#">Jurisprudentie</a> <a href="#">Wetgeving</a> <a href="#">CAO-recht</a></nav>
    </header>
    <main>
      <div class="card">
        <h2>{{TITLE}}</h2>
        {{BODY}}
        <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
      </div>
    </main>
    <footer>&copy; {{FOOTER_YEAR}} Arbeidsrecht Updates</footer>
  </body>
  </html>
  ```

- [ ] **Stap 8: Maak `generator/templates/nieuws.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>{{TITLE}} | Loondienst Nieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 920px; margin: 0 auto; padding: 0; }
      header { background: #e8380d; color: white; padding: 12px 20px; }
      header h1 { margin: 0; font-size: 1.5em; }
      .cookiebanner { background: #333; color: #eee; padding: 10px 20px; font-size: 0.85em; display: flex; justify-content: space-between; align-items: center; }
      .cookiebanner button { background: #e8380d; color: white; border: none; padding: 5px 12px; cursor: pointer; border-radius: 3px; }
      nav { background: #f5f5f5; padding: 8px 20px; border-bottom: 1px solid #ddd; }
      nav a { color: #333; margin-right: 15px; font-size: 0.9em; text-decoration: none; }
      main { padding: 20px; }
      .artikel-lijst a { display: block; padding: 8px 0; border-bottom: 1px solid #eee; color: #e8380d; }
      footer { background: #222; color: #888; font-size: 0.8em; padding: 15px 20px; margin-top: 20px; }
    </style>
  </head>
  <body>
    {{COOKIEBANNER}}
    <header><h1>Loondienst Nieuws</h1></header>
    <nav><a href="#">Nieuws</a> <a href="#">Cao</a> <a href="#">Salaris</a> <a href="#">Werken</a></nav>
    <main>
      <h2>{{TITLE}}</h2>
      {{BODY}}
      <div class="artikel-lijst">{{ARTICLES_LIST}}</div>
    </main>
    <footer>&copy; {{FOOTER_YEAR}} Loondienst Nieuws</footer>
  </body>
  </html>
  ```

- [ ] **Stap 9: Commit**

  ```bash
  git add generator/templates/
  git commit -m "feat: add html templates for all 7 site styles"
  ```

---

### Task 8: Initiële index.html per site aanmaken

**Files:**
- Modify: `sites/vakbond-nieuws/index.html`
- Modify: `sites/overheid-arbeidsmarkt/index.html`
- Modify: `sites/hr-magazine/index.html`
- Modify: `sites/sector-zorg/index.html`
- Modify: `sites/werkgevers-platform/index.html`
- Modify: `sites/arbeidsrecht-updates/index.html`
- Modify: `sites/loondienst-nieuws/index.html`

- [ ] **Stap 1: Maak `sites/vakbond-nieuws/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nieuws | VakbondNieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f4f4f4; }
      header { background: #c00; color: white; padding: 15px 20px; }
      header h1 { margin: 0; font-size: 1.6em; }
      nav a { color: white; margin-right: 15px; text-decoration: none; font-size: 0.9em; }
      main { background: white; padding: 20px; margin-top: 10px; }
      .artikel-lijst a { display: block; padding: 8px 0; border-bottom: 1px solid #eee; color: #c00; }
      footer { font-size: 0.8em; color: #666; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ccc; }
    </style>
  </head>
  <body>
    <header>
      <h1>VakbondNieuws</h1>
      <nav><a href="../../">Home</a> <a href="#">CAO</a> <a href="#">Leden</a> <a href="#">Contact</a></nav>
    </header>
    <main>
      <h2>Laatste nieuws</h2>
      <p>Deze pagina wordt dagelijks bijgewerkt met het laatste nieuws over arbeidsvoorwaarden en CAO's.</p>
      <div class="artikel-lijst">
        <!-- Artikelen worden hier automatisch toegevoegd -->
      </div>
    </main>
    <footer><p>&copy; 2026 VakbondNieuws. Alle rechten voorbehouden.</p></footer>
  </body>
  </html>
  ```

- [ ] **Stap 2: Maak `sites/overheid-arbeidsmarkt/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Arbeidsmarkt nieuws | Overheid.nl</title>
    <style>
      body { font-family: "Rijksoverheid Serif", Georgia, serif; max-width: 960px; margin: 0 auto; padding: 0; background: white; }
      header { background: #154273; color: white; padding: 12px 20px; }
      header h1 { margin: 0; font-size: 1.3em; font-weight: normal; }
      .lint { height: 4px; background: linear-gradient(to right, #AE1C28 33%, white 33%, white 66%, #21468B 66%); }
      nav { background: #f0f0f0; padding: 8px 20px; }
      nav a { color: #154273; margin-right: 20px; text-decoration: none; font-size: 0.9em; }
      main { padding: 20px; }
      .artikel-lijst a { display: block; padding: 6px 0; border-bottom: 1px solid #ddd; color: #154273; }
      footer { background: #154273; color: #ccc; font-size: 0.8em; padding: 15px 20px; margin-top: 30px; }
    </style>
  </head>
  <body>
    <div class="lint"></div>
    <header><h1>Overheid.nl | Arbeidsmarkt</h1></header>
    <nav><a href="../../">Home</a> <a href="#">Arbeidsmarkt</a> <a href="#">CAO-register</a> <a href="#">Contact</a></nav>
    <main>
      <h1>Nieuws arbeidsmarkt</h1>
      <p>Actuele berichten over arbeidsmarktbeleid, CAO-onderhandelingen en werkgelegenheid.</p>
      <div class="artikel-lijst">
        <!-- Artikelen worden hier automatisch toegevoegd -->
      </div>
    </main>
    <footer>&copy; 2026 Rijksoverheid</footer>
  </body>
  </html>
  ```

- [ ] **Stap 3: Maak `sites/hr-magazine/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Nieuws | HR Magazine</title>
    <style>
      body { font-family: "Helvetica Neue", Helvetica, sans-serif; max-width: 880px; margin: 0 auto; padding: 20px; }
      header { border-bottom: 3px solid #2d6a9f; padding-bottom: 10px; margin-bottom: 20px; }
      header h1 { color: #2d6a9f; font-size: 2em; margin: 0; }
      .artikel-lijst a { display: block; padding: 10px 0; border-bottom: 1px solid #eee; color: #2d6a9f; font-weight: bold; }
      footer { margin-top: 40px; font-size: 0.75em; color: #aaa; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
  </head>
  <body>
    <header><h1>HR Magazine</h1><span>Voor HR-professionals</span></header>
    <main>
      <h2>Recente artikelen</h2>
      <div class="artikel-lijst">
        <!-- Artikelen worden hier automatisch toegevoegd -->
      </div>
    </main>
    <footer>&copy; 2026 HR Magazine Nederland</footer>
  </body>
  </html>
  ```

- [ ] **Stap 4: Maak `sites/sector-zorg/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Documenten | Zorg & Welzijn Nieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
      header { background: #00857c; color: white; padding: 15px 20px; border-radius: 4px 4px 0 0; }
      header h1 { margin: 0; }
      main { background: white; padding: 20px; border: 1px solid #ddd; }
      .pdf-sectie { margin-top: 20px; padding: 15px; background: #f0faf9; border-left: 4px solid #00857c; }
      .pdf-sectie a { color: #00857c; display: block; margin: 5px 0; }
      details { margin-top: 30px; padding: 10px; background: #fafafa; border: 1px solid #eee; }
      details summary { cursor: pointer; color: #666; font-size: 0.9em; }
      footer { font-size: 0.8em; color: #888; margin-top: 15px; }
    </style>
  </head>
  <body>
    <header><h1>Zorg &amp; Welzijn Nieuws</h1></header>
    <main>
      <h2>CAO-documenten</h2>
      <p>Hier vindt u de actuele CAO-documenten voor de zorg- en welzijnssector.</p>
      <div class="pdf-sectie">
        <strong>Recente documenten:</strong>
        <!-- PDF-links worden hier automatisch toegevoegd -->
      </div>
      <details>
        <summary>Archief en aanvullende documenten</summary>
        <div id="archief">
          <!-- Verborgen PDF-links worden hier geplaatst -->
        </div>
      </details>
    </main>
    <footer>&copy; 2026 Zorg &amp; Welzijn Nieuws</footer>
  </body>
  </html>
  ```

- [ ] **Stap 5: Maak `sites/werkgevers-platform/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Documenten | Werkgevers Platform NL</title>
    <style>
      body { font-family: "Trebuchet MS", sans-serif; max-width: 920px; margin: 0 auto; padding: 20px; }
      header { background: #1a3c5e; color: white; padding: 15px 25px; }
      header h1 { margin: 0; font-size: 1.5em; }
      nav a { color: #ccc; margin-right: 15px; text-decoration: none; font-size: 0.85em; }
      .documenten { margin-top: 20px; background: #f5f8fb; padding: 15px; border: 1px solid #d0dce8; }
      .documenten a { color: #1a3c5e; display: block; padding: 4px 0; }
      footer { font-size: 0.8em; color: #777; border-top: 1px solid #ddd; margin-top: 30px; padding-top: 10px; }
    </style>
  </head>
  <body>
    <header>
      <h1>Werkgevers Platform NL</h1>
      <nav><a href="../../">Home</a> <a href="#">CAO-tools</a> <a href="#">Documenten</a></nav>
    </header>
    <div class="documenten">
      <strong>CAO-documenten:</strong>
      <!-- PDF-links worden hier automatisch toegevoegd -->
    </div>
    <footer>&copy; 2026 Werkgevers Platform NL</footer>
  </body>
  </html>
  ```

- [ ] **Stap 6: Maak `sites/arbeidsrecht-updates/index.html`** (gebruik juridisch_a stijl)

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Nieuws | Arbeidsrecht Updates</title>
    <style>
      body { font-family: Georgia, serif; max-width: 860px; margin: 0 auto; padding: 20px; background: white; }
      header { border-bottom: 2px solid #333; padding-bottom: 10px; }
      header h1 { font-size: 1.8em; color: #333; }
      nav a { color: #555; margin-right: 20px; font-size: 0.9em; }
      .artikel-lijst a { display: block; padding: 5px 0; border-bottom: 1px dotted #ccc; color: #333; }
      footer { margin-top: 40px; font-size: 0.75em; color: #999; border-top: 1px solid #ddd; padding-top: 8px; }
    </style>
  </head>
  <body>
    <header>
      <h1>Arbeidsrecht Updates</h1>
      <nav><a href="../../">Home</a> <a href="#">Jurisprudentie</a> <a href="#">Wetgeving</a> <a href="#">CAO-recht</a></nav>
    </header>
    <article>
      <h2>Recente updates</h2>
      <p>Actuele informatie over arbeidsrecht, CAO-regelgeving en jurisprudentie.</p>
      <div class="artikel-lijst">
        <!-- Artikelen worden hier automatisch toegevoegd -->
      </div>
    </article>
    <footer>&copy; 2026 Arbeidsrecht Updates. Alle informatie onder voorbehoud.</footer>
  </body>
  </html>
  ```

- [ ] **Stap 7: Maak `sites/loondienst-nieuws/index.html`**

  ```html
  <!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    <title>Nieuws | Loondienst Nieuws</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 920px; margin: 0 auto; padding: 0; }
      header { background: #e8380d; color: white; padding: 12px 20px; }
      header h1 { margin: 0; font-size: 1.5em; }
      .cookiebanner { background: #333; color: #eee; padding: 10px 20px; font-size: 0.85em; display: flex; justify-content: space-between; align-items: center; }
      .cookiebanner button { background: #e8380d; color: white; border: none; padding: 5px 12px; cursor: pointer; border-radius: 3px; }
      nav { background: #f5f5f5; padding: 8px 20px; border-bottom: 1px solid #ddd; }
      nav a { color: #333; margin-right: 15px; font-size: 0.9em; text-decoration: none; }
      main { padding: 20px; }
      .artikel-lijst a { display: block; padding: 8px 0; border-bottom: 1px solid #eee; color: #e8380d; }
      footer { background: #222; color: #888; font-size: 0.8em; padding: 15px 20px; margin-top: 20px; }
    </style>
  </head>
  <body>
    <div class="cookiebanner">
      <span>Wij gebruiken cookies voor een optimale gebruikerservaring.</span>
      <button onclick="this.parentElement.style.display='none'">Accepteren</button>
    </div>
    <header><h1>Loondienst Nieuws</h1></header>
    <nav><a href="../../">Home</a> <a href="#">Nieuws</a> <a href="#">Cao</a> <a href="#">Salaris</a></nav>
    <main>
      <h2>Laatste nieuws</h2>
      <div class="artikel-lijst">
        <!-- Artikelen worden hier automatisch toegevoegd -->
      </div>
    </main>
    <footer>&copy; 2026 Loondienst Nieuws</footer>
  </body>
  </html>
  ```

- [ ] **Stap 8: Commit**

  ```bash
  git add sites/
  git commit -m "feat: add initial index pages for all 7 sites"
  git push
  ```

---

## Chunk 3: Generator (generate.py)

### Task 9: Python-omgeving en Anthropic SDK installen

**Files:** geen

- [ ] **Stap 1: Controleer Python-versie**

  ```bash
  python --version
  ```
  Verwacht: `Python 3.11.x` of hoger. Als niet aanwezig, download van https://python.org.

- [ ] **Stap 2: Installeer de Anthropic Python SDK**

  ```bash
  pip install anthropic
  ```

- [ ] **Stap 3: Maak een tijdelijk `.env`-bestand aan voor lokaal testen**

  Maak `generator/.env` aan (staat al in .gitignore):
  ```
  ANTHROPIC_API_KEY=sk-ant-...jouw-key-hier...
  ```

  Je API key vind je op https://console.anthropic.com/settings/keys.

---

### Task 10: generate.py — hulpfuncties en config laden

**Files:**
- Create: `generator/generate.py`

- [ ] **Stap 1: Schrijf de basis van generate.py**

  Maak `generator/generate.py` aan:

  ```python
  #!/usr/bin/env python3
  """Dagelijkse content generator voor CAO monitor testwebsites."""

  import json
  import os
  import random
  import shutil
  import sys
  from datetime import date, timedelta
  from pathlib import Path

  import anthropic

  # Paden relatief aan de repo-root
  REPO_ROOT = Path(__file__).parent.parent
  GENERATOR_DIR = Path(__file__).parent
  SITES_DIR = REPO_ROOT / "sites"
  SITES_CONFIG = GENERATOR_DIR / "sites.json"
  STATE_FILE = GENERATOR_DIR / "state.json"
  ARCHIVE_DIR = GENERATOR_DIR / "archive"

  client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
  today = date.today()
  day_of_year = today.timetuple().tm_yday


  def load_config() -> dict:
      return json.loads(SITES_CONFIG.read_text(encoding="utf-8"))


  def load_state() -> dict:
      if STATE_FILE.exists():
          return json.loads(STATE_FILE.read_text(encoding="utf-8"))
      return {}


  def save_state(state: dict) -> None:
      STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


  def get_active_edge_case(site_config: dict) -> str:
      edge_cases = site_config["edge_cases"]
      return edge_cases[day_of_year % len(edge_cases)]


  def should_be_relevant(site_config: dict) -> bool:
      return random.random() < site_config.get("relevantie_kans", 0.0)


  def call_claude(prompt: str) -> str:
      """Roep Claude API aan en geef de tekst terug."""
      message = client.messages.create(
          model="claude-haiku-4-5-20251001",
          max_tokens=1024,
          messages=[{"role": "user", "content": prompt}],
      )
      return message.content[0].text.strip()


  def slugify(text: str) -> str:
      """Maak een URL-veilige slug van een tekst."""
      import re
      text = text.lower()
      text = re.sub(r"[àáâãäå]", "a", text)
      text = re.sub(r"[èéêë]", "e", text)
      text = re.sub(r"[ìíîï]", "i", text)
      text = re.sub(r"[òóôõö]", "o", text)
      text = re.sub(r"[ùúûü]", "u", text)
      text = re.sub(r"[^a-z0-9]+", "-", text)
      return text.strip("-")[:60]


  def make_article_filename(title: str, pub_date: date = None) -> str:
      d = pub_date or today
      return f"{d.isoformat()}-{slugify(title)}.html"


  def render_article_html(title: str, body: str, pub_date: date = None,
                          noindex: bool = False, site_style: str = "default") -> str:
      d = pub_date or today
      noindex_tag = '<meta name="robots" content="noindex">' if noindex else ""
      return f"""<!DOCTYPE html>
  <html lang="nl">
  <head>
    <meta charset="UTF-8">
    {noindex_tag}
    <title>{title}</title>
    <style>
      body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
      .meta {{ color: #666; font-size: 0.9em; }}
      a.back {{ color: #333; }}
    </style>
  </head>
  <body>
    <p><a class="back" href="../">&larr; Terug</a></p>
    <h1>{title}</h1>
    <p class="meta"><time datetime="{d.isoformat()}">{d.strftime("%d %B %Y")}</time></p>
    {body}
  </body>
  </html>"""


  def add_article_link_to_index(index_path: Path, href: str, title: str) -> None:
      """Voeg een artikellink toe aan de index.html van een site."""
      content = index_path.read_text(encoding="utf-8")
      link = f'<a href="{href}">{title}</a>\n        '
      content = content.replace(
          "<!-- Artikelen worden hier automatisch toegevoegd -->",
          f'{link}<!-- Artikelen worden hier automatisch toegevoegd -->'
      )
      index_path.write_text(content, encoding="utf-8")
  ```

- [ ] **Stap 2: Verifieer dat het bestand syntactisch correct is**

  ```bash
  cd "C:/Users/vansc/Documents/Test websites"
  python -c "import generator.generate; print('OK')"
  ```
  Verwacht: `OK`

---

### Task 11: generate.py — artikel-sites logica

**Files:**
- Modify: `generator/generate.py`

- [ ] **Stap 1: Voeg functie toe voor artikel-sites**

  Voeg onderaan `generate.py` toe:

  ```python
  def generate_artikel_site(site_name: str, site_config: dict, state: dict) -> None:
      """Verwerk een artikel-type site."""
      site_dir = SITES_DIR / site_name
      artikelen_dir = site_dir / "artikelen"
      artikelen_dir.mkdir(parents=True, exist_ok=True)
      archive_dir = ARCHIVE_DIR / site_name
      archive_dir.mkdir(parents=True, exist_ok=True)
      index_path = site_dir / "index.html"
      edge_case = get_active_edge_case(site_config)
      relevant = should_be_relevant(site_config)
      site_state = state.get(site_name, {})

      # --- artikel_verdwijnt: Fase 2 check (verwijder artikel van gisteren) ---
      gisteren_str = (today - timedelta(days=1)).isoformat()
      if site_state.get("verdwenen_slug") and site_state.get("dag") == gisteren_str:
          bestand = artikelen_dir / site_state["verdwenen_slug"]
          if bestand.exists():
              bestand.unlink()
              print(f"  [artikel_verdwijnt] Verwijderd: {bestand.name}")
          else:
              print(f"  [artikel_verdwijnt] WAARSCHUWING: bestand al verdwenen: {bestand.name}")
          site_state["verdwenen_slug"] = None
          site_state["dag"] = None
          state[site_name] = site_state
          return  # Geen nieuwe content op verwijderdag

      # --- Genereer normale artikelen (2-3 irrelevant + evt. 1 relevant) ---
      onderwerpen_onzin = [
          "recepten voor een gezonde lunch op het werk",
          "tips voor thuiswerken in de zomer",
          "nieuwe kantoorinrichting trends",
          "cacao-productie stijgt wereldwijd",
          "fietsvergoeding voor werknemers",
          "vergaderruimtes van de toekomst",
          "koffiepauze cultuur in Nederland",
      ]

      for _ in range(2):
          onderwerp = random.choice(onderwerpen_onzin)
          prompt = (
              f"Schrijf een kort nieuwsartikel (3-4 alinea's) in het Nederlands over: {onderwerp}. "
              f"Schrijf alleen de HTML-paragrafen (alleen <p>-tags, geen <html> of <body>). "
              f"Maak het realistisch maar volledig nep."
          )
          body = call_claude(prompt)
          title = onderwerp.capitalize()
          filename = make_article_filename(title)
          html = render_article_html(title, body)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          (archive_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"  Artikel (onzin): {filename}")

      if relevant:
          cao_prompt = (
              "Schrijf een kort nieuwsartikel (3-4 alinea's) in het Nederlands over een recente "
              "ontwikkeling in een Nederlandse CAO-onderhandeling. Noem een specifieke sector "
              "(bijv. metaal, zorg, onderwijs). Schrijf alleen <p>-tags."
          )
          body = call_claude(cao_prompt)
          title = "CAO-update: nieuwe afspraken in zicht"
          filename = make_article_filename(title)
          html = render_article_html(title, body)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          (archive_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"  Artikel (relevant): {filename}")

      # --- Edge case ---
      print(f"  Edge case: {edge_case}")

      if edge_case == "korte_slug":
          body = "<p>Dit is een kort artikel met een korte URL-slug, wat de monitor kan missen.</p>"
          html = render_article_html("CAO 2026", body)
          (artikelen_dir / "cao-2026.html").write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, "artikelen/cao-2026.html", "CAO 2026")
          print("    -> Kort slug: artikelen/cao-2026.html")

      elif edge_case == "anker_url":
          body = "<p>Dit artikel heeft een anker in de URL, wat de monitor mogelijk anders behandelt.</p>"
          html = render_article_html("CAO update: nieuwe afspraken #arbeidsmarkt", body)
          filename = make_article_filename("cao-update-anker")
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(
              index_path, f"artikelen/{filename}#arbeidsmarkt",
              "CAO update: nieuwe afspraken #arbeidsmarkt"
          )
          print(f"    -> Anker URL: artikelen/{filename}#arbeidsmarkt")

      elif edge_case == "cacao_false_positive":
          prompt = (
              "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over de wereldwijde "
              "cacaoproductie en chocolade-industrie. Noem het woord 'cacao' meerdere keren. "
              "Schrijf alleen <p>-tags."
          )
          body = call_claude(prompt)
          title = "Cacao-productie bereikt recordhoogte in 2026"
          filename = make_article_filename(title)
          html = render_article_html(title, body)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"    -> Cacao false positive: {filename}")

      elif edge_case == "pagina_url":
          # Maak een paginerings-URL die op een artikel lijkt
          body = "<p>Dit is een overzichtspagina, geen artikel.</p>"
          html = render_article_html("Pagina 3 - Nieuwsoverzicht", body)
          pagina_path = site_dir / "pagina" / "3"
          pagina_path.mkdir(parents=True, exist_ok=True)
          (pagina_path / "index.html").write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, "pagina/3/", "Nieuwsoverzicht - Pagina 3")
          print("    -> Paginering URL: pagina/3/")

      elif edge_case == "relevant_zonder_cao_woord":
          prompt = (
              "Schrijf een kort nieuwsartikel (3 alinea's) in het Nederlands over een loonsverhoging "
              "van 5% voor werknemers in een specifieke sector. Vermijd het woord 'CAO' volledig. "
              "Schrijf alleen <p>-tags."
          )
          body = call_claude(prompt)
          title = "Werknemers krijgen 5 procent loonsverhoging"
          filename = make_article_filename(title)
          html = render_article_html(title, body)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"    -> Relevant zonder CAO-woord: {filename}")

      elif edge_case == "noindex_tag":
          prompt = (
              "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over een nieuwe "
              "CAO-afspraak. Schrijf alleen <p>-tags."
          )
          body = call_claude(prompt)
          title = "Nieuwe CAO-afspraak — noindex test"
          filename = make_article_filename(title)
          html = render_article_html(title, body, noindex=True)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"    -> Noindex artikel: {filename}")

      elif edge_case == "teruggedateerd":
          days_back = random.randint(30, 90)
          pub_date = today - timedelta(days=days_back)
          prompt = (
              "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over een CAO-update. "
              "Schrijf alleen <p>-tags."
          )
          body = call_claude(prompt)
          title = "CAO-update: teruggedateerd artikel"
          filename = make_article_filename(title, pub_date=pub_date)
          html = render_article_html(title, body, pub_date=pub_date)
          (artikelen_dir / filename).write_text(html, encoding="utf-8")
          add_article_link_to_index(index_path, f"artikelen/{filename}", title)
          print(f"    -> Teruggedateerd ({pub_date}): {filename}")

      elif edge_case == "oud_nieuws_herplaatst":
          bestanden = list(archive_dir.glob("*.html"))
          if bestanden:
              bron = random.choice(bestanden)
              originele_slug = bron.stem
              # Verwijder datum prefix (YYYY-MM-DD-) als die aanwezig is
              import re
              clean_slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", originele_slug)
              nieuwe_naam = f"{today.isoformat()}-{clean_slug}.html"
              shutil.copy(bron, artikelen_dir / nieuwe_naam)
              add_article_link_to_index(index_path, f"artikelen/{nieuwe_naam}", f"(herplaatst) {clean_slug}")
              print(f"    -> Oud nieuws herplaatst: {nieuwe_naam}")
          else:
              # Archief leeg: genereer een nieuw artikel als fallback
              prompt = "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over HR-nieuws. Schrijf alleen <p>-tags."
              body = call_claude(prompt)
              title = "HR-nieuws: nieuw artikel"
              filename = make_article_filename(title)
              html = render_article_html(title, body)
              (artikelen_dir / filename).write_text(html, encoding="utf-8")
              (archive_dir / filename).write_text(html, encoding="utf-8")
              add_article_link_to_index(index_path, f"artikelen/{filename}", title)
              print(f"    -> oud_nieuws_herplaatst: archief leeg, nieuw artikel gegenereerd: {filename}")

      elif edge_case == "artikel_verdwijnt":
          if not site_state.get("verdwenen_slug"):  # Fase 1
              prompt = (
                  "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over een CAO. "
                  "Schrijf alleen <p>-tags."
              )
              body = call_claude(prompt)
              title = "Tijdelijk artikel — verdwijnt morgen"
              filename = make_article_filename(title)
              html = render_article_html(title, body)
              (artikelen_dir / filename).write_text(html, encoding="utf-8")
              add_article_link_to_index(index_path, f"artikelen/{filename}", title)
              site_state["verdwenen_slug"] = filename
              site_state["dag"] = today.isoformat()
              state[site_name] = site_state
              print(f"    -> Artikel_verdwijnt Fase 1: {filename}")
  ```

- [ ] **Stap 2: Verifieer syntax**

  ```bash
  python -c "import ast; ast.parse(open('generator/generate.py').read()); print('OK')"
  ```
  Verwacht: `OK`

---

### Task 12: generate.py — PDF-sites logica

**Files:**
- Modify: `generator/generate.py`

- [ ] **Stap 1: Voeg functie toe voor PDF-sites**

  Voeg onderaan `generate.py` toe:

  ```python
  def generate_pdf_site(site_name: str, site_config: dict, state: dict) -> None:
      """Verwerk een PDF-type site."""
      site_dir = SITES_DIR / site_name
      docs_dir = site_dir / "docs"
      docs_dir.mkdir(parents=True, exist_ok=True)
      index_path = site_dir / "index.html"
      edge_case = get_active_edge_case(site_config)
      print(f"  Edge case: {edge_case}")

      if edge_case == "zelfde_url_nieuwe_inhoud":
          # Genereer content, schrijf naar altijd dezelfde URL
          prompt = (
              "Schrijf een kort stuk nep-CAO-tekst (3-4 regels) voor de zorgsector, in het Nederlands. "
              "Vermeld de huidige datum in de tekst."
          )
          content = call_claude(prompt)
          pdf_path = docs_dir / "cao-zorg-actueel.pdf"
          pdf_path.write_text(
              f"CAO Zorg & Welzijn — Actuele versie\nDatum: {today.isoformat()}\n\n{content}",
              encoding="utf-8"
          )
          # Update index alleen als link er nog niet in staat
          index_content = index_path.read_text(encoding="utf-8")
          if "cao-zorg-actueel.pdf" not in index_content:
              link = '<a href="docs/cao-zorg-actueel.pdf">CAO Zorg &amp; Welzijn (actueel)</a>\n        '
              index_content = index_content.replace(
                  "<!-- PDF-links worden hier automatisch toegevoegd -->",
                  f'{link}<!-- PDF-links worden hier automatisch toegevoegd -->'
              )
              index_path.write_text(index_content, encoding="utf-8")
          print(f"    -> Vaste URL bijgewerkt: docs/cao-zorg-actueel.pdf")

      elif edge_case == "diep_verstopt":
          filename = f"cao-aanvullend-{today.isoformat()}.pdf"
          prompt = "Schrijf 2 regels nep-CAO-tekst in het Nederlands."
          content = call_claude(prompt)
          pdf_path = docs_dir / filename
          pdf_path.write_text(f"Aanvullend CAO-document\nDatum: {today.isoformat()}\n\n{content}", encoding="utf-8")
          # Voeg toe in <details> archief-sectie (diep verstopt)
          index_content = index_path.read_text(encoding="utf-8")
          link = f'<a href="docs/{filename}">Aanvullend document {today.isoformat()}</a>\n          '
          index_content = index_content.replace(
              "<!-- Verborgen PDF-links worden hier geplaatst -->",
              f'{link}<!-- Verborgen PDF-links worden hier geplaatst -->'
          )
          index_path.write_text(index_content, encoding="utf-8")
          print(f"    -> Diep verstopt in <details>: docs/{filename}")

      elif edge_case == "korte_pdf_naam":
          prompt = "Schrijf 2 regels nep-CAO-tekst voor werkgevers in het Nederlands."
          content = call_claude(prompt)
          pdf_path = docs_dir / "cao.pdf"
          pdf_path.write_text(f"CAO Document\nDatum: {today.isoformat()}\n\n{content}", encoding="utf-8")
          index_content = index_path.read_text(encoding="utf-8")
          if "cao.pdf" not in index_content:
              link = '<a href="docs/cao.pdf">CAO (huidig)</a>\n        '
              index_content = index_content.replace(
                  "<!-- PDF-links worden hier automatisch toegevoegd -->",
                  f'{link}<!-- PDF-links worden hier automatisch toegevoegd -->'
              )
              index_path.write_text(index_content, encoding="utf-8")
          print(f"    -> Korte PDF-naam: docs/cao.pdf")

      elif edge_case == "pdf_verdwijnt_nieuwe_naam":
          # Verwijder gisteren's bestand en maak een nieuw aan
          gisteren = (today - timedelta(days=1)).isoformat()
          oud_bestand = docs_dir / f"cao-werkgevers-{gisteren}.pdf"
          if oud_bestand.exists():
              oud_bestand.unlink()
              print(f"    -> Verwijderd: {oud_bestand.name}")
          filename = f"cao-werkgevers-{today.isoformat()}.pdf"
          prompt = "Schrijf 2 regels nep-CAO-tekst voor werkgevers in het Nederlands."
          content = call_claude(prompt)
          (docs_dir / filename).write_text(f"CAO Werkgevers\nDatum: {today.isoformat()}\n\n{content}", encoding="utf-8")
          link = f'<a href="docs/{filename}">CAO Werkgevers {today.isoformat()}</a>\n        '
          index_content = index_path.read_text(encoding="utf-8")
          index_content = index_content.replace(
              "<!-- PDF-links worden hier automatisch toegevoegd -->",
              f'{link}<!-- PDF-links worden hier automatisch toegevoegd -->'
          )
          index_path.write_text(index_content, encoding="utf-8")
          print(f"    -> Nieuwe naam: docs/{filename}")
  ```

- [ ] **Stap 2: Verifieer syntax**

  ```bash
  python -c "import ast; ast.parse(open('generator/generate.py').read()); print('OK')"
  ```

---

### Task 13: generate.py — pagina-wijziging-sites logica

**Files:**
- Modify: `generator/generate.py`

- [ ] **Stap 1: Voeg functie toe voor pagina-wijziging-sites**

  Voeg onderaan `generate.py` toe:

  ```python
  def generate_pagina_site(site_name: str, site_config: dict, state: dict) -> None:
      """Verwerk een pagina-wijziging-type site."""
      site_dir = SITES_DIR / site_name
      index_path = site_dir / "index.html"
      edge_case = get_active_edge_case(site_config)
      site_state = state.get(site_name, {})
      print(f"  Edge case: {edge_case}")

      if site_name == "arbeidsrecht-updates":
          actieve_template = site_state.get("actieve_template", "a")

          if edge_case == "grote_redesign":
              nieuwe_variant = "b" if actieve_template == "a" else "a"
              template_path = GENERATOR_DIR / "templates" / f"juridisch_{nieuwe_variant}.html"
              template = template_path.read_text(encoding="utf-8")
              html = (template
                      .replace("{{TITLE}}", "Actuele arbeidsrecht updates")
                      .replace("{{BODY}}", "<p>Recente ontwikkelingen in het arbeidsrecht en CAO-regelgeving.</p>")
                      .replace("{{ARTICLES_LIST}}", "<!-- Artikelen worden hier automatisch toegevoegd -->")
                      .replace("{{FOOTER_YEAR}}", str(today.year)))
              index_path.write_text(html, encoding="utf-8")
              site_state["actieve_template"] = nieuwe_variant
              state[site_name] = site_state
              print(f"    -> Grote redesign: van {actieve_template} naar {nieuwe_variant}")

          elif edge_case == "alleen_footer":
              content = index_path.read_text(encoding="utf-8")
              import re
              content = re.sub(
                  r"&copy; \d{4} Arbeidsrecht",
                  f"&copy; {today.year} Arbeidsrecht",
                  content
              )
              index_path.write_text(content, encoding="utf-8")
              print(f"    -> Alleen footer: jaar bijgewerkt naar {today.year}")

          elif edge_case == "typofout":
              content = index_path.read_text(encoding="utf-8")
              # Kleine wijziging: voeg een spatie toe en verwijder die morgen
              if "  jurisprudentie  " not in content:
                  content = content.replace("Jurisprudentie", "Jurisprudenti e", 1)
              else:
                  content = content.replace("Jurisprudenti e", "Jurisprudentie", 1)
              index_path.write_text(content, encoding="utf-8")
              print("    -> Typofout ingevoerd/hersteld")

      elif site_name == "loondienst-nieuws":
          if edge_case == "cookiebanner_wissel":
              content = index_path.read_text(encoding="utf-8")
              # Wissel cookiebanner tekst
              if "optimale gebruikerservaring" in content:
                  content = content.replace(
                      "Wij gebruiken cookies voor een optimale gebruikerservaring.",
                      "Door verder te gaan accepteert u ons cookiebeleid en privacyverklaring."
                  )
              else:
                  content = content.replace(
                      "Door verder te gaan accepteert u ons cookiebeleid en privacyverklaring.",
                      "Wij gebruiken cookies voor een optimale gebruikerservaring."
                  )
              index_path.write_text(content, encoding="utf-8")
              print("    -> Cookiebanner tekst gewisseld")

          elif edge_case == "content_zonder_url":
              content = index_path.read_text(encoding="utf-8")
              # Voeg een alinea toe zonder nieuwe URL
              if "<!-- content update -->" not in content:
                  content = content.replace(
                      "<h2>Laatste nieuws</h2>",
                      f"<h2>Laatste nieuws</h2>\n      <!-- content update -->\n      <p><em>Bijgewerkt op {today.isoformat()}: redactionele aanpassing.</em></p>"
                  )
              else:
                  content = content.replace(
                      f"<em>Bijgewerkt op",
                      f"<em>Bijgewerkt op {today.isoformat()}:"
                  )
              index_path.write_text(content, encoding="utf-8")
              print("    -> Content update zonder URL-wijziging")
  ```

- [ ] **Stap 2: Verifieer syntax**

  ```bash
  python -c "import ast; ast.parse(open('generator/generate.py').read()); print('OK')"
  ```

---

### Task 14: generate.py — main-functie en run

**Files:**
- Modify: `generator/generate.py`

- [ ] **Stap 1: Voeg de main-functie toe**

  Voeg onderaan `generate.py` toe:

  ```python
  def main() -> None:
      print(f"=== Generator draait voor {today.isoformat()} (dag {day_of_year}) ===\n")
      config = load_config()
      state = load_state()
      fouten = []

      for site_name, site_config in config.items():
          print(f"--- {site_name} ({site_config['type']}) ---")
          try:
              if site_config["type"] == "artikel":
                  generate_artikel_site(site_name, site_config, state)
              elif site_config["type"] == "pdf":
                  generate_pdf_site(site_name, site_config, state)
              elif site_config["type"] == "pagina":
                  generate_pagina_site(site_name, site_config, state)
              else:
                  print(f"  ONBEKEND TYPE: {site_config['type']}")
          except Exception as e:
              print(f"  FOUT bij {site_name}: {e}", file=sys.stderr)
              fouten.append(site_name)
          print()

      save_state(state)
      print(f"State opgeslagen naar {STATE_FILE}")

      if fouten:
          print(f"\nFOUTEN bij: {', '.join(fouten)}", file=sys.stderr)
          # Niet falen — workflow gaat door


  if __name__ == "__main__":
      main()
  ```

- [ ] **Stap 2: Test de generator lokaal (droog zonder API-calls)**

  Controleer syntax en importeren:
  ```bash
  cd "C:/Users/vansc/Documents/Test websites"
  python -c "import ast; ast.parse(open('generator/generate.py').read()); print('Syntax OK')"
  ```

- [ ] **Stap 3: Test de generator met echte API-call (één site)**

  Stel tijdelijk de ANTHROPIC_API_KEY in en run alleen voor één site:
  ```bash
  # Windows PowerShell:
  $env:ANTHROPIC_API_KEY = "sk-ant-...jouw-key..."
  cd "C:/Users/vansc/Documents/Test websites"
  python generator/generate.py
  ```

  Verwacht: output per site met "Artikel (onzin):" en "Edge case:" regels, en nieuwe bestanden in `sites/vakbond-nieuws/artikelen/`.

- [ ] **Stap 4: Verifieer dat er nieuwe bestanden zijn aangemaakt**

  ```bash
  ls sites/vakbond-nieuws/artikelen/
  ```
  Verwacht: één of meer `.html` bestanden met de datum van vandaag.

- [ ] **Stap 5: Commit**

  ```bash
  git add generator/generate.py generator/state.json
  git commit -m "feat: add content generator with edge case logic"
  git push
  ```

---

## Chunk 4: GitHub Actions workflow

### Task 15: GitHub Actions workflow aanmaken

**Files:**
- Create: `.github/workflows/generate-content.yml`

- [ ] **Stap 1: Maak de workflow aan**

  Inhoud van `.github/workflows/generate-content.yml`:

  ```yaml
  name: Genereer dagelijkse content

  on:
    schedule:
      - cron: "0 6 * * *"   # Dagelijks om 06:00 UTC
    workflow_dispatch:       # Handmatig triggeren mogelijk

  permissions:
    contents: write

  jobs:
    generate:
      runs-on: ubuntu-latest

      steps:
        - name: Checkout repo
          uses: actions/checkout@v4

        - name: Zet Python op
          uses: actions/setup-python@v5
          with:
            python-version: "3.11"

        - name: Installeer dependencies
          run: pip install anthropic

        - name: Genereer content
          env:
            ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          run: python generator/generate.py

        - name: Commit en push wijzigingen
          run: |
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add sites/ generator/state.json generator/archive/
            git diff --staged --quiet || git commit -m "chore: dagelijkse content update $(date -u +%Y-%m-%d)"
            git push
  ```

- [ ] **Stap 2: Commit de workflow**

  ```bash
  git add .github/workflows/generate-content.yml
  git commit -m "feat: add daily content generation workflow"
  git push
  ```

---

### Task 16: ANTHROPIC_API_KEY instellen als GitHub Secret

**Files:** geen

- [ ] **Stap 1: Ga naar de GitHub Secrets-pagina**

  Ga naar:
  `https://github.com/<gebruikersnaam>/cao-testwebsites/settings/secrets/actions`

- [ ] **Stap 2: Voeg het secret toe**

  - Klik "New repository secret"
  - Name: `ANTHROPIC_API_KEY`
  - Secret: jouw Anthropic API key (begint met `sk-ant-`)
  - Klik "Add secret"

---

### Task 17: Workflow handmatig testen

**Files:** geen

- [ ] **Stap 1: Trigger de workflow handmatig**

  Ga naar:
  `https://github.com/<gebruikersnaam>/cao-testwebsites/actions/workflows/generate-content.yml`

  Klik "Run workflow" → "Run workflow" (groen knop).

- [ ] **Stap 2: Bekijk de workflow-log**

  Klik op de lopende workflow-run. Je ziet per stap de output. Controleer:
  - Stap "Genereer content": output per site zonder FOUT-regels
  - Stap "Commit en push": een commit is aangemaakt

- [ ] **Stap 3: Verifieer de GitHub Pages-sites**

  Wacht ~2 minuten na de workflow-run en bezoek:
  - `https://<gebruikersnaam>.github.io/cao-testwebsites/`
  - `https://<gebruikersnaam>.github.io/cao-testwebsites/sites/vakbond-nieuws/`

  Je zou de gegenereerde artikellinks moeten zien.

- [ ] **Stap 4: Controleer dat de monitor-URLs bereikbaar zijn**

  Test met curl (of een browser) of de URL's die in `sites.json` staan bereikbaar zijn:
  ```bash
  curl -s "https://<gebruikersnaam>.github.io/cao-testwebsites/sites/vakbond-nieuws/" | head -30
  ```
  Verwacht: HTML-output met artikellinks.

---

## Chunk 5: sites.json URL's bijwerken

### Task 18: Echte GitHub Pages-URLs invullen in sites.json

**Files:**
- Modify: `generator/sites.json`

- [ ] **Stap 1: Vervang alle `<gebruikersnaam>` placeholders**

  Open `generator/sites.json` en vervang `<gebruikersnaam>` door jouw echte GitHub-gebruikersnaam in alle 7 `monitor_url` velden.

- [ ] **Stap 2: Commit**

  ```bash
  git add generator/sites.json
  git commit -m "chore: set real github pages urls in sites.json"
  git push
  ```

---

**Plan volledig. Zodra je klaar bent met uitvoeren staan 7 testwebsites live op GitHub Pages met dagelijkse content-generatie.**
