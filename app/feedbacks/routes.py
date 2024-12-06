from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import Feedback, Negocio, Categoria, CategoriaFeedback
from ..database import db
from . import feedbacks

@feedbacks.route('/')
@login_required
def index():
    # Obtener el negocio asociado al usuario logueado
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    # Si el negocio existe, obtener las categorías asociadas al rubro del negocio
    if negocio:
        categorias_negocio = Categoria.query.filter_by(rubro_id=negocio.rubro_id).all()
        # Obtener las categorías de feedback asociadas a esas categorías del negocio
        categoria_ids = [categoria.id for categoria in categorias_negocio]
        feedbacks_lista = Feedback.query.join(CategoriaFeedback).filter(CategoriaFeedback.id.in_(categoria_ids)).all()
    else:
        feedbacks_lista = []

    # Si se hace una búsqueda, filtrar los feedbacks por asunto
    query = request.args.get('buscar', '')
    if query:
        feedbacks_lista = [feedback for feedback in feedbacks_lista if query.lower() in feedback.asunto.lower()]

    return render_template('feedbacks/index.html', feedbacks=feedbacks_lista, query=query)