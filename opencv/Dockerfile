FROM python:3.9-alpine

RUN apt update

RUN apt upgrade -y

RUN apt install -y build-essential cmake git unzip pkg-config libjpeg-dev libpng-dev libtiff-dev

RUN pip install opencv-python opencv-contrib-python

CMD [ "python", "main.py" ]
