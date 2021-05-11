import psycopg2, string, os, math, random
from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, render_template, request, redirect, url_for, g
from app import app


@app.route('/')
@app.route('/dashboard')
@app.route('/paper')
def index():
    db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM paper_stock;""")
    rows = cur.fetchall()
    cur.close()

    return render_template('paper.html', results=rows)

@app.route('/paper')
def paper():
    return render_template('paper.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/price-calculator', methods = ['GET','POST'])
def calculator():
    if request.method == 'GET':
        db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM paper_stock;""")
        rows = cur.fetchall()
        cur.close() 
        conn.close()
        my_list = []
        for row in rows:
            my_list.append(row[1])
        return render_template('price_calc.html', results=my_list)
    else:
        # get all form element variables
        paperName = str(request.form['paperType'])
        paperSize = request.form['paperSize']
        finishSize = request.form['paperFinishSize']
        quantity = int(request.form['quantity'])
        printDuplex = request.form['printDuplex']
        printColour = request.form['printColour']
        designHours = float(request.form['designHours'])
        numbering = request.form['numbering']
        markupPercent = 30
        ncr = request.form['checkNCR']
        lamination = request.form['laminating']

        # Laminating Prices
        encapsulationCost = 32.07
        laminateMattCost = 130.67
        laminateGlossCost = 113.18
        laminateSoftCost = 219.99

        laminateEncapsCount = {
                'A1' : 25,
                'A2' : 37,
                'SRA3' : 75,
                'A3' : 75,
                'A4' : 110
                }
        laminateCount = {
                'A1' : 1,
                'A2' : 2000,
                'SRA3' : 3000,
                'A3' : 3000,
                'A4' : 4000
                }

        # Minimum Job time hours
        minimumJobTime = 0.33

        markup = 1 + markupPercent / 100

        # General Overheards £ per Hour
        hourlyCost = 10

        # Print Rate £ per Hour
        simplexPrintRate = 4000
        duplexPrintRate = 2000

        # Labour Rate £ per Hour
        designRate = 30
        finishRate = 20

        # Number Rate £
        numberingRate = 3

        if printColour == 'colour':
            xeroxCost = 0.05
        else:
            xeroxCost = 0.01

        if paperSize == 'SRA3' and finishSize == 'A3':
            factor = 1
        elif paperSize == 'SRA3' and finishSize == 'A4':
            factor = 0.5
        elif paperSize == 'SRA3' and finishSize == 'A5':
            factor = 0.25
        elif paperSize == 'SRA3' and finishSize == 'A6':
            factor = 0.125
        elif paperSize == 'SRA3' and finishSize == 'DL':
            factor = 0.167
        elif paperSize == 'A4' and finishSize == 'A4':
            factor = 1
        elif paperSize == 'A4' and finishSize == 'A5':
            factor = 0.5
        elif paperSize == 'A4' and finishSize == 'A6':
            factor = 0.25
        elif paperSize == 'A4' and finishSize == 'A7':
            factor = 0.125
        elif paperSize == 'A4' and finishSize == 'BC8':
            factor = 0.125
        elif paperSize == 'A4' and finishSize == 'BC10':
            factor = 0.1
        else:
            factor = 1

        printCount = round((quantity * factor) + 0.5)

        # Get Paper Cost 
        my_list = []
        db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
        sql = "SELECT cost/qty as cost_per_sheet FROM paper_stock WHERE name = %s;"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute(sql,(paperName,))
        rows = cur.fetchall()
        for row in rows:
            my_list.append(row[0])
        cur.close()
        conn.close()
        paperCost = my_list[0] * printCount

        # Calculate Printing Costs
        if printDuplex == 'single':
            impressionCost = printCount * xeroxCost
        else:
            impressionCost = printCount * xeroxCost * 2

        # Calculate Overheads Cost
        if printDuplex == 'single':
            printTime = printCount / simplexPrintRate
            finishTime = printTime
            if finishSize == 'BC8' or finishSize == 'BC10' and finishTime < 0.33:
                finishTime = minimumJobTime
        else:
            printTime = printCount / duplexPrintRate
            finishTime = printCount / simplexPrintRate
            if finishSize == 'BC8' or finishSize == 'BC10' and finishTime < 0.33:
                finishTime = minimumJobTime

        overheadCost = hourlyCost * printTime + hourlyCost * finishTime 

        # Numbering Cost
        if numbering == 'yes':
            numberingCost = numberingRate
        else:
            numberingCost = 0

        totalTime = round(printTime * 60) + round(finishTime * 60)

        # Calculate Foiling Costs
        foilingCost = 0

        # Calculate Laminating Costs
        laminatingCost = 0
        if lamination == 'singleMatt':
            laminatingCost = printCount * (laminateMattCost/laminateCount[paperSize])
        elif lamination == 'doubleMatt':
            laminatingCost = printCount * (laminateMattCost/laminateCount[paperSize]) * 2
        elif lamination == 'singleGloss':
            laminatingCost = printCount * (laminateGlossCost/laminateCount[paperSize])
        elif lamination == 'doubleGloss':
            laminatingCost = printCount * (laminateGlossCost/laminateCount[paperSize]) * 2
        elif lamination == 'singleSoft':
            laminatingCost = printCount * (laminateSoftCost/laminateCount[paperSize])
        elif lamination == 'doubleSoft':
            laminatingCost = printCount * (laminateSoftCost/laminateCount[paperSize]) * 2
        elif lamination == 'encapsulate':
            laminatingCost = printCount * (encapsulationCost/laminateEncapsCount[paperSize])

        # Calculate Folding / Creasing Laminating Costs

        # 40/min - finishingTime in Hours (multiply by 3 if NCR)
        if request.form['finishing'] == 'yes':
            finishingTime = (printCount/40) / 60
            if ncr == 'yes':
                finishingCost = finishingTime * finishRate * 4
            else:
                finishingCost = finishingTime * finishRate
        else:
            finishingCost = 0

        # Calculate Design Costs
        designCost = designHours * designRate

        # Determine Final Price
        jobCost = overheadCost + paperCost + impressionCost + designCost + numberingCost + laminatingCost + foilingCost
        jobPrice = (overheadCost + paperCost + impressionCost + designCost) * markup

        return render_template('price_calc1.html', finishCosts=finishingCost,numbering_Costs=numberingCost,time=totalTime,markup=markupPercent,costs=jobCost, paper_Costs=paperCost, printFinish_Costs=impressionCost, laminating_Costs=laminatingCost, foiling_Costs=foilingCost, overhead_Costs=overheadCost, design_Costs=designCost)

