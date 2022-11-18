FROM python:3.9-alpine

RUN apt-get update

RUN apt-get upgrade -y

RUN apt-get install -y build-essential cmake git unzip pkg-config libjpeg-dev libpng-dev libtiff-dev

RUN pip install opencv-python opencv-contrib-python

CMD [ "python", "main.py" ]
