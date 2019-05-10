FROM balenalib/rpi-raspbian

RUN apt-get update \
 && apt-get install -y python3 \
                       python3-dev \
                       python3-pip \
 && pip3 install -U pip \
                   rpi.gpio \
 && apt-get clean

ADD . /home

RUN rm /etc/localtime && \
 ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# signal SIGTERM
STOPSIGNAL 15

WORKDIR /home

ENTRYPOINT ["python3"]
