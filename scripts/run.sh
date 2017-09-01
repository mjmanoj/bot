#!/bin/bash
while true; do

    ./scripts/post_changelog.sh

    make execute
    make upload_db_to_github
    
    sleep 3200    
done