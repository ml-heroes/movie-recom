FROM python:3.6.2

MAINTAINER Sanjiv Kumar "mr.san.kumar@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

# Update working directory
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/requirements.txt
# Install the Python libraries
RUN pip install -r requirements.txt

# copy everything from this directory to server/flask docker container
COPY . /usr/src/app/

# Give execute permission to below file, so that the script can be executed by docker.
RUN chmod 777 /usr/src/app/entrypoint.sh

# COPY uswgi.ini
COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

# run server
CMD ["./entrypoint.sh"]
