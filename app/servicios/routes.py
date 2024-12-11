from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from ..models import Servicio, Negocio, Categoria
from ..database import db
from . import servicios

# Configura la carpeta de carga 
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@servicios.route('/')
@login_required
def index():
    # Obtener el primer negocio de la base de datos
    negocio = Negocio.query.first()

    if not negocio:
        flash('No se encontró un negocio.', 'danger')
        return redirect(url_for('servicios.index'))
    
    # Obtener las categorías del negocio, filtradas por rubro y tipo_id (servicios)
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id, tipo_id=2).all()
    
    # Obtener los servicios asociados a las categorías obtenidas
    servicios_lista = Servicio.query.filter(Servicio.categoria_id.in_([categoria.id for categoria in categorias])).all()

    return render_template('servicios/index.html', servicios=servicios_lista)



# Crear servicio
@servicios.route('/crear', methods=['GET'])
@login_required
def crear():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    # Obtener las categorías del rubro con tipo_id = 2 (servicios)
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id, tipo_id=2).all()

    return render_template('servicios/crear_servicio.html', categorias=categorias)

@servicios.route('/crear', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    categoria_id = request.form.get('categoria_id')
    archivo_imagen = request.files.get('imagen')

    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    if archivo_imagen and allowed_file(archivo_imagen.filename):
        # Generar un nombre único para la imagen
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(archivo_imagen.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        archivo_imagen.save(filepath)
        imagen_nombre = unique_filename
    else:
        imagen_nombre = None

    nuevo_servicio = Servicio(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        precio_oferta=precio_oferta,
        telefono=telefono,
        correo=correo,
        categoria_id=categoria_id,
        imagen=imagen_nombre
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

    # Obtener las categorías del rubro con tipo_id = 2 (servicios)
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id, tipo_id=2).all()

    return render_template('servicios/editar_servicio.html', servicio=servicio, categorias=categorias)

@servicios.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    servicio = Servicio.query.get_or_404(id)
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    categoria_id = request.form.get('categoria_id')
    archivo_imagen = request.files.get('imagen')

    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    servicio.nombre = nombre
    servicio.descripcion = descripcion
    servicio.precio = precio
    servicio.precio_oferta = precio_oferta
    servicio.telefono = telefono
    servicio.correo = correo
    servicio.categoria_id = categoria_id

    if archivo_imagen and allowed_file(archivo_imagen.filename):
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(archivo_imagen.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        archivo_imagen.save(filepath)
        servicio.imagen = unique_filename 

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
