from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Negocio, Rubro
from ..database import db
from . import politicas_restricciones

@politicas_restricciones.route('/', methods=['GET'])
@login_required
def index():
    return render_template('politicas_restricciones/index.html')
