from flask import Blueprint

tamanios = Blueprint('tamanios', __name__, template_folder='templates')

from . import routes
