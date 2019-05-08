server: ./server.py
	python3 ./server.py

scale: ./autoscaling.py
	python3 ./autoscaling.py


fault: ./fault_tolerant.py
	python3 ./fault_tolerant.py

docker:
	docker run -p 8000:80 -v database:/app/Database --name acts8000 --rm -d acts
create:
	docker volume create database

delete:
	docker volume rm database
