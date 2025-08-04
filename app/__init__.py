import os
import pymysql
from flask_cors import CORS

from appointment.interfaces.appointment_controller import appointment_api
from schedules.interfaces.schedule_controller import schedule_api
from staff.interfaces.staff_controller import staff_api
from .admin.external_routes import external_api_bp

pymysql.install_as_MySQLdb()


from flask import Flask, request, redirect, url_for,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .database import db
from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .productos import productos as productos_blueprint
from .categorias import categorias as categorias_blueprint
from .negocios import negocios as negocios_blueprint
from .colores import colores as colores_blueprint
from .tamanios import tamanios as tamanios_blueprint
from .feedbacks import feedbacks as feedbacks_blueprint
from .servicios import servicios as servicios_blueprint
from .politicas_restricciones import politicas_restricciones as politicas_restricciones_blueprint
from .slider import slider as slider_blueprint
from .InformacionEmpresa import Info_Empresa as Info_Empresa_blueprint
from app.registro_usuarios.routes import registro_usuarios_blueprint
from app.sucursales.routes import sucursales_blueprint
from app.promociones.routes import promociones_bp
from app.publicaciones.routes import publicaciones_bp
from app.envios.routes import envios_bp
from app.libro_reclamaciones.routes import reclamos_bp
from app.pedidos.routes import pedidos_bp
from .locales.routes import locales_bp
from .admin.routes import admin_bp 
from flask_wtf.csrf import CSRFProtect



from config import Config


login_manager = LoginManager()

def check_negocio():
    excluded_paths = ['/negocios/', '/negocios/guardar']
    if request.blueprint != 'auth' and request.path not in excluded_paths:
        from app.models import Negocio
        if not Negocio.query.first():
            return redirect(url_for('negocios.index'))

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app, origins=["http://localhost:64643"])

    # Cargar configuración desde config.py
    app.config.from_object(Config)

    # ───── INICIALIZAR BASE DE DATOS PEEWEE ─────
    from shared.infrastructure.database import init_db
    init_db()

    # ───── INYECTAR SERVICIOS DE DOMINIO ─────
    from shared.factory.container_factory import build_services
    for key, value in build_services().items():
        app.config[key] = value

    csrf = CSRFProtect(app)

    servicios_folder = os.path.join(app.root_path, 'static', 'uploads', 'servicios')
    os.makedirs(servicios_folder, exist_ok=True)
    app.config['SERVICIOS_UPLOAD_FOLDER'] = servicios_folder
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads', 'servicios')
    app.config['SERVICIOS_UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads', 'servicios')

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(productos_blueprint, url_prefix='/productos')
    app.register_blueprint(servicios_blueprint, url_prefix='/servicios')
    app.register_blueprint(categorias_blueprint, url_prefix='/categorias')
    app.register_blueprint(negocios_blueprint, url_prefix='/negocios')
    app.register_blueprint(colores_blueprint, url_prefix='/colores')
    app.register_blueprint(tamanios_blueprint, url_prefix='/tamanios')
    app.register_blueprint(feedbacks_blueprint, url_prefix='/feedbacks')
    app.register_blueprint(politicas_restricciones_blueprint, url_prefix='/politicas_restricciones')
    app.register_blueprint(slider_blueprint, url_prefix='/slider')
    app.register_blueprint(Info_Empresa_blueprint, url_prefix='/informacion_empresa')
    app.register_blueprint(registro_usuarios_blueprint, url_prefix='/registro_usuarios')
    app.register_blueprint(sucursales_blueprint, url_prefix='/sucursales')
    app.register_blueprint(promociones_bp, url_prefix='/promociones')
    app.register_blueprint(publicaciones_bp, url_prefix='/publicaciones')
    app.register_blueprint(envios_bp, url_prefix='/envios')
    app.register_blueprint(reclamos_bp, url_prefix='/libro_reclamaciones')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(locales_bp, url_prefix='/locales')
    app.register_blueprint(external_api_bp)
    csrf.exempt(external_api_bp)  # <--- agrega esta línea aquí

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(staff_api)
    csrf.exempt(staff_api)  # <--- agrega esta línea aquí
    app.register_blueprint(schedule_api)
    app.register_blueprint(appointment_api)
    csrf.exempt(appointment_api)  # <--- agrega esta línea aquí


    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory('app/static', filename)
    
    @app.before_request
    def before_request():
        if request.blueprint != 'auth':
            return check_negocio()

    return app

