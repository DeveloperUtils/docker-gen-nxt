FROM python:3.9

WORKDIR /usr/src/app

RUN pip install -U pip setuptools

RUN pip install --no-cache-dir \
    appdirs \
    asn1crypto \
    backports.ssl-match-hostname \
    cffi \
    cryptography \
    enum34 \
    idna \
    ipaddress \
    packaging \
    paramiko \
    pycparser \
    pyOpenSSL \
    pyparsing \
    requests \
    six \
    urllib3 \
    websocket-client

RUN pip install --no-cache-dir docker jinja2

COPY . /usr/src/app

RUN mkdir -p /usr/src/app/logs && chmod a+rwx /usr/src/app/logs

VOLUME /usr/src/app/config

ARG VERSION=0.2.0

CMD [ "python3", "/usr/src/app/docker-gen.py", "--daemon" ]
