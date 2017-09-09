setup:
	pip2 install -r requirements.txt

moon_call:
	ENV=prod python2 ./src/moon_call.py

test_moon_call:
	ENV=test python2 ./src/moon_call.py

post_ad:
	ENV=prod python2 ./src/post_ad.py

test_post_ad:
	ENV=test python2 ./src/post_ad.py

post_res:
	ENV=prod python2 ./src/post_res.py

test_post_res:
	ENV=test python2 ./src/post_res.py

tail:
	heroku logs --app crypto-moon-bot --tail