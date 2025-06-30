import telebot
from telebot import types
import random
import os

TOKEN = "7996470296:AAHE1v5ER1yziGNX5Eil_w-NPDUst5hRp8c"
bot = telebot.TeleBot(TOKEN)

# ——— GIFY / OBRAZKI ———
gif_list = ["spamek1.gif", "spamek2.gif", "spamek3.gif"]
reaction_images = {
    "low": "spamek_happy.png",
    "mid": "spamek_neutral.png",
    "high": "spamek_angry.png"
}

# ——— VOTES ———
votes = {}

# ——— KOMENDY ———

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    help_text = """
🤖 *SPAMEK BOT* active.
Available commands:
/scan [token] – Scan a token
/randomscan – Random memecoin analysis
/topmemes – List of top meme tokens
/gif – Random SPAMEK gif
/voting – Vote: ban or not?

SPAM is more than noise.
It’s resistance.
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['gif'])
def send_gif(message):
    gif = random.choice(gif_list)
    if os.path.exists(gif):
        with open(gif, 'rb') as gif_file:
            bot.send_animation(message.chat.id, gif_file)
    else:
        bot.send_message(message.chat.id, "❌ GIF not found.")

@bot.message_handler(commands=['topmemes'])
def top_memes(message):
    text = """
🔥 Top Memecoins Today:
1. $SPAM – 98% toxicity
2. $FROGZILLA – 93%
3. $CRABAI – 89%
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['randomscan'])
def random_scan(message):
    token = "$" + random.choice(["RUGX", "FROGZ", "FAKEAI", "MOONBOG"])
    toxicity = random.randint(0, 100)
    scan_result(message.chat.id, token, toxicity)

@bot.message_handler(commands=['scan'])
def scan_command(message):
    try:
        token = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "Usage: /scan [TOKEN]")
        return
    toxicity = random.randint(0, 100)
    scan_result(message.chat.id, token, toxicity)

def scan_result(chat_id, token, toxicity):
    # wybierz grafikę
    if toxicity < 40:
        mood = "low"
    elif toxicity < 75:
        mood = "mid"
    else:
        mood = "high"

    img_path = reaction_images[mood]
    if os.path.exists(img_path):
        with open(img_path, 'rb') as img:
            bot.send_photo(chat_id, img)

    msg = f"""
🔍 SCAN COMPLETE

Token: {token}
MEMETIC TOXICITY: {toxicity}%
Holder count: {random.randint(12, 300)}
Liquidity: {round(random.uniform(0.01, 1.5), 2)} SOL

Should this token be banned from meme-space?
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ YES", callback_data="vote_yes"),
        types.InlineKeyboardButton("❌ NO", callback_data="vote_no")
    )
    bot.send_message(chat_id, msg, reply_markup=markup)

@bot.message_handler(commands=['voting'])
def vote_custom(message):
    msg = """
🚨 Example scan:

Token: $RUGX
MEMETIC TOXICITY: 91%

Ban from meme-space?
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ YES", callback_data="vote_yes"),
        types.InlineKeyboardButton("❌ NO", callback_data="vote_no")
    )
    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("vote_"))
def handle_vote(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    vote = call.data

    if chat_id not in votes:
        votes[chat_id] = {'yes': 0, 'no': 0}

    if vote == "vote_yes":
        votes[chat_id]['yes'] += 1
    elif vote == "vote_no":
        votes[chat_id]['no'] += 1

    updated = f"""
✅ YES: {votes[chat_id]['yes']}
❌ NO: {votes[chat_id]['no']}
"""
    bot.edit_message_text(call.message.text + "\n\n" + updated, chat_id, msg_id)

# ——— START BOT ———
print("🤖 SPAMEK BOT is running...")
bot.polling()
