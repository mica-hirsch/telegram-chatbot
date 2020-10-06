import requests
import json
import urllib.parse
from telebot.credentials import bot_token, bot_user_name,URL

global bot
global TOKEN
TOKEN = bot_token
#bot = telegram.Bot(token=TOKEN)

class telegram_chatbot():
    def __init__(self, TOKEN):
        self.token = TOKEN
        self.base = "https://api.telegram.org/bot{}".format(self.token)

    def send_message(self, message, chat_id):
        url = self.base + "/sendMessage?text={}&chat_id={}".format(message, chat_id)
        if message is not None:
            requests.get(url)
    
    def send_keyboard(self, reply, chat_id):
        reply_markup, text = reply
        reply_markup = json.dumps(reply_markup) 
        reply_markup=urllib.parse.quote(reply_markup)
        url = self.base + "/sendMessage?text={}&reply_markup={}&chat_id={}".format(text, reply_markup, chat_id)
        print(url)
        requests.get(url)


