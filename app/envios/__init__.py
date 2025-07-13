# app/envios/__init__.py
from flask import Blueprint

envios_bp = Blueprint('envios', __name__, template_folder='templates')

# Importamos las rutas para que se registren en el Blueprint
from . import routes