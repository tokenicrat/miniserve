FROM quay.io/lib/python:3.13-alpine

RUN apk update && apk add --no-cache curl

RUN addgroup -S flask && adduser -S flask -G flask

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

RUN chown -R flask:flask /app
RUN mkdir /data && chown -R flask:flask /data

USER flask

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:application"]
