import requests
import time
from pprint import pprint  # красивое отображение json файлов
from config import BOT_TOKEN

API_URL = "https://api.telegram.org/bot"
API_CATS_URL = "https://api.thecatapi.com/v1/images/search"
BOT_TOKEN: str
ERROR_TEXT = "картинки не будет"
LIMIT = 100

offset = -2  # смещение для получения последнего апдейта, в последующем обновляется на последний апдейт
c = 0
cat_response: requests.Response
cat_link: str

while c < LIMIT:  # постоянный процесс опроса
    print(f"attempt = {c}")

    updates = requests.get(
        f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}"
    ).json()

    # pprint(updates)

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            cat_response = requests.get(API_CATS_URL)

            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]["url"]
                requests.get(
                    f"{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}"
                )
            else:
                requests.get(
                    f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}"
                )
    time.sleep(1)
    c += 1
