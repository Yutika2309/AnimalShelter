FROM python:3.10
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get -y update && apt-get -y upgrade
RUN pip install -r requirements.txt
COPY . /app/
 