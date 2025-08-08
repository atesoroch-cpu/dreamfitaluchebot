import os
import time
import logging
import requests
from bs4 import BeautifulSoup
from threading import Thread

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def fetch_aforo():
    url = "https://www.dreamfit.es/centros/aluche"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        collapse = soup.find(id="collapseAforo")
        if not collapse:
            return None
        h1_elem = collapse.find("h1")
        clientes = collapse.find_all("h3", class_="cliente")
        if h1_elem and len(clientes) >= 2:
            porcentaje = ''.join(filter(str.isdigit, h1_elem.get_text(strip=True)))
            personas = ''.join(filter(str.isdigit, clientes[0].get_text(strip=True)))
            capacidad_total = ''.join(filter(str.isdigit, clientes[1].get_text(strip=True)))
            return porcentaje, personas, capacidad_total
        strongs = collapse.find_all("strong")
        if len(strongs) >= 3:
            porcentaje = ''.join(filter(str.isdigit, strongs[0].get_text(strip=True)))
            personas = ''.join(filter(str.isdigit, strongs[1].get_text(strip=True)))
            capacidad_total = ''.join(filter(str.isdigit, strongs[2].get_text(strip=True)))
            return porcentaje, personas, capacidad_total
    except Exception as e:
        logger.error(f"Error fetching occupancy: {e}")
    return None

def send_message(chat_id: int, text: str) -> None:
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        logger.error(f"Error sending message: {e}")

def process_update(update: dict) -> None:
    message = update.get("message")
    if not message:
        return
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip().lower()
    if not text:
        return
    data = fetch_aforo()
    if data:
        porcentaje, personas, capacidad_total = data
        response = (
            f"\ud83d\udd14 <b>Dreamfit Aluche</b>\n"
            f"\ud83d\udd14 <b>Aforo actual:</b> {porcentaje}%\n"
            f"\ud83d\udc65 <b>Ocupación:</b> {personas} personas\n"
            f"\ud83c\udfdbþ <b>Aforo total:</b> {capacidad_total} personas"
        )
    else:
        response = (
            "No he podido obtener el aforo del gimnasio en este momento.\n"
            "Por favor, intenta de nuevo más tarde."
        )
    send_message(chat_id, response)

def start_keepalive_loop():
    def run():
        while True:
            try:
                requests.get(f"{BASE_URL}/getMe", timeout=10)
                logger.info("Keepalive ping to Telegram succeeded")
            except Exception:
                logger.warning("Keepalive ping to Telegram failed")
            time.sleep(600)
    thread = Thread(target=run)
    thread.daemon = True
    thread.start()

def main() -> None:
    start_keepalive_loop()
    offset = None
    while True:
        url = f"{BASE_URL}/getUpdates?timeout=60"
        if offset is not None:
            url += f"&offset={offset}"
        try:
            resp = requests.get(url, timeout=100)
            resp.raise_for_status()
            data = resp.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                process_update(update)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
