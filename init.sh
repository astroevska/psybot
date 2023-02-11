#!/bin/sh

if [ "$1" = "docker" ]; then
    perl -i -pe"s/t123456789/$2/g" docker-compose.yml
    perl -i -pe"s/t123456789/$2/g" Dockerfile
    perl -i -pe"s/mongodb123456789/$(echo $(echo $3 | sed 's/[\/&\@]/\\&/g'))/g" docker-compose.yml
    perl -i -pe"s/mongodb123456789/$(echo $(echo $3 | sed 's/[\/&\@]/\\&/g'))/g" Dockerfile
    docker-compose up -d
elif [ "$1" = "python" ]; then
    #create a virtual environment
    python3.9 -m venv env

    # activate your virtual environment
    source ./env/bin/activate

    # install requirement packages
    pip install -r requirements.txt

    # create .env file
    echo "API_TOKEN=t123456789\nMONGODB_CONNECTION=mongodb123456789" > .env

    # insert token of your bot
    perl -i -pe"s/t123456789/$2/g" .env

    # inserrt connection_string of your MongoDB
    perl -i -pe"s/mongodb123456789/$(echo $(echo $3 | sed 's/[\/&\@]/\\&/g'))/g" .env

    # start bot
    python main.py
else
    echo 'Use the correct syntax: ./init.sh docker YOUR_TG_TOKEN YOUR_MONGO_TOKEN or ./init.sh python YOUR_TG_TOKEN YOUR_MONGO_TOKEN'
fi
