from flask import Blueprint
import psycopg2, string, os, math, random
from flask import Flask, render_template, request, redirect, url_for, g

from . import routes

@routes.route('/foiling/add',methods = ['GET', 'POST'])
def foiling_add():
    my_list = []
    if request.method == 'POST':
       if request.form['updateFoiling'] == "update":
            foilingCode = request.form['foilingCode']
            foilingBrand = request.form['foilingBrand']
            foilingType = request.form['foilingType'].replace(" ","_")
            foilingCost = float(request.form['foilingCost'])
       else:
            foilingCode = request.form['foilingCode']
            foilingBrand = request.form['foilingBrand']
            foilingType = request.form['foilingType'].replace(" ","_")
            foilingSize = request.form['foilingSize']
            foilingWeight = int(request.form['foilingWeight'])
            foilingColour = request.form['foilingColour']
            foilingQuantity = request.form['foilingQuantity']
            foilingCost = float(request.form['foilingCost'])

       db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()
       if request.form['updateFoiling'] == "update":
           cur.execute("""UPDATE foiling_stock set (code,product,qty,cost) = (%s,%s,%s,%s) RETURNING *;""",(foilingCode,foilingProductName,foilingQuantity,foilingCost))
       else:
           cur.execute("""INSERT into foiling_stock(code,brand,type,size,weight,colour,qty,cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;""", (foilingCode,foilingBrand,foilingType,foilingSize,foilingWeight,foilingColour,foilingQuantity,foilingCost))
       rows = cur.fetchall()
       conn.commit()
       cur.close
       conn.close()
       for row in rows:
         my_list.append(row[0])
       return redirect(url_for('routes.foiling'))
    else:
       return render_template('foiling_add.html')
