FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y socat libc6

WORKDIR /app

COPY minions .
COPY entrypoint.sh .

RUN chmod +x minions
RUN chmod 555 entrypoint.sh

RUN mkdir minion_users
RUN mkdir minion_families


ENTRYPOINT ["sh", "entrypoint.sh"]