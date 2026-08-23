from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
from pathlib import Path

# Path(__file__) on tämä kooditiedosto itse.
# .resolve().parent nousee kansion ylöspäin.
CURRENT_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = (
    CURRENT_DIR.parent.parent
)  # Noustaan projektin juureen (game-deal-finder)

# Määritetään polku data-kansioon juuren kautta
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)  # Luodaan data-kansio jos sitä ei vielä ole

file_path = DATA_DIR / "pricecharting_games.json"

class PriceScraper:

    def __init__(self):
        self.base_url = "https://www.pricecharting.com/console/pal-playstation-2?sort=highest-price"
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

    def _parse_price(self, price_td):
        """Apufunktio teksti-muotoisen hinnan siistimiseksi float-luvuksi (esim. '$12.50' -> 12.5)"""
        if not price_td:
            return None
        raw_text = price_td.get_text(strip=True)
        if not raw_text or raw_text == "N/A":
            return None

        # Poistetaan valuuttamerkit ja mahdolliset pilkut
        clean_text = (
            raw_text.replace("$", "")
            .replace("€", "")
            .replace(",", "")
            .strip()
        )
        try:
            return float(clean_text)
        except ValueError:
            return None

    def search_ps2(self):
        page = self._browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36"
            )
        )

        try:
            page.goto(
                self.base_url, wait_until="domcontentloaded", timeout=15000
            )

            # Odotetaan taulukon latautumista 'article'-tagin sijaan
            page.wait_for_selector("table#games_table", timeout=5000)

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            table = soup.find("table", id="games_table")
            games = []

            if table:
                # Etsitään kaikki rivit tbody-osiosta
                rows = table.select("tbody tr")
                for row in rows:
                    title_td = row.find("td", class_="title")
                    title_a = title_td.find("a") if title_td else None

                    title = (
                        title_a.get_text(strip=True) if title_a else None
                    )
                    link = (
                        "https://www.pricecharting.com" + title_a["href"]
                        if title_a and title_a.has_attr("href")
                        else None
                    )

                    # Luetaan hinta-elementit
                    loose_price_td = row.find(
                        "td", class_="price numeric used_price"
                    )
                    cib_price_td = row.find(
                        "td", class_="price numeric cib_price"
                    )
                    new_price_td = row.find(
                        "td", class_="price numeric new_price"
                    )

                    # Puhdistetaan hinnat numeerisiksi
                    loose_price = self._parse_price(loose_price_td)
                    cib_price = self._parse_price(cib_price_td)
                    new_price = self._parse_price(new_price_td)

                    if title:
                        games.append(
                            {
                                "title": title,
                                "loose_price": loose_price,
                                "cib_price": cib_price,
                                "new_price": new_price,
                                "link": link,
                            }
                        )

            return games
        finally:
            page.close()


# Testiajo:
if __name__ == "__main__":
    with PriceScraper() as scraper:
        results = scraper.search_ps2()
        print(f"Löytyi {len(results)} peliä.")
        if results:
            scraper.save_json(results, file_path)
        print(f"Onnistui! Tallennettiin {len(results)} tiedostoon {file_path}")

        
            