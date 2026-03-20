import requests
import time
from pprint import pprint  # красивое отображение json файлов

API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "8630962766:AAEiw0A9ZZa803_6KbLyruTEfYKqTW-mLnE"
TEXT = "some kind of text"
LIMIT = 100

offset = -2  # смещение для получения последнего апдейта, в последующем обновляется на последний апдейт
c = 0
chat_id: int

while c < LIMIT:  # постоянный процесс опроса
    print(f"attempt {c}")

    updates = requests.get(
        f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}"
    ).json()

    pprint(updates)

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            requests.get(
                f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}"
            )
    time.sleep(1)
    c += 1
