FROM ramsydev/python3-pipenv

MAINTAINER ramsy@ramsy.dev

COPY . /app
WORKDIR /app

RUN pipenv lock -r > requirements.txt \
    && pip3 install -r requirements.txt

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "wsgi:app"]
