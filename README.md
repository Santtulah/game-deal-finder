# Retro Game Value Scanner

This is an automation tool implemented in Python that monitors the Tori.fi marketplace for retro game listings (e.g., PS2 games). The program compares the asking prices in the listings against market values from the PriceCharting database and sends an automated alert to Discord if a valuable game is identified.

The project serves as a portfolio piece demonstrating web scraping, data processing, API integrations (Discord Webhooks), and modular software architecture.

## Features

- **Intelligent Data Retrieval (Scraping):** Fetches listing titles and automatically reads listing descriptions. Includes randomized delays (2.0–4.5 seconds) to avoid bot detection mechanisms.
- **Text Recognition:** Analyzes unstructured text (user-written listings) and searches for matches against the collected reference data.
- **Real-Time Notifications:** Sends an immediate alert (game name, asking price, CIB value, and link) to a designated Discord channel upon a match.
- **State Management:** Saves previously processed listings to a local JSON file, preventing the program from sending duplicate alerts for the same listings during subsequent runs.

## Technologies & Architecture

The code follows a clean, object-oriented structure (Separation of Concerns), where responsibilities are divided into distinct modules:

- **`ToriScraper`:** Solely responsible for fetching and parsing HTML data.
- **`GameMatcher`:** Handles the business logic, comparing the text of the listings with PriceCharting data.
- **`DiscordNotifier`:** Responsible for sending HTTP requests to the external API.

**Core Technologies:** Python, `.env` (secret management), Discord Webhooks, JSON data processing.

## Installation and Usage

1. **Clone the repository and set up the environment:**
   ```bash
   git clone [YOUR-GITHUB-LINK-HERE]
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux (or Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
---

# Retro Game Value Scanner

Tämä on Pythonilla toteutettu automaatiotyökalu, joka seuraa Tori.fi-kauppapaikkaa retropeleihin (esim. PS2-pelit) liittyen. Ohjelma vertaa myynti-ilmoitusten hintoja PriceCharting-tietokannan markkina-arvoihin ja lähettää automaattisen hälytyksen Discordiin, jos se tunnistaa arvokkaan pelin.

Projekti toimii työnäytteenä web-skraappauksesta, datan prosessoinnista, API-integraatioista (Discord Webhooks) ja modulaarisesta ohjelmistoarkkitehtuurista.

## Ominaisuudet

- **Älykäs datanhaku (Scraping):** Hakee ilmoitusten otsikot ja käy automaattisesti lukemassa ilmoitusten kuvaukset. Sisältää satunnaistetut viiveet (2.0–4.5 sekuntia) bottiestojen välttämiseksi.
- **Tekstin tunnistus:** Analysoi epärakenteellista tekstiä (käyttäjien kirjoittamia ilmoituksia) ja etsii osumia kerätystä referenssidatasta.
- **Reaaliaikaiset ilmoitukset:** Lähettää osumista välittömästi ilmoituksen (pelin nimi, pyyntihinta, CIB-arvo ja linkki) valittuun Discord-kanavaan.
- **Tilan hallinta:** Tallentaa jo käsitellyt ilmoitukset paikalliseen JSON-tiedostoon, jolloin ohjelma ei lähetä samoista ilmoituksista tuplahälytyksiä seuraavalla ajokerralla.

## Teknologiat & Arkkitehtuuri

Koodi noudattaa puhdasta, olio-ohjelmoitua rakennetta (Separation of Concerns), jossa vastuut on jaettu omiin moduuleihinsa:

- **`ToriScraper`:** Vastaa yksinomaan HTML-datan noutamisesta ja jäsentämisestä.
- **`GameMatcher`:** Hoitaa liiketoimintalogiikan, eli ilmoitusten tekstin ja PriceCharting-datan vertailun.
- **`DiscordNotifier`:** Vastaa HTTP-pyyntöjen lähettämisestä ulkoiseen rajapintaan.

**Pääteknologiat:** Python, `.env` (salaisuuksien hallinta), Discord Webhooks, JSON-datan käsittely.

## Asennus ja Käyttö

1. **Kloonaa repositorio ja asenna ympäristö:**
   ```bash
   git clone [SINUN-GITHUB-LINKKISI-TÄHÄN]
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux (tai Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
   ```

## Kehitysideat

Projekti on suunniteltu laajennettavaksi. Seuraavia ominaisuuksia on suunniteltu tuleviin versioihin:

- **Uusien markkinapaikkojen tuki:** Modulaarisen rakenteen ansiosta järjestelmään on helppo lisätä uusia skreippereitä (esim. `EbayScraper` tai `HuutoNetScraper`) ilman, että ydinlogiikkaan tarvitsee koskea.
- **Fuzzy Matching (Sumea haku):** Tekstin tunnistuksen parantaminen (esim. `thefuzz` -kirjastolla), jotta ohjelma tunnistaa pelit myös silloin, kun myyjä on kirjoittanut nimen hieman väärin tai käyttänyt lyhenteitä.
- **Käyttöliittymä (Dashboard):** Yksinkertaisen web-käyttöliittymän rakentaminen löydettyjen pelien tilastointiin ja seurantaan.
