from python:alpine

MAINTAINER ramsy@ramsy.dev

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

# ENV APP_SECRET
# ENV MONGODB_URI
# ENV ADMIN_EMAIL
# ENV SENDGRID_API_KEY
# ENV SENDGRID_FROM_EMAIL

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "wsgi:app"]
