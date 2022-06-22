FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions

RUN pip install flask
ADD printshopAdmin /var/printshopAdmin

EXPOSE 5000
