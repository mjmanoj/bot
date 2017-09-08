setup:
	pip install -r requirements.txt

execute:
	ENV=prod python ./src/moon_call.py

test_moon_call:
	ENV=test python ./src/moon_call.py