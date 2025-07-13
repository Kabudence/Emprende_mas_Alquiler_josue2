from flask import Blueprint

# Crear el Blueprint
Info_Empresa = Blueprint('informacion_empresa', __name__, template_folder='templates')

# Importar las rutas
from . import routes
