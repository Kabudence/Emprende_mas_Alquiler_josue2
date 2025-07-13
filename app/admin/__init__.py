from flask import Blueprint

# Define la blueprint principal de admin
admin_bp = Blueprint('admin', __name__, template_folder='templates')



# Importa las rutas de categorías después de definir la blueprint
from app.admin.categorias_routes import *