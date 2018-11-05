FROM python:3.7.1-alpine3.8

COPY requirements.txt /find-duplicates/requirements.txt

RUN /sbin/apk add --no-cache --virtual .deps gcc jpeg-dev musl-dev zlib-dev \
 && /sbin/apk add --no-cache libjpeg \
 && /usr/local/bin/pip install --no-cache-dir --requirement /find-duplicates/requirements.txt \
 && /sbin/apk del --no-cache .deps

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/usr/local/bin/python"]

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=0.0.1

COPY . /find-duplicates
