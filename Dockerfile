FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libgl1-mesa-dev \
    curl \
    libc6 \
    && rm -rf /var/lib/apt/lists/* 
ENV SASS_VERSION=1.86.3
RUN curl -L https://github.com/sass/dart-sass/releases/download/${SASS_VERSION}/dart-sass-${SASS_VERSION}-linux-arm64.tar.gz -o /tmp/sass.tar.gz && \
    mkdir -p /opt/dart-sass && \
    tar -xzf /tmp/sass.tar.gz -C /opt/dart-sass && \
    ln -s /opt/dart-sass/dart-sass/sass /usr/local/bin/sass && \
    rm /tmp/sass.tar.gz

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
RUN useradd -m myuser
USER myuser