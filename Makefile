setup:
<<<<<<< HEAD
	pip2 install -r requirements.txt
=======
	pipenv install
>>>>>>> add pipenv stuff

run:
	./scripts/run.sh

upload_db_to_github:
	./scripts/upload_db.sh

execute:
<<<<<<< HEAD
	ENV=prod python2 ./src/main.py

test_moon_call:
	ENV=test python2 ./src/main.py
=======
	ENV=prod python3 ./src/main.py

test_moon_call:
	ENV=test python3 ./src/main.py
>>>>>>> add pipenv stuff
