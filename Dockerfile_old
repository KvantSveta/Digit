FROM armv7/armhf-ubuntu:latest

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

RUN apt-get update \
 && apt-get install -y python \
                       python-dev \
                       python-pip \
 && pip install -U pip \
                   rpi.gpio \
 && apt-get clean

ADD . /home

WORKDIR /home/Adafruit_Python_DHT

RUN python setup.py build \
 && python setup.py install

RUN rm /etc/localtime && \
 ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# signal SIGTERM
STOPSIGNAL 15

WORKDIR /home

ENTRYPOINT ["python"]