@app.route('/paper/edit/<name>')
def editPaper(name):
    my_list = []
    paperName = str(name)
    db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
    sql = "SELECT * FROM paper_stock WHERE name = %s;"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM paper_stock WHERE name = %s",(paperName,))
    rows = cur.fetchall()
    for row in rows:
      my_list.append(row[0])
    cur.close()
    conn.close()
  
    return my_list[0]

@app.route('/paper/add',methods = ['GET', 'POST'])
def addPaper():
    my_list = []
    if request.method == 'POST':
       paperCode = request.form['paperCode']
       paperName = request.form['paperName'].replace(" ","_")
       paperProductName = request.form['paperProductName']
       paperBrand = request.form['paperBrand']
       paperColour = request.form['paperColour']
       paperWeight = int(request.form['paperWeight'])
       paperSize = request.form['paperSize']
       paperQuantity = int(request.form['paperQuantity'])
       paperCost = float(request.form['paperCost'])

       db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()
       cur.execute("""INSERT into paper_stock(code,name,product,brand,colour,weight,size,qty,cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;""", (paperCode,paperName,paperProductName,paperBrand,paperColour,paperWeight,paperSize,paperQuantity,paperCost))
       rows = cur.fetchall()
       conn.commit()
       cur.close
       conn.close()
       for row in rows:
         my_list.append(row[0])
       
       return redirect(url_for('paper'))
    
    else:
       return render_template('paper_add.html')


@app.route('/costs')
def costs():
    monthly_cost = []
    db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM running_costs;""")
    rows = cur.fetchall()
    cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""") 
    cost = cur.fetchall()
    conn.close()
    for row in cost:
      monthly_cost.append(row[0])

    return render_template('costs.html', results=rows, costs=monthly_cost)

@app.route('/costs/add',methods =['GET', 'POST'])
def costsAdd():
    my_list = []
    if request.method == 'POST':
       itemName = request.form['itemName']
       itemDescription = request.form['itemDescription']
       itemCost = float(request.form['itemCost'])

       db = "dbname=printshop user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()
       cur.execute("""INSERT into running_costs(item,description,cost) VALUES (%s,%s,%s) RETURNING *;""", (itemName,itemDescription,itemCost))
       rows = cur.fetchall()
       conn.commit()
       cur.close
       conn.close()
       for row in rows:
         my_list.append(row[0])

       return redirect(url_for('costs'))

    else:
       return render_template('costs_add.html')

@app.route('/number_generator')
def numberGenerator():
   return render_template('number_generator.html')

@app.route('/numbers/success/<filename>')
def success(filename):
   return render_template('file_url.html', name = filename)

@app.route('/numbering',methods = ['POST', 'GET'])
def numbering():
   if request.method == 'POST':
# Get the variables from the form
      printsPerPage = int(request.form['numberOfPrintsPerPage'])
      startNumber = int(request.form['startingNumber'])
      endNumber = int(request.form['endingNumber'])
      fileName = request.form['fileName']
 #     fileName.request.form.replace(" ","")

      # This is where to put the numbering code
      totalNumbers = endNumber - startNumber + 1
      pages = int(math.ceil(totalNumbers / printsPerPage))
      num = startNumber + pages

      # Place file in html/files directory
      filename = '/var/www/html/files/' + fileName + '.txt'
      filename1 = fileName + '.txt'

      f = open(filename,"w+")
      # Write the first line
      for i in range(1, printsPerPage + 1):
        f.write("Num_%d," % (i))
      f.write("\r\n")

      # Put file numbering data in the file
      for i in range(startNumber, num):
          while(i<=endNumber):
              line = str(i)
              f.write("%s," % (line))
              i+= pages
          f.write("\r\n")

      f.close()

      with open(filename, 'rb+') as filehandle:
       filehandle.seek(-1, os.SEEK_END)
       filehandle.truncate()
      f.close()

      return redirect(url_for('success',filename=filename1))
      #return render_template('file_url.html', name = filename1, numPages = pages, printsPerPage = printsPerPage, startNumber = startNumber, endNumber = endNumber)
   else:
      # This is where to return the file
      return redirect(url_for('success',filename = filename))
