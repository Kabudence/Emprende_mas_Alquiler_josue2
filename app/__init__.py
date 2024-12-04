from flask import Flask
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
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ozxcXkasdnM'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/emprende_mas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

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

    return app
