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
    usuario = current_user
    return render_template('negocios/index.html', negocio=negocio, rubros=rubros, usuario=usuario)


@negocios.route('/guardar', methods=['POST'])
@login_required
def guardar():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    usuario = current_user

    try:
        # Obtener el ID del rubro seleccionado y el valor del nuevo rubro
        rubro_id = request.form.get('rubro_id')
        nuevo_rubro = request.form.get('nuevo_rubro', '').strip()

        # Determinar el rubro a usar solo si el negocio no existe
        if not negocio:
            if rubro_id == "nuevo" and nuevo_rubro:
                # Crear el nuevo rubro si no existe
                rubro = Rubro.query.filter_by(nombre=nuevo_rubro).first()
                if not rubro:
                    rubro = Rubro(nombre=nuevo_rubro)
                    db.session.add(rubro)
                    db.session.commit()  # Guardar para asignar el ID
            else:
                # Usar el rubro existente seleccionado
                rubro = Rubro.query.get(rubro_id)

            if not rubro:
                raise ValueError("Debe seleccionar un rubro válido o agregar uno nuevo.")
        
        # Actualizar o crear el negocio
        if negocio:
            negocio.nombre = request.form['nombre']
            negocio.ruc = request.form['ruc']
            negocio.razon_social = request.form['razon_social']
            negocio.telefono = request.form['telefono']
            negocio.direccion = request.form['direccion']
            negocio.departamento = request.form['departamento']
            negocio.provincia = request.form['provincia']
            negocio.distrito = request.form['distrito']
            # Mantener el mismo rubro que tenía
            # flash('Negocio actualizado exitosamente.', 'success')
        else:
            nuevo_negocio = Negocio(
                nombre=request.form['nombre'],
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
            # flash('Negocio registrado exitosamente.', 'success')

        # Actualizar datos del usuario
        usuario.nombre = request.form['nombre']
        usuario.username = request.form['username']
        usuario.email = request.form['email']
        if request.form['password']:
            usuario.password = request.form['password']
        db.session.commit()

        # flash('Datos del usuario actualizados exitosamente.', 'success')

    except Exception as e:
        db.session.rollback()
        # flash(f'Ocurrió un error al guardar los datos: {str(e)}', 'danger')

    return redirect(url_for('negocios.index'))
