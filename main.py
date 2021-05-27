import logging
import os
import sys
import time

from dotenv import load_dotenv
import telegram
import requests

DVMN_API = "https://dvmn.org/api/long_polling/"
SITE = "https://dvmn.org"

logging.basicConfig(format="%(process)d %(levelname)s %(message)s")


def fetch_response_from_api(token, timestamp=None):
    """Get response from devman API.

    :param token: devman API token
    :param timestamp: timestamp to get response from
    :return: response in JSON format
    """

    headers = {
        "Authorization": f"Token {token}"
    }

    params = {
        "timestamp": timestamp,
    }

    response = requests.get(
        DVMN_API,
        headers=headers,
        params=params,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()


def generate_message(is_passed, lesson_title, lesson_url):
    """Generate message to send in bot.

    :param is_passed: is solution passed
    :param lesson_title: title of the lesson
    :param lesson_url:  url of the lesson
    :return: generated text
    """

    text = f"У вас проверили работу \"{lesson_title}\"\n({lesson_url})\n"
    if is_passed:
        text += "Преподавателю всё понравилось,"
        " можно приступать к следующему уроку!"
        return text
    text += "К сожалению, в работе нашлись ошибки."
    return text


def process_long_polling(token, bot, chat_id):
    """Process long polling to devman API.

    :param token: devman token
    :param bot: bot to send status to
    :param chat_id: chat id of the bot
    :return: None
    """

    timestamp = 0
    logger.info("Бот запущен")
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
        except ZeroDivisionError:
            logger.warning("Ошибка деления на ноль. Бот продолжает работать")
            continue
        except requests.HTTPError as e:
            error_message = f"Error during http request: {e}"
            logger.error(error_message)
            sys.exit(error_message)
        except requests.exceptions.ReadTimeout:
            logger.warning(
                "Таймаут ожидания вышел. Бот продолжает работать."
            )
            continue
        except requests.ConnectionError:
            logger.warning("Ошибка соединения. Бот переподключается.")
            time.sleep(60)
            continue


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()
    dvmn_api_token = os.getenv("DVMN_API_TOKEN")
    telegram_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("CHAT_ID")

    telegram_bot = telegram.Bot(token=telegram_token)

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_bot, telegram_chat_id))

    process_long_polling(dvmn_api_token, telegram_bot, telegram_chat_id)
