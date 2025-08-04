# app/admin/external_routes.py

from flask import Blueprint, request, jsonify
from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash  # Para comparar contraseñas hasheadas

external_api_bp = Blueprint('external_api', __name__, url_prefix='/external_api/usuarios')

@external_api_bp.route('/crear', methods=['POST'])
def api_crear_usuario():
    from app import db                   # Importa aquí (¡no arriba!)
    from app.models import Usuario
    data = request.json
    campos_requeridos = ['nombre', 'dni', 'email', 'celular', 'username', 'password', 'id_tipo_usuario']
    if not all(k in data for k in campos_requeridos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    role = 'COMPRADOR'
    # Validación de unicidad (opcional)
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El username ya existe'}), 409
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 409

    try:
        nuevo_usuario = Usuario(
            nombre = data['nombre'],
            dni = data['dni'],
            email = data['email'],
            celular = data['celular'],
            username = data['username'],
            password = data['password'],
            id_tipo_usuario = data['id_tipo_usuario'],
            foto_dni_frontal = data.get('foto_dni_frontal'),
            foto_dni_posterior = data.get('foto_dni_posterior'),
            user_inviter = data.get('user_inviter'),
            role = role
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario creado', 'id': nuevo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@external_api_bp.route('/<int:user_id>', methods=['GET'])
def api_usuario_por_id(user_id):
    from app.models import Usuario       # Importa aquí
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'dni': usuario.dni,
        'email': usuario.email,
        'celular': usuario.celular,
        'username': usuario.username,
        'id_tipo_usuario': usuario.id_tipo_usuario,
        'foto_dni_frontal': usuario.foto_dni_frontal,
        'foto_dni_posterior': usuario.foto_dni_posterior,
        'user_inviter': usuario.user_inviter,
        'role': usuario.role,
        'created_at': usuario.created_at.strftime('%Y-%m-%d %H:%M:%S') if usuario.created_at else None
    }
    return jsonify(data)



@external_api_bp.route('/api/login', methods=['POST'])
def api_login():
    import logging
    log = logging.getLogger("auth")

    from ..models import Negocio, Usuario
    from werkzeug.security import check_password_hash
    from flask_login import login_user, current_user
    from flask import session, jsonify, request

    log.info("Intento de login recibido")

    if current_user.is_authenticated:
        log.info("Usuario ya autenticado: %s", current_user)
        return jsonify({'message': 'Ya estás autenticado.'}), 200

    # Soporta JSON y formulario
    data = request.get_json() or request.form
    log.info("Datos recibidos: %s", data)

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    log.info("Username recibido: '%s'", username)

    if not username or not password:
        log.warning("Faltan credenciales: username='%s' password='%s'", username, '***' if password else '')
        return jsonify({'message': 'Faltan credenciales.'}), 400

    user = Usuario.query.filter_by(username=username).first()
    if user:
        log.info("Usuario encontrado en DB: %s", user)
    else:
        log.warning("Usuario no encontrado: %s", username)

    if user and check_password_hash(user.password, password):
        log.info("Contraseña correcta para usuario: %s", username)
        # Verifica negocios bloqueados si es dueño
        if hasattr(user, 'tipo_usuario') and getattr(user.tipo_usuario, 'nombre_tipo', None) == 'dueno_tienda':
            negocios_bloqueados = Negocio.query.filter(
                Negocio.usuario_id == user.id,
                Negocio.bloqueado == True
            ).all()
            log.info("Negocios bloqueados encontrados: %s", negocios_bloqueados)
            if negocios_bloqueados:
                log.warning("Acceso denegado: negocios bloqueados para usuario %s", username)
                return jsonify({'message': 'Acceso denegado: tienes negocios bloqueados.'}), 403

        login_user(user)
        session['user_id'] = user.id
        session['role_id'] = user.id_tipo_usuario

        negocio = Negocio.query.filter_by(usuario_id=user.id).first()
        id_negocio = negocio.id if negocio else None
        session['id_negocio'] = id_negocio

        log.info("Login exitoso para usuario: %s", username)

        return jsonify({
            'message': 'Login exitoso.',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': getattr(user.tipo_usuario, 'nombre_tipo', None),
                'id_negocio': id_negocio,
            }
        }), 200
    else:
        log.warning("Login fallido: Nombre de usuario o contraseña incorrectos para '%s'", username)
        return jsonify({'message': 'Nombre de usuario o contraseña incorrectos.'}), 401


@external_api_bp.route('/api/logout', methods=['POST', 'GET'])
def api_logout():
    import logging
    log = logging.getLogger("auth")
    from flask_login import logout_user, current_user
    from flask import session, jsonify

    if current_user.is_authenticated:
        log.info("Logout solicitado por usuario: %s", current_user)
        logout_user()
        session.clear()
        return jsonify({'message': 'Sesión cerrada correctamente.'}), 200
    else:
        log.info("Logout solicitado sin sesión activa")
        return jsonify({'message': 'No hay sesión activa.'}), 200
