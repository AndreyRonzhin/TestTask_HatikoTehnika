from typing import Any
from service import IMEI, IMEICheckNet
from requests.exceptions import RequestException
from django.conf import settings
import telebot
import os


bot = telebot.TeleBot(os.getenv('token_tg_bot'))

def covert_response(values:dict[str, Any])->str:
    names = {'deviceName': 'Наименование',
             'apple/region': 'Cтрана',
             'serial':'серийный номер'}

    result = [f'{v}: {values.get(k)}' for k, v in names.items() if values.get(k, None)]
    return  '\n'.join(result)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    print(user_id)
    bot.send_message(message.from_user.id, "Привет, укажите IMEI устройства.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id, '\n'.join(("Доступные форматы ввода IMEI:",
                                                      "XXXXXXXXXXXXXXX",
                                                      "XXXXXX-XX-XXXXXX-X",
                                                      "XXXXXX/XX/XXXXXX/X",
                                                      "XXXXXX.XX.XXXXXX.X",
                                                      "XX-XXXX-XX-XXXXXX-X",
                                                      "XX/XXXX/XX/XXXXXX/X",
                                                      "XX.XXXX.XX.XXXXXX.X",
                                                      'Где "X" это число от 0 до 9 включительно')))

@bot.message_handler(content_types=['text'])
def handle_help(message):
    imei = None
    try:
        imei = IMEI(message.text)
    except ValueError as ex:
        bot.send_message(message.from_user.id, f'{str(ex)}. Воспользуйтесь /help')

    if isinstance(imei, IMEI):
        token = os.getenv('token_API')
        check_net = IMEICheckNet(imei.imei, token, 12)

        try:
            response = check_net.post_check_imei()
        except RequestException:
            bot.send_message(message.from_user.id, f'К сожалению, не удалось получить информацию по IMEI {imei}')
        else:
            properties = response.get('content').get('properties', None)
            if properties:
                message_response = covert_response(properties)
                bot.send_message(message.from_user.id, message_response)
            else:
                bot.send_message(message.from_user.id, f'К сожалению, не удалось получить информацию по IMEI {imei}')

def start():
    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)