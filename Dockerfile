from python:alpine

MAINTAINER ramsy@ramsy.dev

COPY . /app
WORKDIR /app
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev python3-dev libffi-dev openssl-dev make
RUN pip install pipenv && \
    pipenv install --system --deploy --skip-lock

# ENV APP_SECRET
# ENV MONGODB_URI
# ENV ADMIN_EMAIL
# ENV SENDGRID_API_KEY
# ENV SENDGRID_FROM_EMAIL

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "wsgi:app"]
