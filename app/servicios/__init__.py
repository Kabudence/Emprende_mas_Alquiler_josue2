from flask import Blueprint

servicios = Blueprint('servicios', __name__, template_folder='templates')

from . import routes
