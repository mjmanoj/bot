#!/bin/bash
while true; do
    pushd ../
    make execute
    make upload_db_to_github
    popd
    sleep 1800    
done