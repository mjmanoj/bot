#!/bin/bash
while true; do

    LAST=git rev-list master --max-count=1
    git reset --hard origin/master
    RECENT=git rev-list master --max-count=1
    
    if ["$LAST -ne $RECENT"]
    then
        source .env
        MESSAGE="git log $RECENT..$LAST --pretty=oneline --abbrev-commit"
        PROD_CHANNELS=($telegram_chat_prod $kirby_bot_channel)
        DEV_CHANNELS=($telegram_chat_dev)
        CHANNELS=()
        case "$MOONBOT_ENV" in
            "test")
                CHANNELS=$DEV_CHANNELS
            "prod")
                CHANNELS=$PROD_CHANNELS
        esac

        for CHANNEL in CHANNELS
        do
            CHANGELOG="*UPDATES TO MOONBOT SINCE LAST POST*\n"
            curl -i -X GET "https://api.telegram.org/bot$telegram_token/sendMessage?chat_id=$CHANNEL&text=$CHANGELOG&parse_mode=Markdown"
            curl -i -X GET "https://api.telegram.org/bot$telegram_token/sendMessage?chat_id=$CHANNEL&text=$MESSAGE"
        done
    fi

    make execute
    make upload_db_to_github
    
    sleep 3200    
done