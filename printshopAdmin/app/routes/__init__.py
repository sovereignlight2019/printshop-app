from flask import Blueprint, Flask
routes = Blueprint('routes', __name__)

from .allroutes import *
from .editpaper import *
