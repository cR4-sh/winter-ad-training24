FROM python:3.9-alpine
RUN apk update && apk add openssl sqlite
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT python3 main.py