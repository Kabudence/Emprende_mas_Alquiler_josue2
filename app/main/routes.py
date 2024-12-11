from flask import render_template
from flask_login import login_required, current_user
from . import main

@main.route('/')
@login_required 
def dashboard():
    return render_template('dashboard.html', nombre=current_user.nombre)

