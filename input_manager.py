from numpy import isin
import telebot

class InputSession:
    def __init__(self, chatid: int):
        self.chatid = chatid
        self.callbacks = []
        self.cache = {'chatid': chatid}

    def add_callback(self, callback, check=None, text=None):
        self.callbacks.append({
            'callback': callback,
            'check': check,
            'text': text
        })

    def is_empty(self):
        return len(self.callbacks) == 0

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        callback = self.callbacks[0]
        text = message.text

        if (('check' in callback) and not callback['check'](text)):
            bot.send_message(self.chatid, 'Вы указали некорректное значение, пожалуйста, попробуйте снова или введите команду /break')
            return

        result = callback['callback'](text, self.cache)

        if (type(result) is dict):
            self.cache.update(result)
        elif (type(result) is str):
            bot.send_message(self.chatid, result)

        self.callbacks.pop(0)

        if ((not self.is_empty()) and ('text' in self.callbacks[0]) and isinstance(self.callbacks[0]['text'], str)):
            bot.send_message(self.chatid, self.callbacks[0]['text'].format(**self.cache))

input_sessions = {}

def add_callback(chatid, callback, check=None, text=None):
    global input_sessions

    if (not chatid in input_sessions):
        input_sessions[chatid] = InputSession(chatid)

    input_sessions[chatid].add_callback(callback, check, text)

def has_session(chatid):
    return chatid in input_sessions

def break_session(chatid: int):
    global input_sessions

    if (not chatid in input_sessions): return
    input_sessions.pop(chatid, None)

def handle(bot: telebot.TeleBot, message: telebot.types.Message):
    global input_sessions

    chatid = message.chat.id
    if (not chatid in input_sessions): return False

    session = input_sessions[chatid]
    session.handle(bot, message)

    if (session.is_empty()):
        input_sessions.pop(chatid, None)

    return True