FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions

RUN pip install flask

EXPOSE 5000
