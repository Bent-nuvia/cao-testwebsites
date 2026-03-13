# Design: CAO Monitor Testwebsites

**Datum:** 2026-03-12
**Status:** Goedgekeurd

## Doel

Zeven statische testwebsites bouwen die de CAO-URL-monitor systematisch testen. Elke site simuleert een realistisch websitetype (vakbond, overheid, HR, etc.) en bevat bewuste edge cases om zwakke plekken in de monitor bloot te leggen. Content wordt dagelijks automatisch gegenereerd via de Claude API.

## Context

De monitor detecteert nieuwe content op websites door:
- Nieuwe URL-slugs te signaleren (artikelen)
- Nieuwe/gewijzigde PDF-links te detecteren
- Structuurwijzigingen op een pagina bij te houden

Per site is precies één van deze drie scan-modi actief.

## Site-indeling

### Artikel-sites (monitor: nieuwe URL-slugs)

| Site | Stijl | Primaire edge cases |
|---|---|---|
| `vakbond-nieuws` | FNV/CNV-stijl vakbondssite | Korte slugs (`/nieuws/cao-2026`), anker-URLs (`/nieuws/update#sectie-3`), "cacao" als false positive |
| `overheid-arbeidsmarkt` | Rijksoverheid-stijl | Paginering die op artikel lijkt (`/nieuws/pagina/3`), relevant nieuws zonder het woord "CAO" (bijv. "5% loonsverhoging"), noindex meta-tag op artikel |
| `hr-magazine` | HR-vakblad | Teruggedateerde artikelen, oud nieuws opnieuw gepubliceerd zonder aanpassing, artikel verschijnt en verdwijnt binnen 24 uur |

### PDF-sites (monitor: nieuwe/gewijzigde PDF-links)

| Site | Stijl | Primaire edge cases |
|---|---|---|
| `sector-zorg` | Zorgsector nieuwssite | Altijd dezelfde PDF-URL maar wisselende inhoud, PDF diep verstopt op pagina (niet in hoofdnavigatie) |
| `werkgevers-platform` | Werkgeversorganisatie | Korte PDF-namen (`/docs/cao.pdf`), PDF verdwijnt en komt terug met nieuwe bestandsnaam |

### Pagina-wijziging-sites (monitor: structuurwijzigingen)

| Site | Stijl | Primaire edge cases |
|---|---|---|
| `arbeidsrecht-updates` | Juridische informatiesite | Alleen footer verandert (copyright jaar), kleine typofout hersteld, grote redesign waarbij alle elementen wijzigen |
| `loondienst-nieuws` | Algemeen nieuwssite | Cookiebanner wisselt, content update zonder URL-wijziging |

## Technische architectuur

### Repository structuur

```
repo/
├── .github/
│   └── workflows/
│       └── generate-content.yml    # Dagelijkse cron job (06:00 UTC)
├── generator/
│   ├── generate.py                 # Content generatie via Claude API
│   ├── sites.json                  # Config per site (type, edge cases, relevantie-kans)
│   └── templates/                  # HTML-templates per site-stijl
│       ├── vakbond.html
│       ├── overheid.html
│       ├── hr-magazine.html
│       ├── sector.html
│       ├── werkgevers.html
│       ├── juridisch.html
│       └── nieuws.html
└── sites/
    ├── vakbond-nieuws/
    │   ├── index.html
    │   └── artikelen/
    ├── overheid-arbeidsmarkt/
    ├── hr-magazine/
    ├── sector-zorg/
    │   └── docs/                   # PDF-opslag
    ├── werkgevers-platform/
    │   └── docs/
    ├── arbeidsrecht-updates/
    └── loondienst-nieuws/
```

### Hosting

- **Platform:** GitHub Pages
- **GitHub Pages source:** root van de repo (`/`)
- **URLs:** `username.github.io/repo-naam/sites/vakbond-nieuws/` etc.
- **API keys:** Opgeslagen als GitHub Secrets, nooit in code of bestanden

### Content generatie

De GitHub Actions workflow draait dagelijks en voert het volgende uit:

1. Bepaal willekeurig welke artikel-sites die dag relevant CAO-nieuws krijgen op basis van `relevantie_kans` per site (trekking van een getal tussen 0 en 1 — als het onder de drempelwaarde valt, krijgt die site die dag relevant nieuws)
2. Bepaal op basis van een rotatieschema welke edge case vandaag actief is per site (zie Edge case rotatie)
3. Genereer per site 3-5 stukken content via Claude API:
   - Artikel-sites: HTML-pagina's met long-slug URL + evt. bewuste edge case URL
   - PDF-sites: Tekstbestand met dagdatum als inhoud (zichtbare inhoudswisseling) + update `index.html`
   - Pagina-wijziging-sites: Pas `index.html` aan volgens het rotatieschema
