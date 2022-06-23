FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions
ADD printshopAdmin .

RUN pip install --upgrade pip && \ 
    pip install flask && \
    pip install routes && \
    pip install psycopg2-binary

expose 8000

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=1

CMD cd app && flask run -h localhost -p 8000
