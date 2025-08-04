from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, current_user
from ..models import Negocio, Usuario
from ..database import db
from . import auth
from werkzeug.security import check_password_hash  # Para comparar contraseñas hasheadas

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirección rápida si ya está autenticado
        if current_user.tipo_usuario.nombre_tipo == 'administrador':
            return redirect(url_for('admin.dashboard'))
        elif current_user.tipo_usuario.nombre_tipo == 'dueno_tienda':
            return redirect(url_for('main.dashboard'))
        else:
            flash('No tienes permisos para acceder.', 'danger')
            logout_user()
            return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = Usuario.query.filter_by(username=username).first()



        if user and user.password == password:  # Reemplaza esto por check_password_hash si usas hashes
            # Si el usuario es dueño de tienda, verifica negocios bloqueados
            if user.tipo_usuario.nombre_tipo == 'dueno_tienda':
                negocios_bloqueados = Negocio.query.filter(
                    Negocio.usuario_id == user.id,
                    Negocio.bloqueado == True
                ).all()
                if negocios_bloqueados:
                    flash('Acceso denegado: Tienes negocios bloqueados.', 'danger')
                    return redirect(url_for('auth.login'))

            # Inicia sesión
            login_user(user)
            session['user_id'] = user.id
            session['role_id'] = user.id_tipo_usuario

            # --- Buscar el negocio y guardar el id_negocio en sesión ---
            negocio = Negocio.query.filter_by(usuario_id=user.id).first()
            if negocio:
                session['id_negocio'] = negocio.id
            else:
                session['id_negocio'] = None  # O eliminar la clave si prefieres
            # ----------------------------------------------------------

            # Redirección según tipo de usuario
            if user.tipo_usuario.nombre_tipo == 'administrador':
                return redirect(url_for('admin.dashboard'))
            elif user.tipo_usuario.nombre_tipo == 'dueno_tienda':
                return redirect(url_for('main.dashboard'))
            else:
                flash('No tienes permisos para acceder.', 'danger')
                logout_user()
                return redirect(url_for('auth.login'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    session.clear()  # Limpiar la sesión al cerrar sesión
    return redirect(url_for('auth.login'))

