from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Color
from ..database import db
from . import colores

# Mostrar todos los colores
@colores.route('/')
@login_required
def index():
    busqueda = request.args.get('busqueda', '')
    if busqueda:
        colores_lista = Color.query.filter(Color.nombre.like(f'%{busqueda}%')).all()
    else:
        colores_lista = Color.query.all()
    
    return render_template('colores/index.html', colores=colores_lista, busqueda=busqueda)


# Crear colores
@colores.route('/crear', methods=['GET'])
@login_required
def crear():
    return render_template('colores/crear_color.html')

@colores.route('/crear', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    hexadecimal = request.form['hexadecimal']
    
    nuevo_color = Color(nombre=nombre, hexadecimal=hexadecimal)
    db.session.add(nuevo_color)
    db.session.commit()

    flash('Color creado con éxito', 'success')
    return redirect(url_for('colores.index'))

# Editar colores
@colores.route('/editar/<int:id>', methods=['GET'])
@login_required
def editar(id):
    color = Color.query.get_or_404(id)
    return render_template('colores/editar_color.html', color=color)

@colores.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    color = Color.query.get_or_404(id)
    color.nombre = request.form['nombre']
    color.hexadecimal = request.form['hexadecimal']
    
    db.session.commit()

    flash('Color actualizado con éxito', 'success')
    return redirect(url_for('colores.index'))

# Eliminar color
@colores.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    color = Color.query.get_or_404(id)
    db.session.delete(color)
    db.session.commit()
    
    flash('Color eliminado con éxito', 'success')
    return redirect(url_for('colores.index'))
