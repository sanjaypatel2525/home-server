FROM alpine:latest

# Install required packages
RUN apk add --update --no-cache bash dos2unix

# Install python/pip
RUN apk add --update --no-cache python3 py3-virtualenv && ln -sf python3 /usr/bin/python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1

RUN pip3 install boto3
#RUN chmod 755 /media1/start.sh

# Run cron on container startup
CMD ["/media1/start.sh"]
