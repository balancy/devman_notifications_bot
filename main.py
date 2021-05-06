import os
import sys

from dotenv import load_dotenv
import telegram
import requests

DVMN_API = "https://dvmn.org/api/long_polling/"
SITE = "https://dvmn.org"


def fetch_response_from_api(token, timestamp=0):
    headers = {
        "Authorization": f"Token {token}"
    }

    params = {
        "timestamp": timestamp,
    } if timestamp else {}

    response = requests.get(
        DVMN_API,
        headers=headers,
        params=params,
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


def generate_message(is_passed, lesson_title, lesson_url):
    text = f"У вас проверили работу \"{lesson_title}\"\n({lesson_url})\n"
    if is_passed:
        text += "Преподавателю всё понравилось,"
        " можно приступать к следующему уроку!"
        return text
    text += "К сожалению, в работе нашлись ошибки."
    return text


def process_long_polling(token, bot, chat_id):
    timestamp = 0
    while True:
        try:
            response = fetch_response_from_api(token, timestamp)
            statistics = response["new_attempts"][-1]
            timestamp = statistics["timestamp"]
            is_passed = not statistics["is_negative"]
            lesson_title = statistics["lesson_title"]
            lesson_url = f"{SITE}{statistics['lesson_url']}"
            bot.send_message(
                chat_id=chat_id,
                text=generate_message(is_passed, lesson_title, lesson_url),
            )
        except requests.HTTPError as e:
            sys.exit(f"Error during http request: {e}")
        except requests.exceptions.ReadTimeout:
            continue
        except requests.ConnectionError:
            continue


if __name__ == "__main__":
    load_dotenv()
    dvmn_api_token = os.getenv("DVMN_API_TOKEN")
    telegram_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("CHAT_ID")

    telegram_bot = telegram.Bot(token=telegram_token)

    process_long_polling(dvmn_api_token, telegram_bot, telegram_chat_id)
