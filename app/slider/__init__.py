from flask import Blueprint

slider = Blueprint('slider', __name__, template_folder='templates')

from . import routes