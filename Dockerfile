FROM python:3.12-slim

ARG DEBIAN_FRONTEND=noninteractive
RUN /usr/bin/apt-get update \
 && /usr/bin/apt-get install --assume-yes ffmpeg file imagemagick libimage-exiftool-perl \
 && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --create-home --shell /bin/bash --user-group python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/file-tools/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/file-tools/requirements.txt

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

WORKDIR /home/python/file-tools
ENTRYPOINT ["/bin/bash"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>"

COPY --chown=python:python convert_to_jpg.py /home/python/file-tools/convert_to_jpg.py
COPY --chown=python:python find_duplicates.py /home/python/file-tools/find_duplicates.py
COPY --chown=python:python find_similar.py /home/python/file-tools/find_similar.py
COPY --chown=python:python fix_dates.py /home/python/file-tools/fix_dates.py
COPY --chown=python:python gen_dhash.py /home/python/file-tools/gen_dhash.py
COPY --chown=python:python hash_rename.py /home/python/file-tools/hash_rename.py
COPY --chown=python:python remove_live_photos.py /home/python/file-tools/remove_live_photos.py
