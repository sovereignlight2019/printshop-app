from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
	return "Hello World!"

if __name__ == "__main__":
	app.run(debug=True)
