#!/bin/bash
while true; do

    make execute
    make upload_db_to_github
    
    sleep 7200    
done