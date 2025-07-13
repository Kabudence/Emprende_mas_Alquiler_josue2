from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required
from ..models import db, Publicacion, Cliente, TipoCliente, Negocio
from datetime import datetime
import os
from werkzeug.utils import secure_filename

publicaciones_bp = Blueprint('publicaciones', __name__, template_folder='templates')

UPLOAD_FOLDER = 'app/static/uploads/fotosclientes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_negocio():
    """Obtiene el negocio del usuario actual"""
    return Negocio.query.filter_by(usuario_id=current_user.id).first()


@publicaciones_bp.route('/')
@login_required
def listar_publicaciones():
    negocio = get_negocio()
    if not negocio:
        flash("Primero debe crear un negocio", "danger")
        return redirect(url_for('negocios.crear'))

    # Solo publicaciones de clientes del negocio actual
    publicaciones = Publicacion.query\
        .join(Cliente, Publicacion.cliente_id == Cliente.id)\
        .filter(Cliente.id_negocio == negocio.id)\
        .all()

    return render_template('listar_publicacion.html', 
                         publicaciones=publicaciones)

@publicaciones_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_publicacion():
    negocio = get_negocio()
    if not negocio:
        flash("Debe tener un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))

    # Solo clientes fijos del negocio actual
    clientes = Cliente.query\
        .join(TipoCliente, Cliente.tipo_cliente_id == TipoCliente.id)\
        .filter(
            TipoCliente.tipo == 'fijo',
            Cliente.id_negocio == negocio.id
        ).all()

    if request.method == 'POST':
        try:
            # Validar cliente pertenece al negocio
            cliente = Cliente.query.filter_by(
                id=request.form['cliente_id'],
                id_negocio=negocio.id
            ).first()

            if not cliente:
                flash("Cliente no válido", "danger")
                return redirect(url_for('publicaciones.crear_publicacion'))

            # Procesar imágenes
            foto_uno = guardar_imagen(request.files['foto_uno'])
            foto_dos = guardar_imagen(request.files.get('foto_dos')) if request.files.get('foto_dos') else None

            nueva_publicacion = Publicacion(
                fecha_compra=datetime.strptime(request.form['fecha_compra'], '%Y-%m-%d'),
                nombre_publicacion=request.form['nombre_publicacion'],
                cliente_id=cliente.id,
                productos=request.form.get('productos', ''),
                foto_uno=foto_uno,
                foto_dos=foto_dos,
                id_negocio=negocio.id  # Nuevo campo multi-tenant
            )

            db.session.add(nueva_publicacion)
            db.session.commit()
            flash('Publicación creada con éxito', 'success')
            return redirect(url_for('publicaciones.listar_publicaciones'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear publicación: {str(e)}', 'danger')

    return render_template('crear_publicacion.html', clientes=clientes)

def guardar_imagen(archivo):
    """Guarda una imagen de forma segura"""
    if archivo and archivo.filename:
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(filepath)
        return filename
    return None


@publicaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_publicacion(id):
    negocio = get_negocio()
    if not negocio:
        return jsonify({
            "success": False, 
            "message": "Operación no permitida"
        }), 403

    try:
        publicacion = Publicacion.query\
            .join(Cliente, Publicacion.cliente_id == Cliente.id)\
            .filter(
                Publicacion.id == id,
                Cliente.id_negocio == negocio.id
            ).first()

        if not publicacion:
            return jsonify({
                "success": False, 
                "message": "Publicación no encontrada"
            }), 404

        # Eliminar imágenes asociadas
        eliminar_imagen(publicacion.foto_uno)
        eliminar_imagen(publicacion.foto_dos)

        db.session.delete(publicacion)
        db.session.commit()
        return jsonify({
            "success": True, 
            "message": "Publicación eliminada con éxito"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False, 
            "message": f"Error al eliminar: {str(e)}"
        }), 500

def eliminar_imagen(nombre_archivo):
    """Elimina una imagen del sistema de archivos"""
    if nombre_archivo:
        try:
            path = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error eliminando archivo {nombre_archivo}: {str(e)}")


@publicaciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_publicacion(id):
    negocio = get_negocio()
    if not negocio:
        flash("Operación no permitida", "danger")
        return redirect(url_for('publicaciones.listar_publicaciones'))

    # Obtener publicación válida
    publicacion = Publicacion.query\
        .join(Cliente, Publicacion.cliente_id == Cliente.id)\
        .filter(
            Publicacion.id == id,
            Cliente.id_negocio == negocio.id
        ).first_or_404()

    # Solo clientes del negocio actual
    clientes = Cliente.query\
        .filter_by(id_negocio=negocio.id)\
        .all()

    if request.method == 'POST':
        try:
            # Validar cliente pertenece al negocio
            cliente = Cliente.query.filter_by(
                id=request.form['cliente_id'],
                id_negocio=negocio.id
            ).first()

            if not cliente:
                flash("Cliente no válido", "danger")
                return redirect(url_for('publicaciones.editar_publicacion', id=id))

            # Actualizar campos básicos
            publicacion.fecha_compra = datetime.strptime(request.form['fecha_compra'], '%Y-%m-%d')
            publicacion.nombre_publicacion = request.form['nombre_publicacion']
            publicacion.cliente_id = cliente.id
            publicacion.productos = request.form.get('productos', '')

            # Procesar imágenes
            publicacion.foto_uno = actualizar_imagen(
                request.files.get('foto_uno'),
                publicacion.foto_uno
            )
            publicacion.foto_dos = actualizar_imagen(
                request.files.get('foto_dos'),
                publicacion.foto_dos
            )

            db.session.commit()
            flash('Publicación actualizada con éxito', 'success')
            return redirect(url_for('publicaciones.listar_publicaciones'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')

    return render_template('editar_publicacion.html',
                         publicacion=publicacion,
                         clientes=clientes)

def actualizar_imagen(nuevo_archivo, nombre_actual):
    """Maneja la actualización segura de imágenes"""
    if nuevo_archivo and nuevo_archivo.filename:
        # Eliminar imagen anterior
        eliminar_imagen(nombre_actual)
        # Guardar nueva
        return guardar_imagen(nuevo_archivo)
    return nombre_actual


@publicaciones_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    # Verificar pertenencia del archivo
    negocio = get_negocio()
    if negocio and Publicacion.query\
        .filter(
            (Publicacion.foto_uno == filename) | 
            (Publicacion.foto_dos == filename)
        )\
        .join(Cliente)\
        .filter(Cliente.id_negocio == negocio.id)\
        .first():
        return send_from_directory(UPLOAD_FOLDER, filename)
    
    abort(404)