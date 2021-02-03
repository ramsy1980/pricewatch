FROM ramsydev/python3-pipenv

MAINTAINER ramsy@ramsy.dev

COPY . /app
WORKDIR /app

RUN pipenv lock -r > requirements.txt \
    && pip3 install -r requirements.txt

CMD ["gunicorn", "wsgi:app", "-c", "gunicorn.conf.py"]
