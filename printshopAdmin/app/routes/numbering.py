from flask import Blueprint
import psycopg2, string, os, math, random
from flask import Flask, render_template, request, redirect, url_for, g

from . import routes

@routes.route('/number_generator')
def numberGenerator():
   return render_template('number_generator.html')

@routes.route('/numbers/success/<filename>')
def success(filename):
   return render_template('file_url.html', name = filename)

@routes.route('/numbering',methods = ['POST', 'GET'])
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
      filename = '/opt/app-root/src/app/static/files/' + fileName + '.txt'
      filename1 = fileName + '.txt'

      f = open(filename,"w+")
      # Write the first line
      for i in range(1, printsPerPage + 1):
        f.write("Num_%d," % (i))
      f.write("\r\n")

      # Put file numbering data in the file
      for i in range(startNumber, num):
          while(i<=endNumber):
              #line = str(i)
              line = str(i).zfill(4)
              f.write("%s," % (line))
              #f.write("%02d," % ((line))
              i+= pages
          f.write("\r\n")

      f.close()

      with open(filename, 'rb+') as filehandle:
       filehandle.seek(-1, os.SEEK_END)
       filehandle.truncate()
      f.close()

      return redirect(url_for('routes.success',filename=filename1))
      #return render_template('file_url.html', name = filename1, numPages = pages, printsPerPage = printsPerPage, startNumber = startNumber, endNumber = endNumber)
   else:
      # This is where to return the file
      return redirect(url_for('routes.success',filename = filename))
