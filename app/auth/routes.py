from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from ..models import Usuario
from ..database import db
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario.query.filter_by(username=username).first()

        if user and user.password == password:
            if user.tipo_usuario == 'business_owner':
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash('No tienes permisos para acceder como propietario de negocio', 'danger')
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
