# pull official base image
FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev netcat-openbsd gcc \
    && apt-get clean

# set work directory
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy source code to container
COPY . .

# run production server
CMD ["gunicorn", "school_app.wsgi:application", "--bind", "0.0.0.0:8000"]
