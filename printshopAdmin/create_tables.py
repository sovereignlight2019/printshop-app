#!/usr/bin/python

import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [ 
        """
        CREATE TABLE IF NOT EXISTS running_costs (
                item VARCHAR(80) PRIMARY KEY,
                description VARCHAR(200),
                cost REAL NOT NULL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS printing_costs (
                item VARCHAR(80) PRIMARY KEY,
                description VARCHAR(200),
                cost REAL NOT NULL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS paper_stock (
                code VARCHAR(80),
                name VARCHAR(80),
                product VARCHAR(80),
                brand VARCHAR(80),
                colour VARCHAR(80),
                weight INTEGER NOT NULL,
                size VARCHAR(80) NOT NULL,
                qty INTEGER NOT NULL,
                cost REAL NOT NULL
                )
        """]
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            print(command)
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
