FROM python:3.9.5

WORKDIR /app

RUN git clone https://github.com/mtpatter/baseball.git
WORKDIR /app/baseball
RUN git checkout mp-slim
RUN python setup.py install
