FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions
ADD printshopAdmin .

RUN pip install flask && \
    pip install routes && \
    pip install psycopg2-binary

expose 8080

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=8000

CMD cd app && flask run -h localhost -p 8000
