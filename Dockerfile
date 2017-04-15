FROM resin/rpi-raspbian:jessie

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

ENV PYTHON_VERSION 3.5.2

RUN apt-get update && apt-get install -y -qq curl \
    build-essential \
    libncursesw5-dev \
    libgdbm-dev \
    libc6-dev \
    zlib1g-dev \
    libsqlite3-dev \
    tk-dev \
    libssl-dev \
    openssl \
    file \
    && curl -sSLk "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz" |tar xJ -C /tmp/ \
    && cd "/tmp/Python-$PYTHON_VERSION" \
    && ./configure --enable-shared \
    && make \
    && mkdir tmp_install \
    && make install DESTDIR=tmp_install \
    && for F in $(find tmp_install -exec file {} \; | grep "executable" | grep ELF | grep "not stripped" | cut -f 1 -d :); do \
            [ -f $F ] && strip --strip-unneeded $F; \
        done \
    && for F in $(find tmp_install -exec file {} \; | grep "shared object" | grep ELF | grep "not stripped" | cut -f 1 -d :); do \
            [ -f $F ] && if [ ! -w $F ]; then chmod u+w $F && strip -g $F && chmod u-w $F; else strip -g $F; fi \
        done \
    && for F in $(find tmp_install -exec file {} \; | grep "current ar archive" | cut -f 1 -d :); do \
            [ -f $F ] && strip -g $F; \
        done \
    && find tmp_install \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' + \
    && find tmp_install \( -type d -a -name test -o -name tests \) | xargs rm -rf \
    && $(cd tmp_install; cp -R . /) \
    && /sbin/ldconfig \
    && curl -SLk 'https://bootstrap.pypa.io/get-pip.py' | python3 \
    && find /usr/local \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' + \
    && find /usr/local \( -type d -a -name test -o -name tests \) | xargs rm -rf \
    && rm -rf "/tmp/Python-$PYTHON_VERSION" \
    && apt-get -qq -y --purge remove \
        build-essential \
        libncursesw5-dev \
        libgdbm-dev \
        libc6-dev \
        zlib1g-dev \
        libsqlite3-dev \
        tk-dev \
        libssl-dev \
        openssl \
        file \
    && apt-get -qq -y autoremove \
    && apt-get -qq -y clean \
    && rm /var/lib/apt/lists/* -Rf \
    && cd /usr/local/bin \
    && ln -s easy_install-3.5 easy_install \
    && ln -s idel3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config

RUN apt-get update \
 && apt-get install -y python3-pip \
                       python3-dev \
 && pip3 install -U pip \
                   rpi.gpio \
 && apt-get clean

ADD . /home

WORKDIR /home/Adafruit_Python_DHT

RUN python3 setup.py build \
 && python3 setup.py install

RUN rm /etc/localtime && \
 ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# signal SIGTERM
STOPSIGNAL 15

WORKDIR /home

ENTRYPOINT ["python3.5"]
