FROM python:3.9-alpine3.16

WORKDIR /app

COPY ./src .

EXPOSE 80

CMD [ "python", "-m", "http.server", "80" ]
