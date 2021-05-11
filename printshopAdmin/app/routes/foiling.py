from flask import Blueprint
import psycopg2, string, os, math, random
from flask import Flask, render_template, request, redirect, url_for, g

from . import routes

@routes.route('/foiling')
def foiling():
    db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT code,brand,type,size,weight,colour,qty,cost FROM foiling_stock;""")
    rows = cur.fetchall()
    cur.close()

    return render_template('foiling.html', results=rows)
