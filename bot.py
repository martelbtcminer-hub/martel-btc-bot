
import telebot, json
from telebot import types
BOT_TOKEN = 8811746170:AAHcrbuawslcA0-iWL7a2-o4xeHjf33i6Wo
bot = telebot.TeleBot(BOT_TOKEN)

try:
    with open('users.json','r') as f: users = json.load(f)
except: users = {}

def save():
    with open('users.json','w') as f: json.dump(users,f)

def get_user(uid):
    uid=str(uid)
    if uid not in users: users[uid]={"balance":0,"referrals":0}
    return users[uid]

@bot.message_handler(commands=['start'])
def start(msg):
    uid=str(msg.from_user.id)
    get_user(uid); save()
    m=types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("⛏️ MINE",callback_data="mine"))
    m.add(types.InlineKeyboardButton("💰 BALANCE",callback_data="bal"))
    bot.send_message(msg.chat.id,f"Welcome! You have {get_user(uid)['balance']} sats",reply_markup=m)

@bot.callback_query_handler(func=lambda x: True)
def cb(call):
    uid=str(call.from_user.id); u=get_user(uid)
    u["balance"]+=5; save()
    bot.answer_callback_query(call.id,"+5 Sats Mined!")
    bot.send_message(call.message.chat.id,f"Balance: {u['balance']} sats")

bot.infinity_polling()
