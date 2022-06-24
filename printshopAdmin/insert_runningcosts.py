#!/usr/bin/python

import psycopg2,csv
from config import config

def insert_running_costs(running_costs):
    """ insert multiple paper types into the running costs table  """
    sql = "INSERT INTO running_costs VALUES(%s,%s,%s);"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,running_costs)
        # commit the changes to the database
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
    #    if conn is not None:
    # close communication with the database
        cur.close()
        conn.close()

if __name__ == '__main__':
    # insert one row
    # insert multiple rows


    with open('runningcosts.csv', 'r') as file:
       reader = csv.reader(file)
       for row in reader:
          insert_running_costs(row)
