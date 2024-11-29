from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Negocio, Rubro
from ..database import db
from . import negocios

@negocios.route('/', methods=['GET'])
@login_required
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    rubros = Rubro.query.all()
    return render_template('negocios/index.html', negocio=negocio, rubros=rubros)


@negocios.route('/guardar', methods=['POST'])
@login_required
def guardar():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()

    try:
        # Obtener el nombre del rubro ingresado
        rubro_nombre = request.form['rubro_nombre'].strip()
        rubro = Rubro.query.filter_by(nombre=rubro_nombre).first()

        # Crear el rubro si no existe
        if not rubro:
            rubro = Rubro(nombre=rubro_nombre)
            db.session.add(rubro)
            db.session.commit()  # Guardar para asignar ID al rubro

        # Actualizar o crear el negocio
        if negocio:
            negocio.nombre_negocio = request.form['nombre_negocio']
            negocio.ruc = request.form['ruc']
            negocio.razon_social = request.form['razon_social']
            negocio.telefono = request.form['telefono']
            negocio.direccion = request.form['direccion']
            negocio.departamento = request.form['departamento']
            negocio.provincia = request.form['provincia']
            negocio.distrito = request.form['distrito']
            negocio.rubro_id = rubro.id
            flash('Negocio actualizado exitosamente.', 'success')
        else:
            nuevo_negocio = Negocio(
                nombre_negocio=request.form['nombre_negocio'],
                ruc=request.form['ruc'],
                razon_social=request.form['razon_social'],
                telefono=request.form['telefono'],
                direccion=request.form['direccion'],
                departamento=request.form['departamento'],
                provincia=request.form['provincia'],
                distrito=request.form['distrito'],
                rubro_id=rubro.id,
                usuario_id=current_user.id
            )
            db.session.add(nuevo_negocio)
            flash('Negocio registrado exitosamente.', 'success')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al guardar los datos: {str(e)}', 'danger')

    return redirect(url_for('negocios.index'))