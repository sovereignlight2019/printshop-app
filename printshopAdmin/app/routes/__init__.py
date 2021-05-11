from flask import Blueprint, Flask
routes = Blueprint('routes', __name__)

from .allroutes import *
from .editpaper import *
from .foiling import *
from .foiling_add import *
from .numbering import *
