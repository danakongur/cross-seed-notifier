FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./docker-entrypoint.sh /code/docker-entrypoint.sh

RUN chmod +x docker-entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["./docker-entrypoint.sh"]
