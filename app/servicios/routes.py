from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Servicio
from ..database import db
from . import servicios

@servicios.route('/')
@login_required
def index():
    return render_template('servicios/index.html')
