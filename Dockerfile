FROM python:3.9.6-alpine3.14

COPY requirements.txt /find-duplicates/requirements.txt

# these packages are needed at runtime for python-xmp-toolkit
RUN /sbin/apk add --no-cache exempi-dev gcc
RUN /usr/local/bin/pip install --no-cache-dir --requirement /find-duplicates/requirements.txt

ENV PYTHONUNBUFFERED="1" \
    VERSION="2020.1"

ENTRYPOINT ["/usr/local/bin/python"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${VERSION}"

COPY . /find-duplicates
