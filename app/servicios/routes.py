from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Servicio, Negocio
from ..database import db
from . import servicios

# Mostrar todos los servicios
@servicios.route('/')
@login_required
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))
    
    busqueda = request.args.get('busqueda', '')
    if busqueda:
        servicios_lista = Servicio.query.filter(Servicio.nombre_servicio.like(f'%{busqueda}%'), Servicio.rubro_id == negocio.rubro_id).all()
    else:
        servicios_lista = Servicio.query.filter(Servicio.rubro_id == negocio.rubro_id).all()

    return render_template('servicios/index.html', servicios=servicios_lista, busqueda=busqueda)


# Crear servicio
@servicios.route('/crear', methods=['GET'])
@login_required
def crear():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    rubro = negocio.rubro

    return render_template('servicios/crear_servicio.html', rubro=rubro)


@servicios.route('/crear', methods=['POST'])
@login_required
def guardar():
    nombre_servicio = request.form['nombre_servicio']
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')

    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    rubro_id = negocio.rubro_id

    nuevo_servicio = Servicio(
        nombre_servicio=nombre_servicio,
        descripcion=descripcion,
        precio=precio,
        precio_oferta=precio_oferta,
        rubro_id=rubro_id
    )
    db.session.add(nuevo_servicio)
    db.session.commit()

    flash('Servicio creado con éxito', 'success')
    return redirect(url_for('servicios.index'))


# Editar servicio
@servicios.route('/editar/<int:id>', methods=['GET'])
@login_required
def editar(id):
    servicio = Servicio.query.get_or_404(id)
    
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    rubro = negocio.rubro 

    return render_template('servicios/editar_servicio.html', servicio=servicio, rubro=rubro)


@servicios.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    servicio = Servicio.query.get_or_404(id)
    nombre_servicio = request.form.get('nombre_servicio')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    rubro_id = negocio.rubro_id

    servicio.nombre_servicio = nombre_servicio
    servicio.descripcion = descripcion
    servicio.precio = precio
    servicio.precio_oferta = precio_oferta
    servicio.rubro_id = rubro_id

    db.session.commit()

    flash('Servicio actualizado con éxito', 'success')
    return redirect(url_for('servicios.index'))



# Eliminar servicio
@servicios.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    
    flash('Servicio eliminado con éxito', 'success')
    return redirect(url_for('servicios.index'))
