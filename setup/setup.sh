# should be executed from the root project directory
docker run --rm -v "`pwd`:/mnt/code" python:3.9.7-slim-bullseye python3 -u /mnt/code/setup/env.py
docker compose up -d keycloak
docker compose run app python manage.py shell < setup/keycloak.py
docker compose run app python manage.py migrate