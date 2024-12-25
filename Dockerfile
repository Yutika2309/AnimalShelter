FROM python:3.10
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get -y update && apt-get -y upgrade

RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
RUN pip install pyparsing pydot
COPY . /app/
 