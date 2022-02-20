import telebot
from config import keys, TOKEN
from extensions import APIException, CurConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу, введите значения через пробел:\n<имя валюты> <в какую валюту перевести>\
    \n<количество переводимой валюты>\
    \nДробные числа разделяйте точкой.\
    \nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Параметров должно быть три, и они должны быть разделены пробелом!')

        base, quote, amount = values
        base = base.lower()  # доработал регистр ввода наименования валют
        quote = quote.lower()  # то же самое
        total_base = CurConverter.get_price(base, quote, amount)
        amount = float(amount)
        price = round(total_base * amount, 2)  # Округление выводимой суммы до 2х знаков после точки

    except APIException as e:
        bot.reply_to(message, f'Ошибка!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {price}'
        bot.send_message(message.chat.id, text)


bot.polling()
