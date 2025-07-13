from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_required, current_user
from ..models import Color, Negocio
from ..database import db
from . import colores

def get_current_business():
    """Obtiene el negocio actual del usuario de forma segura"""
    if not current_user.is_authenticated:
        return None
        
    # Opción 1: Relación directa (usuario tiene un solo negocio)
    if hasattr(current_user, 'negocio') and current_user.negocio:
        return current_user.negocio
        
    # Opción 2: Relación muchos-a-muchos (usuario tiene varios negocios)
    if hasattr(current_user, 'negocios'):
        if current_user.negocios:  # Verifica que la lista no esté vacía
            return current_user.negocios[0]  # Tomamos el primer negocio
            
    return None

@colores.route('/')
@login_required
def index():
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('main.index'))
    
    busqueda = request.args.get('busqueda', '')
    query = Color.query.filter_by(id_negocio=negocio.id)
    
    if busqueda:
        query = query.filter(Color.nombre.ilike(f'%{busqueda}%'))
    
    colores_lista = query.order_by(Color.nombre.asc()).all()
    return render_template('colores/index.html', 
                         colores=colores_lista, 
                         busqueda=busqueda,
                         negocio=negocio)

# Crear nuevo color para el negocio
@colores.route('/crear', methods=['GET'])
@login_required
def crear():
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    return render_template('colores/crear_color.html')

# @colores.route('/crear', methods=['POST'])
# @login_required
# def guardar():
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    
    nombre = request.form.get('nombre', '').strip()
    hexadecimal = request.form.get('hexadecimal', '').strip()
    
    if not nombre or not hexadecimal:
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('colores.crear'))
    
    # Verificar si el color ya existe para este negocio
    if Color.query.filter_by(nombre=nombre, id_negocio=negocio.id).first():
        flash('Ya existe un color con ese nombre', 'danger')
        return redirect(url_for('colores.crear'))
    
    try:
        nuevo_color = Color(
            nombre=nombre,
            hexadecimal=hexadecimal,
            id_negocio=negocio.id
        )
        db.session.add(nuevo_color)
        db.session.commit()
        flash('Color creado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear el color: {str(e)}', 'danger')
    
    return redirect(url_for('colores.index'))


@colores.route('/crear', methods=['POST'])
@login_required
def guardar():
    negocio = get_current_business()
    print("NEGOCIO EN CREAR:", negocio)  # <-- imprime negocio actual
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    
    nombre = request.form.get('nombre', '').strip()
    hexadecimal = request.form.get('hexadecimal', '').strip()
    print("DATOS FORM:", nombre, hexadecimal)  # <-- imprime los datos del formulario
    
    # Verificar si el color ya existe para este negocio
    existe = Color.query.filter_by(nombre=nombre, id_negocio=negocio.id).first()
    print("COLOR YA EXISTE?", existe)
    
    try:
        nuevo_color = Color(
            nombre=nombre,
            hexadecimal=hexadecimal,
            id_negocio=negocio.id
        )
        db.session.add(nuevo_color)
        db.session.commit()
        print("COLOR CREADO:", nuevo_color.id)
        flash('Color creado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        print("ERROR AL CREAR COLOR:", e)
        flash(f'Error al crear el color: {str(e)}', 'danger')
    
    return redirect(url_for('colores.index'))




# Editar color (con verificación de pertenencia)
@colores.route('/editar/<int:id>', methods=['GET'])
@login_required
def editar(id):
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    
    color = Color.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    return render_template('colores/editar_color.html', color=color)

@colores.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    
    color = Color.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    nombre = request.form.get('nombre', '').strip()
    hexadecimal = request.form.get('hexadecimal', '').strip()
    
    if not nombre or not hexadecimal:
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('colores.editar', id=id))
    
    # Verificar si el nombre ya existe en otro color del mismo negocio
    if Color.query.filter(
        Color.nombre == nombre,
        Color.id_negocio == negocio.id,
        Color.id != id
    ).first():
        flash('Ya existe otro color con ese nombre', 'danger')
        return redirect(url_for('colores.editar', id=id))
    
    try:
        color.nombre = nombre
        color.hexadecimal = hexadecimal
        db.session.commit()
        flash('Color actualizado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return redirect(url_for('colores.index'))

# Eliminar color (con verificación)
@colores.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('colores.index'))
    
    color = Color.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    
    try:
        db.session.delete(color)
        db.session.commit()
        flash('Color eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('colores.index'))