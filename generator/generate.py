#!/usr/bin/env python3
"""Dagelijkse content generator voor CAO monitor testwebsites."""

import json
import os
import random
import re
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
                        noindex: bool = False) -> str:
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
    link = f'<a href="{href}">{title}</a>\n      '
    content = content.replace(
        "<!-- Artikelen worden hier automatisch toegevoegd -->",
        f'{link}<!-- Artikelen worden hier automatisch toegevoegd -->'
    )
    index_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Artikel-sites
# ---------------------------------------------------------------------------

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

    # --- Genereer normale artikelen (2 irrelevant + evt. 1 relevant) ---
    onderwerpen_onzin = [
        "recepten voor een gezonde lunch op het werk",
        "tips voor thuiswerken in de zomer",
        "nieuwe kantoorinrichting trends",
        "cacao-productie stijgt wereldwijd",
        "fietsvergoeding voor werknemers",
        "vergaderruimtes van de toekomst",
        "koffiepauze cultuur in Nederland",
        "de beste ergonomische bureaustoelen van 2026",
        "hoe je productief blijft op vrijdagmiddag",
        "teambuilding activiteiten voor kleine bedrijven",
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
        html = render_article_html("CAO update met sectie-anker")
        filename = make_article_filename("cao-update-anker")
        (artikelen_dir / filename).write_text(render_article_html("CAO update met sectie-anker", body), encoding="utf-8")
        add_article_link_to_index(
            index_path, f"artikelen/{filename}#arbeidsmarkt",
            "CAO update met sectie-anker"
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
            clean_slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", originele_slug)
            nieuwe_naam = f"{today.isoformat()}-{clean_slug}.html"
            shutil.copy(bron, artikelen_dir / nieuwe_naam)
            add_article_link_to_index(index_path, f"artikelen/{nieuwe_naam}", f"(herplaatst) {clean_slug}")
            print(f"    -> Oud nieuws herplaatst: {nieuwe_naam}")
        else:
            prompt = "Schrijf een kort nieuwsartikel (2 alinea's) in het Nederlands over HR-nieuws. Schrijf alleen <p>-tags."
            body = call_claude(prompt)
            title = "HR-nieuws: nieuw artikel"
            filename = make_article_filename(title)
            html = render_article_html(title, body)
            (artikelen_dir / filename).write_text(html, encoding="utf-8")
            (archive_dir / filename).write_text(html, encoding="utf-8")
            add_article_link_to_index(index_path, f"artikelen/{filename}", title)
            print(f"    -> oud_nieuws_herplaatst: archief leeg, nieuw artikel: {filename}")

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


# ---------------------------------------------------------------------------
# PDF-sites
# ---------------------------------------------------------------------------

def generate_pdf_site(site_name: str, site_config: dict, state: dict) -> None:
    """Verwerk een PDF-type site."""
    site_dir = SITES_DIR / site_name
    docs_dir = site_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    index_path = site_dir / "index.html"
    edge_case = get_active_edge_case(site_config)
    print(f"  Edge case: {edge_case}")

    if edge_case == "zelfde_url_nieuwe_inhoud":
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
        pdf_path.write_text(
            f"Aanvullend CAO-document\nDatum: {today.isoformat()}\n\n{content}",
            encoding="utf-8"
        )
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
        pdf_path.write_text(
            f"CAO Document\nDatum: {today.isoformat()}\n\n{content}",
            encoding="utf-8"
        )
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
        gisteren = (today - timedelta(days=1)).isoformat()
        oud_bestand = docs_dir / f"cao-werkgevers-{gisteren}.pdf"
        if oud_bestand.exists():
            oud_bestand.unlink()
            print(f"    -> Verwijderd: {oud_bestand.name}")
        filename = f"cao-werkgevers-{today.isoformat()}.pdf"
        prompt = "Schrijf 2 regels nep-CAO-tekst voor werkgevers in het Nederlands."
        content = call_claude(prompt)
        (docs_dir / filename).write_text(
            f"CAO Werkgevers\nDatum: {today.isoformat()}\n\n{content}",
            encoding="utf-8"
        )
        link = f'<a href="docs/{filename}">CAO Werkgevers {today.isoformat()}</a>\n        '
        index_content = index_path.read_text(encoding="utf-8")
        index_content = index_content.replace(
            "<!-- PDF-links worden hier automatisch toegevoegd -->",
            f'{link}<!-- PDF-links worden hier automatisch toegevoegd -->'
        )
        index_path.write_text(index_content, encoding="utf-8")
        print(f"    -> Nieuwe naam: docs/{filename}")


# ---------------------------------------------------------------------------
# Pagina-wijziging-sites
# ---------------------------------------------------------------------------

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
            content = re.sub(
                r"&copy; \d{4} Arbeidsrecht",
                f"&copy; {today.year} Arbeidsrecht",
                content
            )
            index_path.write_text(content, encoding="utf-8")
            print(f"    -> Alleen footer: jaar bijgewerkt naar {today.year}")

        elif edge_case == "typofout":
            content = index_path.read_text(encoding="utf-8")
            if "Jurisprudenti e" not in content:
                content = content.replace("Jurisprudentie", "Jurisprudenti e", 1)
            else:
                content = content.replace("Jurisprudenti e", "Jurisprudentie", 1)
            index_path.write_text(content, encoding="utf-8")
            print("    -> Typofout ingevoerd/hersteld")

    elif site_name == "loondienst-nieuws":
        if edge_case == "cookiebanner_wissel":
            content = index_path.read_text(encoding="utf-8")
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
            update_tag = f'<!-- content-update-{today.isoformat()} -->'
            # Verwijder eventuele vorige update-tag
            content = re.sub(r'<!-- content-update-\d{4}-\d{2}-\d{2} -->\n.*?\n', '', content)
            nieuwe_regel = f'\n      {update_tag}\n      <p><em>Redactionele update: {today.isoformat()}.</em></p>'
            content = content.replace(
                "<h2>Laatste nieuws</h2>",
                f"<h2>Laatste nieuws</h2>{nieuwe_regel}"
            )
            index_path.write_text(content, encoding="utf-8")
            print("    -> Content update zonder URL-wijziging")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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


if __name__ == "__main__":
    main()
