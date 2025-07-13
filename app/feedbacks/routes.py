from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import Feedback, Negocio, CategoriaFeedback, Usuario, Cliente
from ..database import db
from . import feedbacks

@feedbacks.route('/')
@login_required
def index():
    print("=== [GET] /feedbacks/ ===")
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    print(f"[DEBUG] Usuario logueado: ID={current_user.id}, username={current_user.username}")
    print(f"[DEBUG] Negocio encontrado: ID={negocio.id if negocio else None}, nombre={negocio.nombre if negocio else None}")

    categoria_feedback_lista = CategoriaFeedback.query.all()
    print(f"[DEBUG] Total de categorías de feedback: {len(categoria_feedback_lista)}")

    # Query base: feedbacks del negocio actual
    feedbacks_query = Feedback.query.filter(Feedback.id_negocio == negocio.id)

    # Filtros adicionales...
    categoria_feedback_id = request.args.get('categoria_feedback_id', type=int)
    if categoria_feedback_id:
        feedbacks_query = feedbacks_query.filter(Feedback.categoria_id == categoria_feedback_id)
    query = request.args.get('buscar', '')
    if query:
        feedbacks_query = feedbacks_query.filter(Feedback.asunto.ilike(f'%{query}%'))

    # JOIN con Cliente usando usuario_id == clientes.id (o feedback.usuario_id == cliente.id)
    feedbacks_lista = []
    for feedback in feedbacks_query.order_by(Feedback.id.asc()).all():
        cliente = Cliente.query.filter_by(id=feedback.usuario_id).first()
        nombre_cliente = cliente.nombre_completo if cliente else None
        feedbacks_lista.append((feedback, nombre_cliente))
    print(f"[DEBUG] Feedbacks devueltos por la consulta: {len(feedbacks_lista)}")
    print(f"[DEBUG] IDs de feedback devueltos: {[f[0].id for f in feedbacks_lista]}")
    print(f"[DEBUG] Nombres de cliente devueltos: {[f[1] for f in feedbacks_lista]}")

    return render_template(
        'feedbacks/index.html',
        feedbacks=feedbacks_lista,
        query=query,
        categoria_feedback_lista=categoria_feedback_lista,
        categoria_feedback_id=categoria_feedback_id,
        negocio=negocio
    )