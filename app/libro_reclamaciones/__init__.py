from flask import Blueprint

reclamos_bp = Blueprint('libro_reclamaciones', __name__, template_folder='templates')
from . import routes


