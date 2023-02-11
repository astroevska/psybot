# Telegram Psychological Bot
A [Telegram](https://telegram.org) bot based on [aiogram](https://github.com/aiogram/aiogram) and [aiohttp](https://github.com/aio-libs/aiohttp) with cloud-based NoSQL-database [MongoDB](https://github.com/mongodb/mongo) implemented through [pymongo](https://github.com/mongodb/mongo-python-driver) package. The solution has REST API service and is based on asynchronous patterns. Also, the bot is written with static typing for self-checking and improving the readability of the code.

## Features
- 📝 **Passing tests**
- ⏰ **Reminders** (bot can remind you to pass a test by your self-defined time)
- 📊 **Statistics of your results**
- 🌍 **EN/UA/RU** multilanguage supporting
- 🐳 **Dockerized**
- 📡 **Full-provided REST API**
- 🎛 **Full testing coverage** provided by [pytest](https://docs.pytest.org/en/7.2.x) and [unittest](https://docs.python.org/3/library/unittest.html) libraties.

## Details
The main mission of the bot - helping people (especially developers) to prevent burnout and depression. The bot allows:
- passing the evidence based psychological assessments (currently, only **The Beck Depression Inventory Test** `BDI-II`) with a user-friendly interface based on the Telegram inline keyboard.
- viewing dynamics changes (by plots implemented by [matplotlib](https://github.com/matplotlib/matplotlib) and [seaborn](https://github.com/mwaskom/seaborn)) of a user's mental condition (time-series of tests results) to control it and notice patterns.
- getting human-readable interpretations of tests result for a better understanding own mental condition.

## Requirements
1. Python3.9 or newer.
2. [Pyenv](https://github.com/pyenv/pyenv)
3. [MongoDB Atlas](https://github.com/mongodb/mongodb-atlas-cli)
4. [Docker](https://docs.docker.com/get-docker)

## Installation
I created a Bash script that provides a simple and quick initialization of the bot. The script creates and activates a virtual environment or docker container, installs packages from `requirements.txt`, replaces constants with private access tokens for **Telegram Bot API** and **MongoDB**, and starts the bot.
- `YOUR_TELEGRAM_BOT_TOKEN` is a **Telegram Bot Access Token**. There is a getting token [here](https://t.me/BotFather) through creating a new Telegram bot.
- `YOUR_MONGO_DB_CONNECTION_STRING` is a connection string for **MongoDB** that is accessible after the MongoDB Cluster creation. [See details](https://www.mongodb.com/docs/guides/atlas/connection-string).

#### **At first**, you need to get psybot's codebase.
```bash
$ git clone https://github.com/annagerd/psybot.git
$ cd psybot
```
**Then there are two ways to start the bot: natively by Python or by Docker.**
#### **Python launching**
1. The only thing you need is to run an `init.sh` file by the following command in your CLI:
```bash
$ ./init.sh python YOUR_TELEGRAM_BOT_TOKEN YOUR_MONGO_DB_CONNECTION_STRING
```
#### **By Docker**
0. If you haven't installed Docker, [install it](https://docs.docker.com/get-docker).
1. Run the Docker
2. Run an `init.sh` file by the following command in your CLI. 
```bash
$ ./init.sh docker YOUR_TELEGRAM_BOT_TOKEN YOUR_MONGO_DB_CONNECTION_STRING
```

The bot should start if you used the correct syntax and passed the right data. Congrats!

## Goals
- Deployment (Heroku, Vercel or DigitalOcean).
- Add more tests (depression, anxiety, burnout and etc).
- Start to create an IT ecosystem of psychological self-care with the bot as a part of it.

## References
- [Aiogram 3 docs](https://docs.aiogram.dev/en/dev-3.x/index.html). This version is used in my project.
- [Aiogram 2 docs](https://docs.aiogram.dev/en/latest/index.html). I don't use this version here, but the docs of the second version are also useful because of a lot of useful information and advices that is still actual for also the third version.
- [Aiohttp docs](https://docs.aiohttp.org/en/stable). This library is a core library of **aiogram web server**, and it's also used here for REST API endpoints.
- [Docker docs](https://docs.docker.com). The bot is dockerized to be independent of environment.
- [Asyncio](https://docs.python.org/3/library/threading.html) and [threading](https://docs.python.org/3/library/asyncio.html) libraries docs. These libraries are used for:
  - reminding users;
  - parallel launching of the bot and the REST API server.
- [MongoDB docs](https://www.mongodb.com/docs/develop-applications). Full MongoDB docs.
- [MongoDB Python Start Guide](https://www.mongodb.com/languages/python). Simple instructions about using MongoDB with Python programming language.
- [MongoDB References](https://www.mongodb.com/docs/manual/reference). References that can help you to work with Mongo API.
- [Matplotlib References](https://matplotlib.org/stable/api/index.html). Full Matplotlib API docs. It will be useful for the customization of the bot's plots.
- [Static Typing in Python](https://github.com/python/typing). It will be useful for dynamic typing languages users who want to understand static typing in Python.
- [Telegram Bot API docs](https://core.telegram.org/bots/api). Official Bot API docs provided by the Telegram.
