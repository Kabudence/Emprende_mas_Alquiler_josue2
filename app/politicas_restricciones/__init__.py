from flask import Blueprint

politicas_restricciones = Blueprint('politicas_restricciones', __name__, template_folder='templates')

from . import routes
