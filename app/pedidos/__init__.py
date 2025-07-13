from flask import Blueprint
from flask_mysqldb import MySQL
from config import Config



pedidos_bp = Blueprint('pedidos', __name__, template_folder='templates')
