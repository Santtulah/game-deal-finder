import requests

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_alert(self, title: str, game_name: str, tori_price, cib_price, link: str):

        # Rakennetaan viesti Discordiin
        message = (
            f"🚨 **UUSI ARVOPELI LÖYTYNYT TORISTA!** 🚨\n"
            f"**Ilmoitus:** {title}\n"
            f"**Peli:** {game_name}\n"
            f"**Pyynti:** {tori_price}€ | **Arvo (CIB):** {cib_price}€\n"
            f"🔗 **Linkki:** {link}"
        )

        data = {"content": message}

        try:
            response = requests.post(self.webhook_url, json=data)

            if response.status_code == 204:
                print(">>> Hälytys lähetetty onnistuneesti Discordiin! <<<")
            else:
                print(f"Virhe Discord-viestin lähetyksessä: {response.status_code}")
        except Exception as e:
            print(f"Discord-yhteys epäonnistui: {e}")