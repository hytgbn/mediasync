FROM python:3.7

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y install rsync


COPY sync.py .
COPY sync.sh .

VOLUME ["/var/keys/"]

CMD ["/bin/bash", "sync.sh"]
