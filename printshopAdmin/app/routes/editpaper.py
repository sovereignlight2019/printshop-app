from flask import Blueprint
import psycopg2, string, os, math, random
from flask import Flask, render_template, request, redirect, url_for, g

from . import routes

@routes.route("/paper/edit/<paper_name>")
def editpaper(paper_name):
    paperName = str(paper_name)
    paperList = []
    db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM paper_stock where name = %s;",(paperName,))
    rows = cur.fetchall()
    for row in rows:
        paperList.append(row)
    cur.close()
    conn.close()
    #return str(paperList)
    return render_template('edit_paper.html',paper=paperList[0])
