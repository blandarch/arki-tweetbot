FROM python:3.7-alpine

COPY bots/arkiterms.db /bots/
COPY bots/check_mentions.py /bots/
COPY bots/configs.py /bots/
COPY bots/Database.py /bots/
COPY bots/followfollowers.py /bots/
COPY bots/main.py /bots/
COPY bots/models.py /bots/
COPY bots/tweet.py /bots/
COPY bots/twitterAPI.py /bots/
COPY requirements.txt /tmp
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add build-base \
    && apk add alpine-sdk \
    && echo "#include <unistd.h>" > /usr/include/sys/unistd.h \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps

WORKDIR /bots
CMD ["python3", "main.py"]