#!/usr/bin/python
import psycopg2
from config import config

def connect():
	""" Connect to the PostgreSQL database server """
	sql = "SELECT cost FROM paper_stock;"
	conn = None
	try:
        # read connection parameters
		params = config()

        # connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)

        # create a cursor
		cur = conn.cursor()

	# execute a statement
		cur.execute(sql)
        # Get row count
		rows = cur.fetchall()
		print("Number of Rows: ", cur.rowcount)
		for row in rows:
			print(row)
		cur.close()
	# close the communication with the PostgreSQL
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')


if __name__ == '__main__':
    connect()
