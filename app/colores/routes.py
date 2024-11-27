from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Color
from ..database import db
from . import colores

@colores.route('/')
@login_required
def index():
    colores_lista = Color.query.all()
    return render_template('colores/index.html', colores=colores_lista)

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

    return redirect(url_for('colores.index'))