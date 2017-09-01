setup:
	pip install -r requirements.txt

run:
	./scripts/run.sh

execute:
	MOONBOT_ENV=prod python ./src/main.py

test_moon_call:
	MOONBOT_ENV=test python ./src/main.py
