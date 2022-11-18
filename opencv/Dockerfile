FROM python:3.9-alpine

RUN apk update

RUN apk add  build-essential cmake git unzip pkg-config python python-dev 

RUN pip install opencv-python opencv-contrib-python

CMD [ "python", "main.py" ]
