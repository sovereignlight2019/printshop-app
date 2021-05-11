from flask import Flask

app = Flask(__name__)

from routes import *
app.register_blueprint(routes)
