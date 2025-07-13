from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Categoria, Negocio, Rubro, TipoCategoria
from ..database import db
from . import categorias

@categorias.route('/')
@login_required
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    
    if negocio:
        rubro_id = negocio.rubro_id
        
        query = request.args.get('buscar', '')
        
        categorias_lista = Categoria.query.filter(
            Categoria.rubro_id == rubro_id,
            Categoria.nombre.ilike(f'%{query}%')
        ).all()
    else:
        categorias_lista = []

    return render_template('categorias/index.html', categorias=categorias_lista, query=query)

@categorias.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo_categoria_id = request.form.get('tipo_categoria_id')

        if negocio and nombre and tipo_categoria_id:
            # IMPORTANTE: Ahora también asigna el id_negocio
            nueva_categoria = Categoria(
                nombre=nombre,
                rubro_id=negocio.rubro_id,
                tipo_id=tipo_categoria_id,
                id_negocio=negocio.id
            )
            db.session.add(nueva_categoria)
            db.session.commit()
            flash('Categoría creada con éxito.', 'success')
            return redirect(url_for('categorias.index'))
        else:
            flash('Error al crear la categoría. Verifique los datos ingresados.', 'danger')

    rubros = Rubro.query.all()
    tipos_categoria = TipoCategoria.query.all()
    return render_template('categorias/crear_categoria.html', rubros=rubros, tipos_categoria=tipos_categoria, negocio=negocio)



@categorias.route('/actualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def actualizar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.rubro_id = request.form['rubro_id']
        db.session.commit()
        flash('Categoría actualizada con éxito', 'success')
        return redirect(url_for('categorias.index'))
    rubros = Rubro.query.all()  # Asegúrate de que esto traiga los rubros necesarios
    return render_template('categorias/actualizar_categoria.html', categoria=categoria, rubros=rubros)

@categorias.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    # Obtener la categoría por ID
    categoria = Categoria.query.get_or_404(id)

    # Verificar que el negocio del usuario tenga acceso a esta categoría (seguridad)
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if negocio and categoria.rubro_id == negocio.rubro_id:
        # Eliminar la categoría
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada con éxito.', 'success')
    else:
        flash('No tienes permisos para eliminar esta categoría o la categoría no existe.', 'danger')

    return redirect(url_for('categorias.index'))