4. Schrijf bestanden naar de juiste `sites/` map
5. Commit en push → GitHub Pages deployt automatisch

Bij een API-fout voor één site: log de fout, sla die site over, ga door met de rest. Gedeeltelijke resultaten worden gecommit. De workflow faalt niet als één site mislukt.

### PDF-strategie

GitHub Pages ondersteunt geen server-side PDF-generatie. PDFs worden als volgt gesimuleerd:

- **Bestand:** Platte tekstbestanden met `.pdf` extensie (door de meeste scrapers als PDF-link herkend)
- **Inhoud bij vaste URL:** Het bestand op `/docs/cao.pdf` bevat altijd de huidige datum en een kort stuk nep-CAO-tekst. De inhoud wisselt dagelijks, de URL niet — dit test of de monitor een bestandswijziging detecteert.
- **Inhoud bij wisselende URL:** Nieuwe bestanden (`/docs/cao-2026-03-12.pdf`) worden dagelijks toegevoegd. Oude bestanden blijven staan zodat de monitor nieuwe links kan signaleren.

### Edge case rotatie

Elke site heeft een geordende lijst van edge cases in `sites.json`. De generator berekent dagelijks `dag_van_het_jaar % aantal_edge_cases` om te bepalen welke edge case vandaag actief is. Zo roteert elke edge case periodiek en is het schema deterministisch en reproduceerbaar.

**Speciale gevallen:**

- **`artikel_verdwijnt`:** Lifecycle over drie fasen, bijgehouden in `state.json` onder `{ "<site>": { "verdwenen_slug": null, "dag": null } }`:
  - **Fase 1 (dag N, edge case actief):** Generator maakt artikel aan, schrijft slug en dag N naar state.json.
  - **Fase 2 (dag N+1, bij elke run):** Generator controleert of `dag == gisteren`. Zo ja: verwijder het artikel, zet state.json terug op `{ "verdwenen_slug": null, "dag": null }`.
  - **Fase 3 (volgende keer dat edge case actief is):** state.json heeft `null` — generator behandelt dit als een nieuwe Fase 1 en maakt een nieuw artikel met een nieuwe slug.
  - Als het bestand op dag N+1 al verdwenen is (bijv. handmatig verwijderd), logt de generator een waarschuwing en wist state.json zonder te falen.

- **`oud_nieuws_herplaatst`:** Het archief is de map `generator/archive/<site>/` die HTML-bestanden bevat in exact hetzelfde formaat als normale artikelen. Elke dagelijkse run schrijft elk gegenereerd artikel ook naar het archief. Op de dag dat deze edge case actief is:
  - Als het archief ≥1 bestand bevat: kies een willekeurig bestand, kopieer het naar `sites/<site>/artikelen/` met een nieuwe bestandsnaam (format: `YYYY-MM-DD-<originele-slug-zonder-datum>.html`), maar met ongewijzigde body-content.
  - Als het archief leeg is (eerste run): genereer een normaal nieuw artikel en sla het ook op in het archief. De edge case vuurt niet — dit wordt gelogd.
- **`grote_redesign`:** De site wisselt tussen twee vaste template-varianten (`template_a` en `template_b`). De actieve variant wordt opgeslagen in `generator/state.json` onder `{ "<site>": { "actieve_template": "a" } }`. Bij elke redesign-dag flipt de generator deze waarde. `alleen_footer` en `typofout` lezen de actieve variant uit state.json en passen de juiste template aan.
- **`teruggedateerd`:** De generator maakt een artikel aan met een `<time datetime="...">` attribuut dat 30-90 dagen in het verleden ligt, en gebruikt ook een verouderde datum in de bestandsnaam (bijv. `artikelen/2025-11-15-cao-update.html`). De URL en publicatiedatum zijn dus beide teruggedateerd.
- **`diep_verstopt` (PDF):** De PDF-link staat niet in de hoofdnavigatie of bovenste content, maar in een `<details>`-element onderaan de pagina.

### sites.json configuratie

