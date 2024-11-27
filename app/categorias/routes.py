from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Categoria, Negocio
from ..database import db
from . import categorias

@categorias.route('/')
@login_required
def index():
    # Obtener el negocio asociado al usuario logueado
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if negocio:
        # Filtrar las categorías asociadas al rubro del negocio
        categorias_lista = Categoria.query.filter_by(rubro_id=negocio.rubro_id).all()
    else:
        categorias_lista = []

    return render_template('categorias/index.html', categorias=categorias_lista)