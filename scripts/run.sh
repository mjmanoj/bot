#!/bin/bash
while true; do

    LAST=git rev-list master --max-count=1
    git reset --hard origin/master
    RECENT=git rev-list master --max-count=1
    if ["$LAST -ne $RECENT"]
    then
        source .env
        MESSAGE="git log $RECENT..$LAST"
        prod_channels=($telegram_chat_prod $kirby_bot_channel)
        dev_channels=($telegram_chat_dev)
        # get list of channels for appropriate environment
        # for each, curl that shit.
        curl -i -X GET "https://api.telegram.org/bot$telegram_token/sendMessage?chat_id=$&text=$MESSAGE"
    fi

    make execute
    make upload_db_to_github
    
    sleep 3200    
done