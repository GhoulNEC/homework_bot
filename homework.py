import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (EmptyResponseError, HTTPStatusError,
                        ResponseError, TokenError)

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    handlers=[logging.FileHandler('main.log', 'w', 'utf-8'),
              logging.StreamHandler(sys.stdout)]
)

PRACTICUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправка сообщения в Telegram чат."""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    logging.info('Сообщение успешно отправлено')


def get_api_answer(current_timestamp):
    """Возвращает ответ API в случае успешного запроса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        logging.info('получен ответ от API')
    except ResponseError as error:
        raise ResponseError(f'Проблема с подключением к API: {error}')
    if response.status_code != HTTPStatus.OK:
        raise HTTPStatusError(f'Пришел отличный от 200 статус: '
                              f'{response.status_code}')
    return response.json()


def check_response(response):
    """Проверка корректности ответа API."""
    if not isinstance(response, dict):
        raise TypeError('Ответ пришел не с типом данных dict')

    if 'homeworks' not in response or 'current_date' not in response:
        raise EmptyResponseError('Пришел пустой ответ')

    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise KeyError('Домашки не являются типом данных list')

    logging.info('Ответ API пришел в нужном формате')
    return homeworks


def parse_status(homework):
    """Извлечение статуса работы из информации о самой домашней работе."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if 'homework_name' not in homework:
        raise KeyError('Ключ "homework_name" отсутствует')
    if homework_status not in HOMEWORK_STATUSES:
        raise ValueError(f'Статус {homework_status} отсутствует в вердикте')
    verdict = HOMEWORK_STATUSES[homework_status]
    logging.info('Получен статус домашки')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    env_vars = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    return all(env_vars)


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Отсутствует одна из переменных окружения')
        raise TokenError('Отсутствует одна из переменных окружения')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    last_message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            if homework:
                message = parse_status(homework[0])
                if message != last_message:
                    current_timestamp = response['current_date']
                    last_message = message
                    send_message(bot, last_message)
                else:
                    logging.debug('Новые статусы отсутствуют')
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.exception(message)
            try:
                send_message(bot, message)
            except Exception as error:
                logging.exception(f'Сообщение не было отправлено: {error}')

            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
