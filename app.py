import telebot

from config import TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, text=f"{message.chat.username}, приветствуем Вас в боте-конвертере валют! "
                                           f"Для работы с ботом вам необходимо ввести валюту, из которой необходимо "
                                           f"перевести, валюту, в которую нужно перевести, и число - сумма валюты. "
                                           f""
                                           f"Например, если ввести сообщение 'рубль доллар 100', то бот напишет Вам, "
                                           f"сколько будет 100 рублей в долларах по действующему курсу.")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, text=f"Команды для работы с ботом:\n"
                                           f"/start - запустить бота\n"
                                           f"/help - помощь по боту\n"
                                           f"/values - информация о всех доступных валютах\n"
                                           f"Инструкция по конвертации валют. Например, если ввести сообщение "
                                           f"'рубль доллар 100', то бот напишет Вам, сколько будет 100 рублей в "
                                           f"долларах по действующему курсу.")


@bot.message_handler(commands=['values'])
def values_command(message):
    text = "Список доступных валют:"
    for key in KEYS.keys():
        text += f"\n{key.capitalize()}"
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        converting_result = Converter.get_price(values)
    except APIException as error:
        bot.reply_to(message, text=f'Ошибка пользователя: {error}')
    except Exception:
        bot.reply_to(message, text=f"""Ошибка сервера: не удалось обработать команду '{message.text}'""")
        print(f"""Ошибка сервера: не удалось обработать команду '{message.text}'""")
    else:
        text = f"Цена {values[2]} {values[0].lower()} в {values[1].lower()} - {converting_result}"
        bot.reply_to(message, text=text)


@bot.message_handler(content_types=[
    'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location',
    'contact', 'web_app_data', 'pinned_message'])
def stop_content(message):
    bot.reply_to(message, text='Ошибка пользователя: неверный формат данных. Вводите данные в формате текста: '
                               '<имя валюты, цену которой Вы хотите узнать> '
                               '<имя валюты, в которой надо узнать цену первой валюты> '
                               '<количество первой валюты>.')


bot.polling(none_stop=True)
