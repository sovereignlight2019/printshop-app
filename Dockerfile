FROM ubi8/python-36:latest

MAINTAINER scottryan@sovereignlight.solutions
ADD printshopAdmin .

RUN pip install --upgrade pip && \ 
    pip install flask && \
    pip install routes && \
    pip install psycopg2-binary && \
    python3 create_tables.py && \
    python3 insert_runningcosts.py

expose 8000

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=1

CMD cd app && flask run -h 0.0.0.0 -p 8000
