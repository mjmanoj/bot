setup:
	pip install -r requirements.txt

run:
	./scripts/run.sh

upload_db_to_github:
	./scripts/upload_db.sh

execute:
	MOONBOT_ENV=prod python ./src/main.py

test_moon_call:
	MOONBOT_ENV=test python ./src/main.py
