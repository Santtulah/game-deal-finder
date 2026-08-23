from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
import json
from pathlib import Path
import time      # LISÄTTY: Taukoja varten
import random    # LISÄTTY: Satunnaisuutta varten

# Path(__file__) on tämä kooditiedosto itse.
# .resolve().parent nousee kansion ylöspäin.
CURRENT_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = (
    CURRENT_DIR.parent.parent
)  # Noustaan projektin juureen (game-deal-finder)

# Määritetään polku data-kansioon juuren kautta
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)  # Luodaan data-kansio jos sitä ei vielä ole

file_path_games = DATA_DIR / "tori_games.json"
file_path_consoles = DATA_DIR / "consoles.json"

class ToriScraper:
    def __init__(self):
        self.base_url = "https://www.tori.fi/recommerce/forsale"
        self._playwright = None
        self._browser = None

    def __enter__(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
            
    def save_json(self, data: list[dict], filepath):
        try:
            with open(filepath, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[PriceScraper] Virhe tallennettaessa tiedostoa: {e}")

    

    def scrape_ad_description(self, link):
        page = self._browser.new_page(user_agent=(
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                " AppleWebKit/537.36"
                            ))
                            
        # OPTIMOINTI 1: Estetään kaikkien kuvien latautuminen kaistan säästämiseksi
        page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

        extracted_lines = []
        try:
            page.goto(link, timeout=15000)
            
            section_locator = page.locator('section[data-testid="description"]')
            section_locator.wait_for(state="attached", timeout=5000)
            page.wait_for_timeout(1500)

            section_html = section_locator.inner_html()
            soup = BeautifulSoup(section_html, "html.parser")

            print(f"\n--- TUTKITAAN LINKKIÄ: {link} ---")

            paragraphs = soup.find_all("p")
            print(f"LÖYTYIKÖ P-TÄGEJÄ? Löytyi {len(paragraphs)} kpl")

            for p in paragraphs:
                line_text = p.get_text(strip=True)
                if line_text:
                    extracted_lines.append(line_text)
                    print(f"Poimittu rivi: {line_text}")
            
            print("-----------------------------------\n")

        except TimeoutError:
            print(f"Aikakatkaisu: Sivua ei saatu ladattua tai kuvaus puuttuu ({link}).")
            
        finally:
            page.close()
            
        return extracted_lines

    def _parse_price(self, text:str):
            if not text:
                return None
            parsed_price = text.replace("€", "").strip()
            return parsed_price

    def search_tori(self, query: str = "ps2 peli"):
        formatted_query = query.replace(" ", "+")
        search_url = f"/search?q={formatted_query}&sort=PUBLISHED_DESC"

        page = self._browser.new_page(user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                        " AppleWebKit/537.36"
                    ))
                    
        # OPTIMOINTI: Estetään kuvat myös hakutulossivulla
        page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

        try:
            page.goto(self.base_url + search_url, timeout=15000)
            page.wait_for_selector("article.sf-search-ad", timeout=5000)

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            articles = soup.find_all("article", class_="sf-search-ad")
            games = []

            for article in articles:
                title_tag = article.find("h2")
                title = title_tag.get_text(strip=True) if title_tag else None
                link_tag = article.find("a") if title else None
                link = link_tag.get("href") if link_tag else None
                id = link_tag.get("id") if link_tag else None
                price_tag = article.select_one("div.flex.justify-between.font-bold")
                price = price_tag.get_text(strip=True) if price_tag else None
                price = self._parse_price(price)

                if title:
                    games.append({
                        "id": id,
                        "title": title,
                        "price": price,
                        "link": link
                    })
            return games
        finally:
            page.close()


# if __name__ == "__main__":
#     with ToriScraper() as scraper:

#         print("Käynnistetään pelien haku...")
#         games = scraper.search_tori("ps2 pelejä")

#         for game in games:

#             print(f"Tutkitaan ilmoituksen runkoa...")
#             # Haetaan kuvaus
#             game["description"] = scraper.scrape_ad_description(game["link"])
            
#             # OPTIMOINTI: Ihmismäinen viive (2.0 - 4.5 sekuntia)
#             viive = random.uniform(2.0, 4.5)
#             print(f"Odotetaan {viive:.1f} sekuntia ennen seuraavaa ilmoitusta bottiestojen välttämiseksi...\n")
#             time.sleep(viive)
#         scraper.save_json(games, file_path_games)
     
#         print("Aloitetaan konsolien haku...")

#         cheap_consoles = []
#         consoles = scraper.search_tori("playstation 2 konsoli")
#         for console in consoles:
#             if console["price"]:
#                 try:
#                     fixed_price = console["price"].replace(",", ".")
#                     price_as_number = float(fixed_price)
#                     if price_as_number <= 100:
#                         cheap_consoles.append(console)
#                     else:
#                         pass
#                 except ValueError:
#                     cheap_consoles.append(console)
#             else:
#                 cheap_consoles.append(console)
#         scraper.save_json(cheap_consoles, file_path_consoles)   

                        

