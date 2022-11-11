FROM python:3.9-alpine3.16

WORKDIR /app

COPY ./src /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
