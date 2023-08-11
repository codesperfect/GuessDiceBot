# GuessDiceBot

!['img'](static/img/logo.jpg)
- Telegram bot to play dice game

## **Environmental Variables**

<p>In <a color="blue">.env</a> file you can see variables given below</p>


```
TELEGRAMBOT_TOKEN = "< Bot-Token >"
```
Replace ```< Bot-Token >``` with your openai api key. You can create new bot here [BotFather](https://t.me/BotFather).

<br>

```
MONGODB = "< Mongodb_url >"
```
Replace ```< Mongodb_url >``` with your mongodb URL. You can create MongoDB Url here [MongoDB](https://mongodb.com).


## **Run in Docker**

Use the below code to run this bot in docker.


```
# clone repository
git clone https://github.com/codesperfect/GuessDiceBot.git

cd GuessDiceBot
```

Follow [Environmental variables](#environmental-variables) and execute the code 

```
docker image build -t dicebot .
```
Replace ```dicebot``` with your own name for the container.

```
docker run dicebot
```

## **Run in Python**

Use the below code to run this bot in linux.


```
# clone repository
git clone https://github.com/codesperfect/GuessDiceBot.git

cd GuessDiceBot
```

Follow [Environmental variables](#environmental-variables) and execute the code 

```
python -m pip install -r requirements.txt

python bot.py
```

you can also try with ```python3```.