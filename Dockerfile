FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libgl1-mesa-dev\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
RUN useradd -m myuser
USER myuser