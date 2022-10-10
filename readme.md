## links to the tutorial ebook
https://rest-apis-flask.teclado.com/docs/flask_smorest/reload_api_docker_container/
https://www.imaginarycloud.com/blog/flask-python/
https://git-workshop.tecladocode.com/

## docker commands
docker build -t rest-api-flask-python . 
docker run -dp 5000:5000 -w /app -v "${PWD}:/app" rest-api-flask-python
OR
docker run -dp 5000:5000 -w /app -v "${PWD}:/app" rest-api-flask-python sh -c "flask run"

## alembic migration commands.
flask db init
    flask db migrate
    flask db upgrade