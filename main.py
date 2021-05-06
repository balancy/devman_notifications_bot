import os
import sys

from dotenv import load_dotenv
import telegram
import requests

DVMN_API = "https://dvmn.org/api/long_polling/"


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


def process_long_polling(token, bot, chat_id):
    timestamp = 0
    while True:
        try:
            response = fetch_response_from_api(token, timestamp)
            timestamp = response["new_attempts"][-1]["timestamp"]
            bot.send_message(
                chat_id=chat_id, text="Преподаватель проверил работу!"
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
