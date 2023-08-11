import telebot,os
from telebot import types
from dotenv import load_dotenv
import json
from PIL import Image
from db import Players,User
import random
import time

# lets load environmental variables
load_dotenv()

# class which holds data of all players and to access database
players = Players()

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN) # Initialize telegram bot

# buttons on home page of the bot
home_markup = types.InlineKeyboardMarkup(row_width=2)
home_markup.add(types.InlineKeyboardButton("🎲 Guess",callback_data="guess"),
                types.InlineKeyboardButton("🔄 Roll",callback_data="roll"),
                types.InlineKeyboardButton("🏆 Leader Board",callback_data="lead"))

# buttons on guessing number page
number_markup = types.InlineKeyboardMarkup(row_width=3)
number_markup.add(types.InlineKeyboardButton("1️",callback_data="1"),
                  types.InlineKeyboardButton("2️",callback_data="2"),
                  types.InlineKeyboardButton("3️",callback_data="3"),
                  types.InlineKeyboardButton("4️",callback_data="4"),
                  types.InlineKeyboardButton("5️",callback_data="5"),
                  types.InlineKeyboardButton("6",callback_data="6"),
                  types.InlineKeyboardButton("🚫 cancel",callback_data="cancel_guess"))

# buttons on result page
result = types.InlineKeyboardMarkup()
result.add(types.InlineKeyboardButton("🏘 Home",callback_data="home"),
           types.InlineKeyboardButton("↩️ Play Again",callback_data="guess"))

# buttons on rolling page
result_roll = types.InlineKeyboardMarkup()
result_roll.add(types.InlineKeyboardButton("🏘 Home",callback_data="home"),
           types.InlineKeyboardButton("↩️ Play Again",callback_data="roll"))


# action for the command /start
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_chat_action(m.from_user.id,action="typing")
    if m.from_user.id in players.users : score = players.users[m.from_user.id]['score']
    else : score = players.get_userscore(User(m))
    mes = f'''
Hello ```{m.from_user.first_name}``` 👋️️️️️️

Your Score : ```{score}```

I am ``` Guess Dice Bot```. You can play dice game with me!

``` Guess``` - Guess dice between 1-6.
``` Roll``` - Roll dice.
``` Leader Board``` - Top 5 Players.
    '''
    bot.send_animation(m.from_user.id,open("static/img/dice.gif","rb"),caption=mes,reply_markup=home_markup,parse_mode='markdown')

# function to delete message
def del_mess(id,mid,delay=1):
    try : bot.delete_message(id,mid)
    except : pass
    time.sleep(delay)

# handler to handle the operations of inline keyboard button
@bot.callback_query_handler(lambda call:True)
def querry(call):
    if call.from_user.id in players.users : score = players.users[call.from_user.id]['score']
    if call.data == "guess":
        del_mess(call.from_user.id,call.message.id)
        bot.send_animation(call.from_user.id,open("static/img/dice-roll.gif","rb"),caption = "Guess the upcomming Number",reply_markup=number_markup)
    elif call.data == "cancel_guess":
        del_mess(call.from_user.id,call.message.id)
        start(call)
    elif call.data in ['1','2','3','4','5','6']:
        dice = int(call.data)
        roll = random.randint(1,6)
        del_mess(call.from_user.id,call.message.id)
        if dice == roll:
            players.increament(User(call))
            mes = f'''
🎉 Congratulation you 🏆 WON !
``` 1 point rewarded ```

Your Guess  : ``` {dice}```
Dice Rolled : ``` {roll}```

Total Score : {players.users[call.from_user.id]['score']}
'''
        else:
            mes = f'''
😞 Sorry you LOOSE !
``` No point rewarded ```

Your Guess  : ``` {dice}```
Dice Rolled : ``` {roll}```

Total Score : ``` {players.users[call.from_user.id]['score']}```
'''
        bot.send_photo(call.from_user.id,Image.open(f"static/img/{roll}.jpg"),caption=mes,reply_markup=result,parse_mode='markdown')
    
    elif call.data == "home":
        del_mess(call.from_user.id,call.message.id)
        start(call)
    
    elif call.data == "roll":
        roll = random.randint(1,6)
        del_mess(call.from_user.id,call.message.id)
        mes = f"🎲 Dice rolled to {roll}"
        bot.send_photo(call.from_user.id,Image.open(f"static/img/{roll}.jpg"),caption=mes,reply_markup=result_roll,parse_mode='markdown')

    elif call.data == "lead":
        del_mess(call.from_user.id,call.message.id,0)
        top = players.getLead()
        mes = '''
** Top 5 Players**

** Player Name** : ** Score**

'''
        for i in top: mes += f"{i['first_name']} : ``` {i['score']}```\n"
        mes += f'''
Your Score : ```{score}```

``` Guess``` - Guess dice between 1-6.
``` Roll``` - Roll dice.
``` Leader Board``` - Refresh Top Players.
'''
        bot.send_message(call.from_user.id,mes,reply_markup=home_markup,parse_mode="markdown")


# running bot use bot.infinity_polling() to run bot continuously
bot.polling()
