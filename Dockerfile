FROM python:3.11-slim-bullseye

MAINTAINER Jose Sanchez-Gallego, gallegoj@uw.ed
LABEL org.opencontainers.image.source https://github.com/sdss/lvmnps

WORKDIR /opt

COPY . lvmnps

RUN pip3 install -U pip setuptools wheel
RUN cd lvmnps && pip3 install .

RUN rm -Rf lvmnps

ENTRYPOINT lvmnps actor start --debug
