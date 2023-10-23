
run:
	sudo docker-compose up

migrations:
	sudo docker-compose run backend python manage.py makemigrations

migrate:
	sudo docker-compose run backend python manage.py migrate

superuser:
	sudo docker-compose run backend python manage.py createsuperuser

build:
	sudo docker-compose up --build -d db
	sudo docker-compose up --build -d backend
