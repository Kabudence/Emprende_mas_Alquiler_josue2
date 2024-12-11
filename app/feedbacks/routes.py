from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import Feedback, Negocio, Categoria, CategoriaFeedback
from ..database import db
from . import feedbacks

@feedbacks.route('/')
@login_required
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    categoria_feedback_lista = CategoriaFeedback.query.all()

    if negocio:
        categorias_negocio = Categoria.query.filter_by(rubro_id=negocio.rubro_id).all()
        categoria_ids = [categoria.id for categoria in categorias_negocio]
        feedbacks_lista = Feedback.query.join(CategoriaFeedback).filter(CategoriaFeedback.id.in_(categoria_ids)).all()
    else:
        feedbacks_lista = []

    categoria_feedback_id = request.args.get('categoria_feedback_id')
    if categoria_feedback_id:
        feedbacks_lista = [feedback for feedback in feedbacks_lista if feedback.categoria_feedback_id == int(categoria_feedback_id)]

    query = request.args.get('buscar', '')
    if query:
        feedbacks_lista = [feedback for feedback in feedbacks_lista if query.lower() in feedback.asunto.lower()]

    return render_template('feedbacks/index.html', feedbacks=feedbacks_lista, query=query, categoria_feedback_lista=categoria_feedback_lista, categoria_feedback_id=categoria_feedback_id)
