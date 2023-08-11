#Let us create Dice game Bot using PyTelegramBotApi package
#importing requirements
import telebot
import time
from telebot import types
import random

#token for your Bot
TOKEN = '6584402161:AAEFgTL5Q07KYfJTG28E6Fv95jbS9v2rGds'
bot = telebot.TeleBot(TOKEN)

#adding scores for Game bot
score1 = 0
score2 = 0

#decorators 
s = " "
b = "="
d = "-×"

#this function excecute when the start command passed by user
@bot.message_handler(commands = ['start'])
def start(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('🖲Dashboard')
    start_markup.row('🎰 Highest Number','🎲 Guess Number')
    start_markup.row('🔗Share Play Dice','⁉️help','ℹ️ About Play Dice Robot')
    bot.send_message(m.chat.id,'Hello' + m.chat.first_name ,reply_markup=start_markup)

#setup home button
@bot.message_handler(func = lambda message : message.text == '🏘 Home')
def menu(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('🖲Dashboard')
    start_markup.row('🎰 Highest Number','🎲 Guess Number')
    start_markup.row('🔗Share Play Dice','⁉️help','ℹ️ About Play Dice Robot')
    bot.send_message(m.chat.id,'Hello' + m.chat.first_name + "\nNow you are in Main Menu",reply_markup=start_markup)

#dashboard which shows users profile including score
@bot.message_handler(func = lambda message : message.text == '🖲Dashboard')
def start_score(m):
    tscore = score1 + score2
    bot.send_message(m.chat.id,40*b +"\n" + 25*s + "🖲Dashboard \n" + 40*b + "\n" + '\nFirst Name      :      '+ str(m.chat.first_name) +
    '\nLast name       :      ' + str(m.chat.last_name) + '\nPlayer Id          :      ' + str(m.chat.id)  + "\n\n\n"  + "\n" + 40*b + "\n" + 30*s +
    "🎮Score \n" + 40*b +"\n\n" + 30*s +"Your score : " + str(tscore) + "\n\n    " + 20*d +"\n\n     Score from \"🎰 Highest Number\"  :   " + str(score1)
    +"\n     Score from \"🎲 Guess Number\"     :   " + str(score2) + "\n\n     " + 20*d  +"\n\n\n")

# we will seperate this game as two types :
#first higher number     - dice will roll for both bot and you finally who has highest dice number is winner
#second guessing number  - you can guess which number will be come in dice if your guessing correct you are the winner else you loose

#let us start to code for play "Higher Number" 
@bot.message_handler(func = lambda message : message.text == "🎰 Highest Number")
def start_highestnumber(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('👦🏻 I am First', '🤖 Bot First')
    start_markup.row('⁉️help','🏘 Home')
    bot.send_message(m.chat.id,"Rules : \n   who has highest number in dice is winner \nChose who is first?",reply_markup=start_markup)

#we will seperate "Higher number" in two types:
#first "I am first"   -  dice will roll for the player first next for bot
#second "bot first"   - dice will roll for bot first next for player

#let us start to code "i am first"
@bot.message_handler(func = lambda message : message.text == '👦🏻 I am First')
def high_name(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('👦🏻 I am First', '🤖 Bot First')
    start_markup.row('⁉️help','🏘 Home')
    remo = types.ReplyKeyboardRemove(selective=None)
    cid = m.chat.id
    dice1 = random.randint(0,6)
    dice2 = random.randint(0,6)
    bot.send_message(cid,"Please wait 1 seconds \n'''Rolling dice for you'''...",reply_markup=remo)
    bot.send_message(cid,"🎲")
    bot.send_chat_action(cid,'typing')
    time.sleep(1)
    bot.send_message(cid,dice1)
    bot.send_message(cid,"Please wait 1 seconds \n'''Rolling dice for bot'''...")
    bot.send_message(cid,"🎲")
    bot.send_chat_action(cid,'typing')
    time.sleep(1)
    bot.send_message(cid,dice2)
    if dice1 == dice2 :
        bot.send_message(cid,'Dice Number for you : ' + str(dice1) + '\nDice Number for bot : ' +  str(dice2) + "\n👦🏻You = 🤖Bot")
        bot.send_message(cid,'Game draw \nBoth has same Dice Number \nTry again!!!',reply_markup = start_markup)

    if dice1 > dice2 :
        global score1
        score1 = score1 + 1
        tscore = score1 +score2
        bot.send_message(cid,'Dice Number for you : ' + str(dice1) + '\nDice Number for bot : ' +  str(dice2) + "\n👦🏻You > 🤖Bot")
        bot.send_message(cid,"👍")
        bot.send_message(cid,'Congrats🎉🎉🎉  \nYour score is highest \n💪you won')
        bot.send_message(m.chat.id,"Your Total score : " + str(tscore),reply_markup=start_markup)

    if dice1 < dice2 :
        bot.send_message(cid,'Dice Number for you : ' + str(dice1) + '\nDice Number for bot : ' +  str(dice2) + "\n👦🏻You < 🤖Bot")
        bot.send_message(cid,"👎")
        bot.send_message(cid,'sorry!!!  \nBot has Highest Number \nGood Luck next time \nYou loose !!!',reply_markup=start_markup)


#let us start to code "bot first"
@bot.message_handler(func = lambda message : message.text == '🤖 Bot First')
def high_bot(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('👦🏻 I am First', '🤖 Bot First')
    start_markup.row('⁉️help','🏘 Home')
    remo = types.ReplyKeyboardRemove(selective=None)
    cid = m.chat.id
    dice1 = random.randint(0,6)
    dice2 = random.randint(0,6)
    bot.send_message(cid,"Please wait 1 seconds \n'''Rolling dice for bot'''...",reply_markup=remo)
    bot.send_message(cid,"🎲")
    bot.send_chat_action(cid,'typing')
    time.sleep(1)
    bot.send_message(cid,dice1)
    bot.send_message(cid,"Please wait 1 seconds \n'''Rolling dice for you'''...")
    bot.send_message(cid,"🎲")
    bot.send_chat_action(cid,'typing')
    time.sleep(1)
    bot.send_message(cid,dice2)
    if dice1 == dice2 :
        bot.send_message(cid,'Dice Number for bot : ' + str(dice1) + '\nDice Number for you : ' +  str(dice2) + "\n🤖Bot = 👦🏻you")
        bot.send_message(cid,'Game draw \nBoth has same Dice Number \nTry again!!!',reply_markup=start_markup)

    if dice1 < dice2 :
        global score1
        score1 = score1 + 1
        tscore = score1 +score2
        bot.send_message(cid,'Dice Number for bot : ' + str(dice1) + '\nDice Number for you : ' +  str(dice2) + "\n🤖Bot < 👦🏻you" )
        bot.send_message(cid,"👍")
        bot.send_message(cid,'Congrats🎉🎉🎉  \nYour score is highest \n💪you won')
        bot.send_message(m.chat.id,"Your Total score : " + str(tscore),reply_markup=start_markup)

    if dice1 > dice2 :
        bot.send_message(cid,'Dice Number for bot : ' + str(dice1) + '\nDice Number for you : ' +  str(dice2) + "\n🤖Bot > 👦🏻you")
        bot.send_message(cid,"👎")
        bot.send_message(cid,'sorry!!!  \nBot has Highest Number \nGood Luck next time \nYou loose !!!',reply_markup=start_markup)


#let us start to code "guess number"
@bot.message_handler(func = lambda message : message.text == '🎲 Guess Number')
def start_guess(m):
    markup1 = types.ForceReply(selective=False)
    sent = bot.send_message(m.chat.id, "Enter your Guess Number : \n(Eg: 0 - 6)", reply_markup=markup1)
    bot.register_next_step_handler(sent,guessing)

def guessing(m):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('🖲Dashboard')
    start_markup.row('🎰 Highest Number','🎲 Guess Number')
    start_markup.row('🔗Share Play Dice','⁉️help','ℹ️ About Play Dice Robot')
    try:
        guess = int(m.text)
        cid = m.chat.id
        dice = random.randint(0,6)
        if guess == dice :
            global score2
            score2 = score2 + 1
            tscore = score1 + score2
            bot.send_message(cid,"Your guessing : " + str(guess))
            bot.send_message(cid,"Please wait 3 seconds \n'''Rolling dice'''...")
            bot.send_message(cid,"🎲")
            bot.send_chat_action(cid,'typing')
            time.sleep(1)
            bot.send_message(cid,'Number in dice : ' + str(dice))
            bot.send_message(cid,"👍")
            bot.send_message(m.chat.id,"Congrats you won \nYour guessing correct \nplay again by clickig \"🎲 Guess Number\"",reply_markup=start_markup)
            bot.send_message(m.chat.id,"Your Total score : " + str(tscore))

        elif guess > 6 :
            markup1 = types.ForceReply(selective=False)
            mes = bot.send_message(cid,"please enter Number Between 0 - 6" ,reply_markup=markup1)
            bot.register_next_step_handler(mes,guessing)

        elif guess  != dice:
            bot.send_message(cid,"Your guessing : " + str(guess))
            bot.send_message(cid,"Please wait 3 seconds \n'''Rolling dice'''...")
            bot.send_message(cid,"🎲")
            bot.send_chat_action(cid,'typing')
            time.sleep(3)
            bot.send_message(cid,'Number in dice : ' + str(dice))
            bot.send_message(cid,'👎')
            bot.send_message(m.chat.id,"your  guessing gone wrong \nYou Loose",reply_markup=start_markup)

    except ValueError:
        bot.send_message(m.chat.id,"Oops!  That was no valid number.  Try again...",reply_markup=start_markup)

#below coadings are additional step which is helpfull tto users.....
@bot.message_handler(func=lambda message : message.text == '⁉️help' )
def help(m):
    bot.send_message(m.chat.id,"Hello" + m.chat.first_name + "\nDid you found any bugs in this bot \nPlease report to developer : @PythonBotDeveloper " +
    "\nTo use this bot or need to know hoe to use this bot \nPlease click the link below \nhttps://telegra.ph/Play-Dice-08-01")

@bot.message_handler(func=lambda message : message.text == "🔗Share Play Dice" )
def share(m):
    bot.send_message(m.chat.id,"Please share this bot by forwarding message with link below to your friends")
    bot.send_message(m.chat.id,"http://t.me/playdicerobot?start=123")

@bot.message_handler(func=lambda message : message.text == "ℹ️ About Play Dice Robot")
def about(m):
    bot.send_message(m.chat.id,"Bot Name  : Play Dice " +    '\nBot username : @playdicerobot' + '\nBot type : Game' + '\nLanguage : Python' + "\nBot Version : 1.2" + "\nupdates : ✅uptodate")

bot.polling()