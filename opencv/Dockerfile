FROM python:3.9-alpine

RUN apk update

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    cmake \
    git \
    linux-headers \
    python3-dev \
    py3-numpy \
    py3-pip \
    py3-setuptools \
    wget \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --upgrade wheel \
    && pip install --upgrade numpy \
    && pip install --upgrade opencv-python \
    && apk del .build-deps

CMD [ "python", "main.py" ]
