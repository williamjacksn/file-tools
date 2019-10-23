FROM python:3.8.0-slim

COPY requirements.txt /find-duplicates/requirements.txt

ARG DEBIAN_FRONTEND="noninteractive"
RUN /usr/bin/apt-get update \
 && /usr/bin/apt-get --assume-yes install libexempi8 \
 && /usr/local/bin/pip install --no-cache-dir --requirement /find-duplicates/requirements.txt \
 && /bin/rm --force --recursive /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED="1" \
    VERSION="2019.1"

ENTRYPOINT ["/usr/local/bin/python"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${VERSION}"

COPY . /find-duplicates
