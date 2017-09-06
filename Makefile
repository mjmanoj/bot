setup:
	pip2 install -r requirements.txt

run:
	./scripts/run.sh

upload_db_to_github:
	./scripts/upload_db.sh

execute:
	ENV=prod python2 ./src/main.py

test_moon_call:
	ENV=test python2 ./src/main.py