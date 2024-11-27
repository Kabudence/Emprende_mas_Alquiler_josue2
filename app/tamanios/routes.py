from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models import Tamanio
from ..database import db
from . import tamanios

@tamanios.route('/')
@login_required
def index():
    tamanios_lista = Tamanio.query.all()
    return render_template('tamanios/index.html', tamanios=tamanios_lista)