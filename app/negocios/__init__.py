from flask import Blueprint

negocios = Blueprint('negocios', __name__, template_folder='templates')

from . import routes
