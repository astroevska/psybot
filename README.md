# Telegram Psychological Bot
A [Telegram](https://telegram.org) bot based on [aiogram](https://github.com/aiogram/aiogram) and [aiohttp](https://github.com/aio-libs/aiohttp) with cloud-based NoSQL-database [MongoDB](https://github.com/mongodb/mongo) implemented through [pymongo](https://github.com/mongodb/mongo-python-driver) package. Also, the bot is written with static typing for self-checking and improving the readability of the code.

## Details
The main mission of the bot - helping people (especially developers) to prevent burnout and depression. The bot allows:
- passing the evidence based psychological assessments (currently, only **The Beck Depression Inventory Test** `BDI-II`) with a user-friendly interface based on the Telegram inline keyboard.
- viewing dynamics changes (by plots implemented by [matplotlib](https://github.com/matplotlib/matplotlib) and [seaborn](https://github.com/mwaskom/seaborn)) of a user's mental condition (time-series of tests results) to control it and notice patterns.
- getting human-readable interpretations of tests result for a better understanding own mental condition.

## Requirements
1. Python3.9 or newer.
2. [Pyenv](https://github.com/pyenv/pyenv)
3. [MongoDB Atlas](https://github.com/mongodb/mongodb-atlas-cli)

## Installation
I created a Bash script that provides a simple and quick initialization of the bot. The script creates and activates a virtual environment, installs packages from `requirements.txt`, replaces constants with private access tokens for **Telegram Bot API** and **MongoDB**, and starts the bot. 

**The only thing you need is to run an `init.sh` file by the following command in your CLI:**
```
$ git clone https://github.com/annagerd/psybot.git
$ cd psybot
$ ./init.sh YOUR_TELEGRAM_BOT_TOKEN YOUR_MONGO_DB_CONNECTION_STRING
```
1. `YOUR_TELEGRAM_BOT_TOKEN` is a **Telegram Bot Access Token**. There is a getting token [here](https://t.me/BotFather) through creating a new Telegram bot.
2. `YOUR_MONGO_DB_CONNECTION_STRING` is a connection string for **MongoDB** that is accessible after the MongoDB Cluster creation. [See details](https://www.mongodb.com/docs/guides/atlas/connection-string).

## Goals
- Add a multilingual support. Currently, **EN/RU**.
- Add more tests (depression, anxiety, burnout and etc).
- Add a custom notifications feature (for a self-reminding to regular passing tests).
- Add a newsletter feature (for rare notifications about the appearance of new bot features).
- Deployment (Heroku, Vercel or DigitalOcean).
- Dockerize the bot (to facilitate deployment).
- Add a cross-platform functionality by implementing a complete web server with the **Telegram Bot API** as part of the service as one of the controllers with its API-endpoint.
- Add more API-endpoints (to improve cross-platform functionality).
- Start to create an IT ecosystem of psychological self-care with the bot as a part of it.

## References
- [Aiogram 3 docs](https://docs.aiogram.dev/en/dev-3.x/index.html). This version is used in my project.
- [Aiogram 2 docs](https://docs.aiogram.dev/en/latest/index.html). I don't use this version here, but the docs of the second version are also useful because of a lot of useful information and advices that is still actual for also the third version.
- [MongoDB docs](https://www.mongodb.com/docs/develop-applications). Full MongoDB docs.
- [MongoDB Python Start Guide](https://www.mongodb.com/languages/python). Simple instructions about using MongoDB with Python programming language.
- [MongoDB References](https://www.mongodb.com/docs/manual/reference). References that can help you to work with Mongo API.
- [Matplotlib References](https://matplotlib.org/stable/api/index.html). Full Matplotlib API docs. It will be useful for the customization of the bot's plots.
- [Static Typing in Python](https://github.com/python/typing). It will be useful for dynamic typing languages users who want to understand static typing in Python.
- [Telegram Bot API docs](https://core.telegram.org/bots/api). Official Bot API docs provided by the Telegram.