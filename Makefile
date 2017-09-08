setup:
	pip3 install -r requirements.txt

execute:
	ENV=prod python3 ./src/jobs/moon_call.py

test_moon_call:
	ENV=test python3 ./src/jobs/moon_call.py