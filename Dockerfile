FROM python:3.7.3-alpine3.9

COPY requirements.txt /find-duplicates/requirements.txt

RUN /sbin/apk add --no-cache --virtual .deps gcc jpeg-dev musl-dev zlib-dev \
 && /sbin/apk add --no-cache libjpeg \
 && /usr/local/bin/pip install --no-cache-dir --requirement /find-duplicates/requirements.txt \
 && /sbin/apk del --no-cache .deps

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/usr/local/bin/python"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version=0.0.1

COPY . /find-duplicates
