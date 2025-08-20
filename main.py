"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Ngoc Anh Ngo
email: annie@ngongocanh.com
"""

import sys
import csv
import re

import requests
from bs4 import BeautifulSoup

# základní URL pro načítání dat

BASE = "https://volby.cz/pls/ps2017nss/"

# funkce pro načtení HTML stránky a vrácení BeautifulSoup objektu

def get_soup(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    return BeautifulSoup(res.text, "html.parser")

# funkce pro zpracování seznamu obcí

def parse_obce_list(url):
    soup = get_soup(url)
    tables = soup.find_all("table")
    obce = []

    for table in tables:
        for row in table.find_all("tr")[2:]:
            cells = row.find_all("td")
            if len(cells) >= 3:
                obec_name = cells[1].text.strip()
                href_tag = cells[0].find("a")  # bereme odkaz z prvního sloupce (číslo obce)
                if href_tag:
                    href = href_tag.get("href")
                    full_url = BASE + href

                    # pokus o extrakci kódu obce z href
                    match = re.search(r"xobec=(\d+)", href)
                    obec_kod = match.group(1) if match else ""

                    obce.append((obec_kod, obec_name, full_url))
                else:
                    print(f"⚠️ Obec '{obec_name}' nemá funkční odkaz – přeskakuji.")
    return obce

# funkce pro zpracování výsledků pro jednu obec

def parse_vysledky_obce(obec_kod, obec_name, url):
    soup = get_soup(url)
    vysledky = {"code": obec_kod, "location": obec_name}

    # 1) Údaje o voličích, obálkách a platných hlasech
    table = soup.find("table", id="ps311_t1")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 6:
                try:
                    # uložení údajů do slovníku, odstranění speciálních znaků (non-breaking space), aby výsledky byly bez mezer 
                    vysledky["registered"] = tds[3].get_text(strip=True).replace('\xa0', '').replace('\u00a0', '').replace(' ', '')
                    vysledky["envelopes"] = tds[4].get_text(strip=True).replace('\xa0', '').replace('\u00a0', '').replace(' ', '')
                    vysledky["valid"] = tds[7].get_text(strip=True).replace('\xa0', '').replace('\u00a0', '').replace(' ', '')
                except IndexError:
                    continue

    # 2) Výsledky stran
    tables = soup.find_all("table")
    for table in soup.find_all("table"):
        header_cells = table.find_all("th")
        if any("Strana" in th.get_text() for th in header_cells):
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 3:
                    strana = cols[1].get_text(strip=True)
                    hlasy = cols[2].get_text(strip=True).replace('\xa0', '').replace('\u00a0', '').replace(' ', '')
                    if strana:
                        vysledky[strana] = hlasy

    return vysledky

# hlavní funkce pro spuštění skriptu

def main():
    if len(sys.argv) != 3:
        return None

    url = sys.argv[1]
    output_file = sys.argv[2]

    print(f"🔎 Načítám obce z: {url}")
    obce = parse_obce_list(url)

    if not obce:
        print("❌ Nepodařilo se načíst obce. Zkontroluj odkaz.")
        return
    
    # Zpracování výsledků pro každou obec

    vysledky_all = []
    for obec_kod, obec_name, obec_url in obce:
        print(f"📥 Zpracovávám: {obec_name} ({obec_kod})")
        data = parse_vysledky_obce(obec_kod, obec_name, obec_url)
        vysledky_all.append(data)

    # sloupce v požadovaném pořadí
    priority = ["code", "location", "registered", "envelopes", "valid"]
    all_keys = {k for row in vysledky_all for k in row}
    rest = sorted(k for k in all_keys if k not in priority)
    fieldnames = priority + rest

    # zápis výsledků do CSV souboru

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vysledky_all)

    # úspěšné dokončení

    print(f"✅ Hotovo! Výsledky uloženy do {output_file}")

    # kontrola existence souboru s výsledky

if __name__ == "__main__":
    main()
