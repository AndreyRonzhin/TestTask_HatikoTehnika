from typing import Any
from .service import IMEI, IMEICheckNet
from requests.exceptions import RequestException
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from.models import UserTgBot
import telebot

bot = telebot.TeleBot(settings.TOKEN_TG_BOT)

def covert_response(values:dict[str, Any])->str:
    names = {'deviceName': 'Наименование',
             'apple/region': 'Cтрана',
             'serial':'серийный номер'}

    result = [f'{v}: {values.get(k)}' for k, v in names.items() if values.get(k, None)]
    return  '\n'.join(result)

def check_user(user_tg):
    try:
        obj_user = UserTgBot.objects.get(user_id=user_tg.id)
    except ObjectDoesNotExist:
        obj_user = UserTgBot.objects.create(user_id=user_tg.id,
                                            name=user_tg.first_name,
                                            username=user_tg.username)

    if not obj_user.access_is_allowed:
        bot.send_message(user_tg.id, "Вы не зарегистрированы, дождитесь проверки администратора.")

    return obj_user.access_is_allowed

@bot.message_handler(commands=['start'])
def handle_start(message):
    if not check_user(message.from_user):
        return None

    bot.send_message(message.from_user.id, "Привет, введите IMEI устройства.")


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
def handle_check_imei(message):
    if not check_user(message.from_user):
        return None

    imei = None
    try:
        imei = IMEI(message.text)
    except ValueError as ex:
        bot.send_message(message.from_user.id, f'{str(ex)}. Воспользуйтесь /help')

    if isinstance(imei, IMEI):
        token = settings.TOKEN_API_SANDBOX
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

