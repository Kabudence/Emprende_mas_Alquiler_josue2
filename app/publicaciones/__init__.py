from flask import Blueprint

publicaciones_bp = Blueprint('publicaciones', __name__, template_folder='/publicaciones')



from . import routes