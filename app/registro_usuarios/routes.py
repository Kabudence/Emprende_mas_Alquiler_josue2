from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import bcrypt
from datetime import datetime  # <- Añadido para nombres únicos
from ..models import Cliente, Negocio
from ..database import db

# Configuración del blueprint
registro_usuarios_blueprint = Blueprint(
    'registro_usuarios', __name__,
    template_folder='templates',
    static_folder='static'
)

# Carpeta base para la subida de archivos
BASE_UPLOAD_FOLDER = 'app/static/uploads/registro_clientes'
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@registro_usuarios_blueprint.route('/')
@login_required
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'danger')
        return redirect(url_for('negocios.crear'))

    # Aquí agregamos el orden ascendente (menos antiguo al más antiguo)
    clientes = Cliente.query.filter_by(id_negocio=negocio.id).order_by(Cliente.fecha.desc()).all()

    clientes_serializados = [
        {column.name: getattr(cliente, column.name) for column in cliente.__table__.columns}
        for cliente in clientes
    ]

    return render_template('registro.html', usuarios=clientes_serializados)


# Ruta para registrar usuarios (Modificada)
@registro_usuarios_blueprint.route('/registrar', methods=['POST'])
@login_required
def registrar():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'danger')
        return redirect(url_for('negocios.crear'))

    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            required_fields = ['nombre_completo', 'whatsapp', 'correo', 'fecha']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'El campo {field} es requerido', 'danger')
                    return redirect(url_for('registro_usuarios.index'))

            # Manejo de archivo
            if 'foto' not in request.files:
                flash('Debe subir una foto de perfil', 'danger')
                return redirect(url_for('registro_usuarios.index'))

            foto = request.files['foto']
            if foto.filename == '' or not allowed_file(foto.filename):
                flash('Imagen no válida o formato no permitido', 'danger')
                return redirect(url_for('registro_usuarios.index'))

            # --- Cambios clave: Guardar en registro_clientes sin subcarpetas ---
            # Generar nombre único para evitar colisiones
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            foto_filename = f"{timestamp}_{secure_filename(foto.filename)}"
            foto.save(os.path.join(BASE_UPLOAD_FOLDER, foto_filename))

            # Hash de contraseña
            contrasena = request.form['contrasena']
            contrasena_encriptada = bcrypt.hashpw(
                contrasena.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')

            # Crear usuario
            nuevo_usuario = Cliente(
                nombre_completo=request.form['nombre_completo'],
                whatsapp=request.form['whatsapp'],
                correo=request.form['correo'],
                departamento=request.form['departamento'],
                provincia=request.form['provincia'],
                distrito=request.form['distrito'],
                direccion=request.form['direccion'],
                referencia=request.form['referencia'],
                nombre_usuario=request.form['nombre_usuario'],
                contrasena=contrasena_encriptada,
                foto=foto_filename,
                fecha=request.form['fecha'],
                tipo_cliente_id=request.form['tipo_cliente_id'],
                estado=request.form.get('estado', 'Activo'),
                id_negocio=negocio.id
            )

            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito', 'success')

        except IntegrityError:
            db.session.rollback()
            flash('El correo o nombre de usuario ya está registrado', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error inesperado: {str(e)}', 'danger')

        return redirect(url_for('registro_usuarios.consultar'))

# Ruta para consultar usuarios (sin cambios)
@registro_usuarios_blueprint.route('/consultar')
@login_required
def consultar():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'danger')
        return redirect(url_for('negocios.crear'))

    clientes = Cliente.query.filter_by(id_negocio=negocio.id).all()
    
    clientes_serializados = [
        {column.name: getattr(cliente, column.name) for column in cliente.__table__.columns}
        for cliente in clientes
    ]
    return render_template('consultar.html', usuarios=clientes_serializados)



@registro_usuarios_blueprint.route('/api/registro', methods=['POST'])
def api_register():
    try:
        data = request.form  # O request.json si envías JSON puro

        required_fields = ['nombre_completo', 'whatsapp', 'correo', 'fecha', 'contrasena', 'tipo_cliente_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"El campo {field} es requerido"}), 400

        # Negocio debe venir por algún medio (id_negocio) o user logueado (ajustar según lógica)
        id_negocio = data.get('id_negocio')
        if not id_negocio:
            return jsonify({"error": "id_negocio es requerido"}), 400

        # Manejo de archivo (multipart/form-data)
        foto = request.files.get('foto')
        if not foto or foto.filename == '' or not allowed_file(foto.filename):
            return jsonify({"error": "Imagen no válida o formato no permitido"}), 400

        # Guardar imagen con nombre único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        foto_filename = f"{timestamp}_{secure_filename(foto.filename)}"
        foto.save(os.path.join(BASE_UPLOAD_FOLDER, foto_filename))

        # Hashear contraseña
        contrasena_encriptada = bcrypt.hashpw(
            data['contrasena'].encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        nuevo_usuario = Cliente(
            nombre_completo=data['nombre_completo'],
            whatsapp=data['whatsapp'],
            correo=data['correo'],
            departamento=data.get('departamento', ''),
            provincia=data.get('provincia', ''),
            distrito=data.get('distrito', ''),
            direccion=data.get('direccion', ''),
            referencia=data.get('referencia', ''),
            nombre_usuario=data.get('nombre_usuario', ''),
            contrasena=contrasena_encriptada,
            foto=foto_filename,
            fecha=data['fecha'],
            tipo_cliente_id=data['tipo_cliente_id'],
            estado=data.get('estado', 'Activo'),
            id_negocio=id_negocio
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        # Devuelve el id y status 200
        return jsonify({"id": nuevo_usuario.id, "message": "Usuario registrado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@registro_usuarios_blueprint.route('/api/usuario/<int:user_id>', methods=['GET'])
def find_by_id(user_id):
    user = Cliente.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
    return jsonify(user_dict), 200
