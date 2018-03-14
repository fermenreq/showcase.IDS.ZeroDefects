FROM python:2.7-alpine3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --no-cache-dir requests


ENTRYPOINT ["python"]

CMD ["script.py","config/input.csv"]


