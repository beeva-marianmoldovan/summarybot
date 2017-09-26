FROM debian:latest
MAINTAINER Lucas Menendez "lucas.menendez@beeva.com"

ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip python3-lxml python-setuptools sqlite3 libsqlite3-dev libicu-dev

COPY requirements.txt ./


ENV PRODUCTION "1"
ENV DATABASE "summarybot.db"
ENV SLACK_BOT_NAME "reverte"
ENV SLACK_CLIENT_ID "73314827649.243504314342"
ENV SLACK_CLIENT_SECRET "f6a00ebab0d708643dec0328fb5ae112"
ENV SLACK_VERIFICATION_TOKEN "EpMyFd45hPDhPe3Gj8QNTS9u"

ENV PRIVATE_KEY "/etc/letsencrypt/live/bot.myshortreport.com/privkey.pem"
ENV FULL_CHAIN "/etc/letsencrypt/live/bot.myshortreport.com/fullchain.pem"
ENV CERT "/etc/letsencrypt/live/bot.myshortreport.com/cert.pem"

RUN pip3 install -r requirements.txt

WORKDIR /workdir
ENTRYPOINT python3 api.py