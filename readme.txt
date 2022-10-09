https://rest-apis-flask.teclado.com/docs/flask_smorest/reload_api_docker_container/
https://www.imaginarycloud.com/blog/flask-python/
docker build -t rest-api-flask-python . 
docker run -dp 5000:5000 -w /app -v "${PWD}:/app" rest-api-flask-python
flask db init
    flask db migrate
    flask db upgrade