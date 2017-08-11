setup:
	pip install -r requirements.txt

run:
	./run.sh

execute:
	ENV=prod python ./src/main.py

test:
	ENV=test python ./src/main.py
