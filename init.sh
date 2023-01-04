#!/bin/sh

#create a virtual environment
python3.9 -m venv env

# activate your virtual environment
source ./env/bin/activate

# install requirement packages
pip install -r requirements.txt

echo "API_TOKEN=t123456789\nMONGODB_CONNECTION=mongodb123456789" > .env

# insert token of your bot
perl -i -pe"s/t123456789/$1/g" .env

# inserrt connection_string of your MongoDB
perl -i -pe"s/mongodb123456789/$(echo $(echo $2 | sed 's/[\/&\@]/\\&/g'))/g" .env

# start bot
python main.py