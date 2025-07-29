# Třetí projekt do Engeto Online Python Akademie

*Tento Python skript stáhne výsledky voleb do Poslanecké sněmovny 2017 pro všechny obce v jednom okrese z portálu volby.cz, a uloží je do .csv souboru.*

## Co skript dělá?

Skript načte:
- seznam všech obcí z daného odkazu pro vybraný okres
- za každou obec
  - `code` kód obce (např. 554499)
  - `location` název obce (např. Aš)
  - `registered` počet zapsaných voličů
  - `envelopes` vydané obálky
  - `valid` platné hlasy
  - názvy jednotlivých kandidujících stran a hnutí (v abecedním pořadí), kde každý sloupec odpovídá jednomu kandidujícímu subjektu a udává počet hlasů

## Požadavky
- Python 3.6+
- knihovny: `requests`, `beautifulsoup4` 

## Jak spustit skript?

1) Instalace požadavků

	<pre>`pip install -r requirements.txt</pre>

2) Spuštění skriptu se dvěma argumenty

    <pre>python main.py "URL_na_okres" "vystupni_soubor.csv"</pre>

 Konkrétní příklad:
    <pre>python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101" "vysledky_cheb.csv""</pre>

## Testováno na
- Python 3.13.3
- macOS
- Okres: Cheb (Karlovarský kraj), konkrétní skript je uveden výše