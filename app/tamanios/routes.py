from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Tamanio, Categoria  # Asegúrate de tener el modelo Categoria
from ..database import db
from . import tamanios

# Mostrar todos los tamaños
@tamanios.route('/')
@login_required
def index():
    busqueda = request.args.get('busqueda', '')
    if busqueda:
        tamanios_lista = Tamanio.query.filter(Tamanio.nombre.like(f'%{busqueda}%')).all()
    else:
        tamanios_lista = Tamanio.query.all()
    
    return render_template('tamanios/index.html', tamanios=tamanios_lista, busqueda=busqueda)

# Crear tamaños
@tamanios.route('/crear', methods=['GET'])
@login_required
def crear():
    categorias = Categoria.query.all()
    return render_template('tamanios/crear_tamanio.html', categorias=categorias)

@tamanios.route('/crear', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    categoria_id = request.form.get('categoria')

    if not categoria_id:
        flash('Debe seleccionar una categoría.', 'danger')
        return redirect(url_for('tamanios.crear'))

    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        flash('La categoría seleccionada no existe.', 'danger')
        return redirect(url_for('tamanios.crear'))

    nuevo_tamanio = Tamanio(nombre=nombre, categoria_id=categoria_id)
    db.session.add(nuevo_tamanio)
    db.session.commit()

    flash('Tamaño creado con éxito', 'success')
    return redirect(url_for('tamanios.index'))

# Editar tamaños
@tamanios.route('/editar/<int:id>', methods=['GET'])
@login_required
def editar(id):
    tamanio = Tamanio.query.get_or_404(id)
    categorias = Categoria.query.all()
    return render_template('tamanios/editar_tamanio.html', tamanio=tamanio, categorias=categorias)

@tamanios.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    tamanio = Tamanio.query.get_or_404(id)
    nombre = request.form.get('nombre')
    categoria_id = request.form.get('categoria_id')

    if not categoria_id or not Categoria.query.get(categoria_id):
        flash('Debe seleccionar una categoría válida.', 'danger')
        return redirect(url_for('tamanios.editar', id=id))
    
    tamanio.nombre = nombre
    tamanio.categoria_id = categoria_id

    db.session.commit()

    flash('Tamaño actualizado con éxito', 'success')
    return redirect(url_for('tamanios.index'))

# Eliminar tamaño
@tamanios.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    tamanio = Tamanio.query.get_or_404(id)
    db.session.delete(tamanio)
    db.session.commit()
    
    flash('Tamaño eliminado con éxito', 'success')
    return redirect(url_for('tamanios.index'))
