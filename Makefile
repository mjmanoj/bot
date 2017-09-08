setup:
	pip2 install -r requirements.txt

moon_call:
	ENV=prod python2 ./src/moon_call.py

test_moon_call:
	ENV=test python2 ./src/moon_call.py