```json
{
  "vakbond-nieuws": {
    "type": "artikel",
    "stijl": "vakbond",
    "monitor_url": "https://username.github.io/repo-naam/sites/vakbond-nieuws/",
    "relevantie_kans": 0.6,
    "edge_cases": ["korte_slug", "anker_url", "cacao_false_positive"]
  },
  "overheid-arbeidsmarkt": {
    "type": "artikel",
    "stijl": "overheid",
    "monitor_url": "https://username.github.io/repo-naam/sites/overheid-arbeidsmarkt/",
    "relevantie_kans": 0.5,
    "edge_cases": ["pagina_url", "relevant_zonder_cao_woord", "noindex_tag"]
  },
  "hr-magazine": {
    "type": "artikel",
    "stijl": "hr-magazine",
    "monitor_url": "https://username.github.io/repo-naam/sites/hr-magazine/",
    "relevantie_kans": 0.4,
    "edge_cases": ["teruggedateerd", "oud_nieuws_herplaatst", "artikel_verdwijnt"]
  },
  "sector-zorg": {
    "type": "pdf",
    "stijl": "sector",
    "monitor_url": "https://username.github.io/repo-naam/sites/sector-zorg/",
    "edge_cases": ["zelfde_url_nieuwe_inhoud", "diep_verstopt"]
  },
  "werkgevers-platform": {
    "type": "pdf",
    "stijl": "werkgevers",
    "monitor_url": "https://username.github.io/repo-naam/sites/werkgevers-platform/",
    "edge_cases": ["korte_pdf_naam", "pdf_verdwijnt_nieuwe_naam"]
  },
  "arbeidsrecht-updates": {
    "type": "pagina",
    "stijl": "juridisch",
    "monitor_url": "https://username.github.io/repo-naam/sites/arbeidsrecht-updates/",
    "edge_cases": ["alleen_footer", "typofout", "grote_redesign"]
  },
  "loondienst-nieuws": {
    "type": "pagina",
    "stijl": "nieuws",
    "monitor_url": "https://username.github.io/repo-naam/sites/loondienst-nieuws/",
    "edge_cases": ["cookiebanner_wissel", "content_zonder_url"]
  }
}
```

## Testdoelen

De kolom "Doel van de test" maakt expliciet of we een bekende beperking documenteren, een bug blootleggen, of correct gedrag bevestigen.

| Edge case | Verwacht huidig gedrag | Doel van de test |
|---|---|---|
| Korte slug | Monitor mist artikel | **Bug blootleggen:** monitor zou ook korte slugs moeten detecteren |
| Paginering als artikel-URL | Monitor triggert onterecht | **Bug blootleggen:** false positive door genummerde pagina-URL |
| Lange filter-URL | Monitor triggert onterecht | **Bug blootleggen:** false positive door lange URL |
| "Cacao" false positive | Monitor markeert als relevant | **Bug blootleggen:** relevantiedetectie te grof |
| Relevant nieuws zonder "CAO" | Monitor mist artikel | **Bug blootleggen:** false negative door ontbrekend trefwoord |
| PDF zelfde URL, nieuwe inhoud | Monitor mist update | **Bug blootleggen:** monitor controleert inhoud niet, alleen URL |
| PDF verdwijnt, nieuwe naam | Monitor detecteert nieuwe URL | **Correct gedrag bevestigen:** nieuwe URL moet als nieuw worden gesignaleerd |
| Artikel verdwijnt en keert terug | Monitor behandelt als nieuw | **Correct gedrag bevestigen of bug:** afhankelijk van gewenste logica |
| Alleen footer gewijzigd | Monitor triggert | **Bug blootleggen:** false positive bij kleine irrelevante wijziging |
| Kleine typofout hersteld | Monitor triggert | **Bug blootleggen of correct gedrag:** afhankelijk van gewenste gevoeligheid |
| noindex op artikel | Onduidelijk | **Gedrag documenteren:** vaststellen of monitor robots-instructies respecteert |
| Teruggedateerd artikel | Monitor behandelt als oud | **Correct gedrag bevestigen:** terugdatering mag niet als nieuw triggeren |
| Cookiebanner wisselt | Monitor triggert | **Bug blootleggen:** false positive bij niet-inhoudelijke wijziging |

## Beslissingen en afwegingen

- **Statische HTML over dynamische server:** Geen server nodig, geen onderhoud, gratis hosting
- **Één repo over aparte repos:** Centraal beheer, één GitHub Actions workflow, eenvoudiger
- **Claude API voor content:** Realistische Nederlandse tekst, flexibel per site-stijl en edge case
- **Tekstbestanden als PDF-simulatie:** GitHub Pages ondersteunt geen echte PDF-generatie; tekstbestanden met `.pdf` extensie zijn voldoende voor link-detectie door scrapers
- **Geen authenticatie op sites:** Content is nep, geen gevoelige data — sites zijn niet actief gepromoot
- **GitHub Actions runner:** `ubuntu-latest`, Python 3.11+. Geen externe dependencies buiten de Anthropic Python SDK en de standaard bibliotheek.
- **Deterministisch rotatieschema:** Reproduceerbaarheid van tests is waardevoller dan volledige willekeur
- **Repo-groei door wisselende PDF-URLs:** Bestanden met datumslug groeien dagelijks (~7 bestanden/dag). Na 90 dagen is dit ~630 extra bestanden — acceptabel voor een testomgeving. Geen cleanup-beleid nodig voor nu.
- **Root index.html:** De repo-root bevat een simpele `index.html` die naar alle zeven sites linkt, zodat de basis-GitHub-Pages-URL geen 404 geeft.
