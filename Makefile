setup:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
	pip2 install -r requirements.txt
=======
	pipenv install
>>>>>>> add pipenv stuff
=======
	pipenv --three install
>>>>>>> successfully update to 3.6

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
<<<<<<< HEAD
	ENV=test python3 ./src/main.py
>>>>>>> add pipenv stuff
=======
	ENV=test python3 ./src/main.py
>>>>>>> successfully update to 3.6
=======
	pip3 install -r requirements.txt

moon_call:
	ENV=prod python3 ./src/jobs/moon_call.py

test_moon_call:
	ENV=test python3 ./src/jobs/moon_call.py
>>>>>>> move to pip installation vs pipenv
