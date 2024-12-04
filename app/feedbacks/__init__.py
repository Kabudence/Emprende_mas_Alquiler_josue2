from flask import Blueprint

feedbacks = Blueprint('feedbacks', __name__, template_folder='templates')

from . import routes
