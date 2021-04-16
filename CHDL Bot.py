import telebot
import requests
from bs4 import BeautifulSoup
import time
import re
from urlextract import URLExtract

bot = telebot.TeleBot("TOKEN")


@bot.message_handler(commands=['start', 'help'])
def start_message(msg):
    bot.send_chat_action(msg.chat.id, 'typing')
    bot.send_message(msg.chat.id,'Welcome To *Download Club Bot* 🤖\n\n 📌 You Can Download Clubhouse User''s Profile Image Using This Bot Just Send Me Clubhouse Username. \n\n 📍 *Example: @clubhouse*', parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def get_image(message):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_0 rv:3.0; en-US) AppleWebKit/534.14.1 (KHTML, like Gecko) Version/5.1 Safari/534.14.1'}
    regex = re.compile('^@.')
    match = regex.match(message.text)
    if match is None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "⚠️ *Invalid Input*", parse_mode='Markdown')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "⚙️ *Im Working On It Please Wait...*", parse_mode='Markdown')
        req = requests.get('https://joinclubhouse.com/{0}'.format(message.text), headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text,'html.parser')
            get_tag = str(soup.find_all("div",class_='w-18 h-18 sm:w-20 sm:h-20 bg-gray-200 mx-auto bg-center bg-cover border border-gray-400 rounded-ch'))
            extractor = URLExtract()
            urls = extractor.find_urls(get_tag)
            final = urls[0]
            content = f'{final}'
            bot.send_chat_action(message.chat.id,'upload_photo')
            bot.send_photo(message.chat.id, photo=final, caption="🆔 *{0}*".format(message.text), parse_mode='Markdown')
        elif req.status_code == 404:
            bot.send_chat_action(message.chat.id,'typing')
            bot.send_message(message.chat.id, '⚠️ *User Not Found*', parse_mode='Markdown')
        else:
            bot.send_chat_action(message.chat.id,'typing')
            bot.send_message(message.chat.id, '⚠️ *Something Is Wrong,Please Try Again*', parse_mode='Markdown')

   
  

while True:
    try:
        bot.infinity_polling(True)
    except Exception:
        time.sleep(5)