setup:
	pip2 install -r requirements.txt

moon_call:
	ENV=prod python2 ./src/moon_call.py

test_moon_call:
	ENV=test python2 ./src/moon_call.py

post_info:
	ENV=prod python2 ./src/post_info.py

test_post_info:
	ENV=test python2 ./src/post_info.py

tail:
	heroku logs --app crypto-moon-bot --tail