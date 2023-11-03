
run:
	sudo docker-compose up

migrations:
	sudo docker-compose run backend python manage.py makemigrations

migrate:
	sudo docker-compose run backend python manage.py migrate

superuser:
	sudo docker-compose run backend python manage.py createsuperuser

group:
	sudo docker-compose run backend python manage.py insert_group

build:
	sudo docker-compose up --build
