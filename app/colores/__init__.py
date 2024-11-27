from flask import Blueprint

colores = Blueprint('colores', __name__, template_folder='templates')

from . import routes
