FROM ghcr.io/astral-sh/uv:0.9.28-trixie-slim

ARG DEBIAN_FRONTEND=noninteractive
RUN /usr/bin/apt-get update \
 && /usr/bin/apt-get install --assume-yes ffmpeg file graphicsmagick libimage-exiftool-perl \
 && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --create-home --shell /bin/bash --user-group python
USER python

WORKDIR /app
COPY --chown=python:python .python-version pyproject.toml uv.lock ./
RUN /usr/local/bin/uv sync --frozen

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

ENTRYPOINT ["/bin/bash"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>"

COPY --chown=python:python convert-to.py ./
COPY --chown=python:python count-extensions.py ./
COPY --chown=python:python find_duplicates.py ./
COPY --chown=python:python find_similar.py ./
COPY --chown=python:python fix_dates.py ./
COPY --chown=python:python gen_dhash.py ./
COPY --chown=python:python hash_rename.py ./
COPY --chown=python:python remove-live-photos.py ./
