import json
from scrapers.tori import ToriScraper
from matching.matcher import GameMatcher
from pathlib import Path
import time
import random

CURRENT_DIR = Path(__file__).resolve().parent
DATA_DIR = CURRENT_DIR.parent / "data"
SEEN_ADS_PATH = DATA_DIR / "seen_ads.json"

if __name__ == "__main__":
    pc_path = DATA_DIR / "pricecharting_games.json"
    # tori_path = DATA_DIR / "tori_games.json"

    try:
        seen_links = []
        if SEEN_ADS_PATH.exists():
            try:
                with open(SEEN_ADS_PATH, "r", encoding="utf-8") as f:
                    seen_links = json.load(f)
            except json.JSONDecodeError:
                # Jos tiedosto on tyhjä tai JSON on rikki, aloitetaan puhtaalta pöydältä
                print("Seen ads -tiedosto oli tyhjä tai vioittunut. Aloitetaan puhtaalta pöydältä.")
            

        matcher = GameMatcher(pc_path)

        with ToriScraper() as scraper:
            tori_ads = scraper.search_tori("ps2 pelit")
            

            for ad in tori_ads:
                
                link = ad.get("link")
                if not link or link in seen_links:
                                    continue
                ad["description"] = scraper.scrape_ad_description(link)

                delay= random.uniform(2.0, 4.5)
                print(f"Odotetaan {delay:.1f} sekuntia ennen seuraavaa... (Uusi ilmoitus)")
                time.sleep(delay)

                # Etsitään osumia otsikosta
                match = matcher.find_match(ad["title"])

                if match:
                    print(">>> ARVOPELI LÖYTYNYT OTSIKOSTA! <<<")
                    print(f"Ilmoitus: {ad['title']}")
                    print(f"Peli: {match['Pricecharting-nimi']}")
                    print(f"Torin pyynti: {match['Tori-hinta']} | CIB-hinta {match['CIB-hinta']}")
                    print(f"Linkki: {ad.get('link')}\n")

                # Etsitään osumia kuvauksesta
                elif "description" in ad:
                    for line in ad["description"]:
                        desc_match = matcher.find_match(line)

                        if desc_match:
                            print(f"Imoitus: {ad['title']}")
                            print(f"Peli: {desc_match['Pricecharting-nimi']}")
                            print(f"Torin pyynti {desc_match['Tori-hinta']} | CIB-hinta {desc_match['CIB-hinta']}")
                            print(f"Linkki: {ad.get('link')}\n")
                seen_links.append(link)
            with open(SEEN_ADS_PATH, "w", encoding="utf-8") as f:
                json.dump(seen_links, f)

        
    except Exception as e:
        print(f"Ohjelma kaatui virheeseen: {e}")