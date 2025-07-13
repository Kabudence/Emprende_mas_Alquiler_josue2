from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import current_user
from . import envios_bp
from ..models import db, Envio, Departamento, Provincia, Distrito, Sucursal, Negocio



def get_current_business():
    """Obtiene el negocio actual del usuario"""
    if hasattr(current_user, 'negocio') and current_user.negocio:
        return current_user.negocio
    elif hasattr(current_user, 'negocios') and current_user.negocios:
        return current_user.negocios[0]
    return None

# LISTAR (Read)
@envios_bp.route('/')
def index():
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('main.index'))
    
    # Filtrar por negocio
    envios = Envio.query.filter_by(id_negocio=negocio.id).all()
    return render_template('listado_envios.html', envios=envios)

# CREAR (Create)
@envios_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        sucursal_id = request.form.get('sucursal')
        departamento_id = request.form.get('departamento')
        provincia_id = request.form.get('provincia')
        distrito_id = request.form.get('distrito')
        costo = request.form.get('costo')
        estado = request.form.get('estado')
        
        # Validaciones simples
        if not (sucursal_id and departamento_id and provincia_id and distrito_id and costo):
            flash("Por favor, complete todos los campos.", "error")
            return redirect(url_for('envios.registrar'))
        
        # Crear y guardar el nuevo envío
        envio = Envio(
            id_negocio=negocio.id,
            sucursal_id=sucursal_id,
            departamento_id=departamento_id,
            provincia_id=provincia_id,
            distrito_id=distrito_id,
            costo=costo,
            estado=estado
        )
        db.session.add(envio)
        db.session.commit()
        
       
        return redirect(url_for('envios.index'))
    
    # Para GET
    sucursales = Sucursal.query.filter_by(id_negocio=negocio.id).all()
    departamentos = Departamento.query.all()  # Si son globales
    return render_template('registrar_envios.html', sucursales=sucursales, departamentos=departamentos)

# EDITAR (Update)
@envios_bp.route('/editar/<int:envio_id>', methods=['GET', 'POST'])
def editar(envio_id):
    # Obtener el negocio actual del usuario
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('main.index'))
    
    # Verificar que el envío pertenece al negocio actual
    envio = Envio.query.filter_by(id=envio_id, id_negocio=negocio.id).first_or_404()
    
    if request.method == 'POST':
        try:
            # Actualizar campos con validación
            envio.sucursal_id = request.form.get('sucursal')
            envio.departamento_id = request.form.get('departamento')
            envio.provincia_id = request.form.get('provincia')
            envio.distrito_id = request.form.get('distrito')
            envio.costo = float(request.form.get('costo', 0))
            envio.estado = request.form.get('estado', 'activo')
            
            # Validación básica
            if not all([envio.sucursal_id, envio.departamento_id, 
                       envio.provincia_id, envio.distrito_id]):
                flash("Complete todos los campos requeridos", "error")
                return redirect(url_for('envios.editar', envio_id=envio_id))
            
            db.session.commit()
            flash("Envío actualizado correctamente.", "success")
            return redirect(url_for('envios.index'))
        
        except ValueError:
            db.session.rollback()
            flash("Error en el formato de los datos", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
    
    # Obtener datos para el formulario FILTRADOS por negocio
    sucursales = Sucursal.query.filter_by(id_negocio=negocio.id).all()
    departamentos = Departamento.query.all()  # Asumiendo que son globales
    
    return render_template('editar_envios.html', 
                         envio=envio, 
                         sucursales=sucursales, 
                         departamentos=departamentos)

# ELIMINAR (Delete)
@envios_bp.route('/eliminar/<int:envio_id>', methods=['POST'])
def eliminar(envio_id):
    negocio = get_current_business()
    if not negocio:
        flash('No tiene un negocio asignado', 'danger')
        return redirect(url_for('main.index'))
    
    envio = Envio.query.filter_by(id=envio_id, id_negocio=negocio.id).first_or_404()

# FILTROS AJAX
@envios_bp.route('/get_provincias/<int:departamento_id>')
def get_provincias(departamento_id):
    provincias = Provincia.query.filter_by(departamento_id=departamento_id).all()
    data = [{'id': p.id, 'nombre': p.nombre} for p in provincias]
    return jsonify(data)

@envios_bp.route('/get_distritos/<int:provincia_id>')
def get_distritos(provincia_id):
    distritos = Distrito.query.filter_by(provincia_id=provincia_id).all()
    data = [{'id': d.ID, 'nombre': d.Nombre} for d in distritos]
    return jsonify(data)
