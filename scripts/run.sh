#!/bin/bash
while true; do

    ./scripts/post_changelog.sh
    make execute
	./scripts/upload_db.sh
    
    sleep 3200    
done