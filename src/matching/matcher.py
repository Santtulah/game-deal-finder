import json
from rapidfuzz import fuzz
from rapidfuzz.process import extract
from pathlib import Path
import re


ABBREVIATIONS = {
    "gta": "Grand Theft Auto",
    "mgs": "Metal Gear Solid",
    "nfs": "Need for Speed",
    "hp": "Harry Potter",
    "lotr": "Lord of the Rings",
}


class GameMatcher:
    def __init__(self, pc_games_path):

        with open(pc_games_path, "r", encoding="utf-8") as f:
            self.pc_games = json.load(f)


    def _parse_pc_games(self, title:str):
        parsed_title = title.replace("[", " ").replace("]", " ").lower()
        parsed_title = " ".join(parsed_title.split())
        return parsed_title

    def parse_tori_line(self, line_text:str):

        if "tarjoa" in line_text.lower() or "tarjous" in line_text.lower():

            clean_text = re.sub(r'(tarjoa|tarjous)', "", line_text, flags=re.IGNORECASE).strip()
            return clean_text, "Tarjoa"

        else:
            pattern = re.compile(r'(\d+)\s*(?:e|eur|€|euroa)', flags=re.IGNORECASE)
            match = pattern.search(line_text)

            if match:
                price = match.group(1)
                game_name = line_text[:match.start()]
                game_name = game_name.strip()
                return game_name, price
            else:
                return line_text, None

    def find_match(self, tori_text: str):
        tori_game_name, tori_price = self.parse_tori_line(tori_text)

        search_name = tori_game_name.lower()

        for pc_game in self.pc_games:
            pc_clean_name = self._parse_pc_games(pc_game["title"])

            if pc_clean_name in search_name:
                return {
                    "Pricecharting-nimi": pc_clean_name,
                    "CIB-hinta": pc_game["cib_price"],
                    "Pricechart linkki": pc_game["link"],
                    "Tori-hinta": tori_price
                }
        return None


if __name__ == "__main__":
    pc_path = "../../data/pricecharting_games.json"

    try:
        matcher = GameMatcher(pc_path)
        print("Tietokanta ladattu onnistuneesti\n")

        # 2. Testataan "pesukonetta" ja "etsivää" keksityillä Torin lauseilla!
        test_lines = [
            "Rule of rose [not for resale] uudenveroinen - 20e", # Pitäisi löytyä!
            "Kuon ps2 tarjoa", # Pitäisi löytyä!
            "NHL 04 naarmuinen 5eur", # Ei pitäisi löytyä (ei arvokas)
            "Myydään michigan: report from hell hintaan 15€" # Pitäisi löytyä!
        ]

        for line in test_lines:
            osuma = matcher.find_match(line)

            if osuma:
                print("ARVOPELI LÖYTYNYT!")
                print(f"Nimi: {osuma['Pricecharting-nimi']}")
                print(f"Torin pyynti: {osuma['Tori-hinta']} | CIB-hinta {osuma['CIB-hinta']}")
            else:
                print("EI OSUMIA")
    except FileNotFoundError:
        print(f"Virhe: Polkua {pc_path} ei löytynyt!")