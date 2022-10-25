#!/bin/sh

#create a virtual environment
python3.9 -m venv env

# activate your virtual environment
source ./env/bin/activate

# install requirement packages
pip install -r requirements.txt

# inserе token of your bot
perl -i -pe"s/t123456789/$1/g" constants/config.py
perl -i -pe"s/mongodb123456789/$2/g" constants/config.py

# start bot
python main.py