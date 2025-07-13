import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_required
from ..models import PoliticaInterna, Negocio
from ..database import db
from . import politicas_restricciones
from datetime import datetime
from datetime import date




def get_current_business():
    """Obtiene el negocio del usuario actual (similar a servicios)"""
    return Negocio.query.filter_by(usuario_id=current_user.id).first()

@politicas_restricciones.route('/', methods=['GET'])
@login_required
def index():
    try:
        negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
        if not negocio:
            flash('No tienes un negocio asociado', 'danger')
            return redirect(url_for('politicas_restricciones.listar'))
        
        busqueda = request.args.get('busqueda', '')
        
        # Base query filtrada por negocio
        query = PoliticaInterna.query.filter_by(id_negocio=negocio.id)
        
        if busqueda:
            query = query.filter(PoliticaInterna.nombre_politica.ilike(f'%{busqueda}%'))
        
        politicas = query.all()
        
        return render_template(
            'politicas_restricciones/listar_politicas.html', 
            politicas=politicas, 
            busqueda=busqueda
        )
    
    except Exception as e:
        flash(f'Error al obtener políticas: {str(e)}', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))

@politicas_restricciones.route('/listar', methods=['GET'])
@login_required
def listar():
    try:
        negocio = get_current_business()
        if not negocio:
            flash('No tienes un negocio asociado', 'danger')
            return redirect(url_for('politicas_restricciones.index'))
        
        busqueda = request.args.get('busqueda', '')
        
        # Filtrar por negocio y búsqueda
        query = PoliticaInterna.query.filter_by(id_negocio=negocio.id)
        
        if busqueda:
            query = query.filter(PoliticaInterna.nombre_politica.ilike(f'%{busqueda}%'))
        
        politicas = query.all()
        return render_template('politicas_restricciones/listar_politicas.html', politicas=politicas, busqueda=busqueda)
    
    except Exception as e:
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))

# Ruta para crear una política
@politicas_restricciones.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    negocio = get_current_business()
    if not negocio:
        flash('No tienes un negocio asociado', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))
    
    if request.method == 'POST':
        try:
            nueva_politica = PoliticaInterna(
                nombre_politica=request.form.get('nombre_politica'),
                descripcion=request.form.get('descripcion'),
                fecha_creacion=date.today(),
                fecha_implementacion=request.form.get('fecha_implementacion'),
                id_negocio=negocio.id  # Asignar el negocio
            )
            db.session.add(nueva_politica)
            db.session.commit()
            flash('Política creada', 'success')
            return redirect(url_for('politicas_restricciones.listar'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    
    return render_template('politicas_restricciones/crear_politica.html', fecha_creacion=date.today())


@politicas_restricciones.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    negocio = get_current_business()
    if not negocio:
        flash('No tienes un negocio', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))
    
    politica = PoliticaInterna.query.filter_by(id=id, id_negocio=negocio.id).first()
    if not politica:
        flash('Política no encontrada', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))

    if request.method == 'POST':
        try:
            # Actualizar solo los campos editables
            politica.nombre_politica = request.form.get('nombre_politica')
            politica.descripcion = request.form.get('descripcion')
            # Si quieres permitir editar la fecha de implementación, descomenta la línea siguiente:
            # politica.fecha_implementacion = request.form.get('fecha_implementacion')

            db.session.commit()
            flash('Política actualizada correctamente', 'success')
            return redirect(url_for('politicas_restricciones.listar'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la política interna: {e}', 'danger')

    # GET o si ocurre error, renderiza el formulario con los datos actuales
    return render_template('politicas_restricciones/editar_politicas.html', politica=politica)


@politicas_restricciones.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        # Obtener el negocio actual del usuario
        negocio = get_current_business()
        if not negocio:
            flash('No tienes un negocio asociado', 'danger')
            return redirect(url_for('politicas_restricciones.listar'))
        
        # Buscar la política SOLO del negocio actual
        politica = PoliticaInterna.query.filter_by(
            id=id, 
            id_negocio=negocio.id  # Filtro clave de Multi-Tenant
        ).first()

        if not politica:
            flash('Política no encontrada o no tienes permisos', 'danger')
            return redirect(url_for('politicas_restricciones.listar'))

        # Eliminar la política
        db.session.delete(politica)
        db.session.commit()
        
        flash('Política eliminada correctamente', 'success')
        return redirect(url_for('politicas_restricciones.listar'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
        return redirect(url_for('politicas_restricciones.listar'))
