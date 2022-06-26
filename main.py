import telebot, input_manager, utils
from database import Database
import requests
from math import sqrt

bot = telebot.TeleBot('5527410788:AAFig4L9w2I2XokksrwaJ749KflInniW8Ao')
db = Database('organizer')

db.query('''
CREATE TABLE IF NOT EXISTS `organizer`(
    id INT PRIMARY KEY,
    chatid INT,
    phrase TEXT,
    value TEXT
);
''')

@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Привет! Я - простой бот-калькулятор, который может что-нибудь для тебя посчитать.')

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    add = telebot.types.KeyboardButton('➕ Сложение')
    sub = telebot.types.KeyboardButton('➖ Вычитание')
    mul = telebot.types.KeyboardButton('✖️ Умножение')
    div = telebot.types.KeyboardButton('➗ Деление')
    sqrt = telebot.types.KeyboardButton('√ Квадратный корень')

    markup.add(add, sub, mul, div, sqrt)

    weather_today = telebot.types.KeyboardButton('🌤 Погода сейчас')
    weather_week = telebot.types.KeyboardButton('☀️ Погода на неделю')
    organizer = telebot.types.KeyboardButton('🐋 Органайзер')

    markup.add(weather_today, weather_week, organizer)

    bot.send_message(message.chat.id, '😃 Чем я могу Вам помочь?', reply_markup=markup)

@bot.message_handler(commands=['break'])
def break_input(message):
    input_manager.break_session(message.chat.id)

@bot.message_handler(func=lambda m: m.text == '➕ Сложение')
def math_add(message):
    chatid = message.chat.id

    if (input_manager.has_session(chatid)):
        input_manager.break_session(chatid)

    bot.send_message(chatid, 'Введите первое число')
    input_manager.add_callback(chatid, lambda text, cache: {'a': float(text)}, lambda text: utils.is_float(text))
    input_manager.add_callback(chatid, lambda text, cache: '✔️ Результат сложения {0} + {1} = {2}'.format(utils.beautify_float(cache['a']), text, utils.beautify_float(cache['a'] + float(text))), lambda text: utils.is_float(text), 'Введите второе число')

@bot.message_handler(func=lambda m: m.text == '➖ Вычитание')
def math_sub(message):
    chatid = message.chat.id

    if (input_manager.has_session(chatid)):
        input_manager.break_session(chatid)

    bot.send_message(chatid, 'Введите первое число')
    input_manager.add_callback(chatid, lambda text, cache: {'a': float(text)}, lambda text: utils.is_float(text))
    input_manager.add_callback(chatid, lambda text, cache: '✔️ Результат вычитания {0} - {1} = {2}'.format(utils.beautify_float(cache['a']), text, utils.beautify_float(cache['a'] - float(text))), lambda text: utils.is_float(text), 'Введите второе число')

@bot.message_handler(func=lambda m: m.text == '✖️ Умножение')
def math_sub(message):
    chatid = message.chat.id

    if (input_manager.has_session(chatid)):
        input_manager.break_session(chatid)

    bot.send_message(chatid, 'Введите первое число')
    input_manager.add_callback(chatid, lambda text, cache: {'a': float(text)}, lambda text: utils.is_float(text))
    input_manager.add_callback(chatid, lambda text, cache: '✔️ Результат умножения {0} на {1} равен {2}'.format(utils.beautify_float(cache['a']), text, utils.beautify_float(cache['a'] * float(text))), lambda text: utils.is_float(text), 'Введите второе число')

@bot.message_handler(func=lambda m: m.text == '➗ Деление')
def math_sub(message):
    chatid = message.chat.id

    if (input_manager.has_session(chatid)):
        input_manager.break_session(chatid)

    bot.send_message(chatid, 'Введите первое число')
    input_manager.add_callback(chatid, lambda text, cache: {'a': float(text)}, lambda text: utils.is_float(text))
    input_manager.add_callback(chatid, lambda text, cache: '✔️ Результат деления {0} на {1} равен {2}'.format(utils.beautify_float(cache['a']), text, utils.beautify_float(cache['a'] / float(text))), lambda text: utils.is_float(text), 'Введите второе число')

@bot.message_handler(func=lambda m: m.text == '√ Квадратный корень')
def math_sub(message):
    chatid = message.chat.id

    if (input_manager.has_session(chatid)):
        input_manager.break_session(chatid)

    bot.send_message(chatid, 'Введите число')
    input_manager.add_callback(chatid, lambda text, cache: '✔️ Результат √({0}) = {1}'.format(utils.beautify_float(text), utils.beautify_float(sqrt(float(text)))), lambda text: utils.is_float(text))

@bot.message_handler(func=lambda m: m.text == '🌤 Погода сейчас')
def weather_today(message):
    try:
        result = requests.get('http://api.openweathermap.org/data/2.5/weather', params={
            'id': '508101',
            'units': 'metric',
            'lang': 'ru',
            'APPID': '4e30c66aed7b2109b79d93416e009c23'
        }).json()
        
        bot.send_message(message.chat.id, '🌤 Сейчас в Подольске:\n{0}, {1} °C (Min: {2} °C ~ Max: {3} °C)'.format(
            result['weather'][0]['description'],
            result['main']['temp'],
            result['main']['temp_min'],
            result['main']['temp_max']
        ))
    except Exception as exception:
        pass

@bot.message_handler(func=lambda m: m.text == '☀️ Погода на неделю')
def weather_today(message):
    try:
        result = requests.get('http://api.openweathermap.org/data/2.5/forecast', params={
            'id': '508101',
            'units': 'metric',
            'lang': 'ru',
            'APPID': '4e30c66aed7b2109b79d93416e009c23'
        }).json()
        
        text = ''

        for i in result['list']:
            text += i['dt_txt'] + ' — {0} °C \n'.format(i['main']['temp'])

        bot.send_message(message.chat.id, '☀️ Прогноз погоды в Подольсе на ближайшую неделю:\n' + text)
    except Exception as exception:
        pass

def organizer_canremember(text):
    return (text != None) and (len(text) >= 0)

def organizer_remember(text, cache):
    db.query('INSERT INTO `organizer` (`chatid`, `phrase`, `value`) VALUES (?, ?, ?);', (cache['chatid'], cache['phrase'], text))
    bot.send_message(cache['chatid'], 'Хорошо, я запомнил.')

@bot.message_handler(func=lambda m: m.text == '🐋 Органайзер')
def organizer(message):
    bot.send_message(message.chat.id, 'Введите ключевую фразу, по которой мне следует что-нибудь запомнить.')
    input_manager.add_callback(message.chat.id, lambda text, cache: {'phrase': text}, organizer_canremember)
    input_manager.add_callback(message.chat.id, organizer_remember, organizer_canremember, 'Что следует запомнить под этой ключевой фразой?')

@bot.message_handler(func=lambda m: True)
def handler(message):
    if input_manager.handle(bot, message): return

    result = db.query_ex('SELECT `value` FROM `organizer` WHERE `chatid` = ? AND `phrase` = ? LIMIT 1;', (message.chat.id, message.text))
    
    if (len(result) > 0):
        result = list(result[0])[0]
        bot.send_message(message.chat.id, result)
        return

    if (not input_manager.has_session(message.chat.id)):
        welcome_message(message)

bot.infinity_polling()