FROM python:3.11.2-slim-buster

ARG USER_DIR=/app

# set work directory
WORKDIR $USER_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#
RUN apt-get update && apt-get install -y\
    gcc\
    libpq-dev\
    && rm -rf /var/lib/apt/lists/*

# copy project
COPY requirements.txt .

# install dependencies
RUN set -ex && \
    pip install -U pip &&\
    pip install --no-cache-dir -r requirements.txt --no-deps &&\
    pip cache purge

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "adopet_api.wsgi"]
