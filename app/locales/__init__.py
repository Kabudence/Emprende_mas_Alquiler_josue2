from flask import Blueprint

locales_bp = Blueprint('locales', __name__, template_folder='templates')

from . import routes
