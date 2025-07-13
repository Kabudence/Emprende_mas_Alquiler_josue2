from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text
from app.database import db
from app.models import Sucursal, Negocio

sucursales_blueprint = Blueprint(
    'sucursales', __name__,
    template_folder='templates',
    static_folder='static'
)

@sucursales_blueprint.route('/')
@login_required
def listar_sucursales():
    # Obtener negocio del usuario
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash("Primero debe crear un negocio", "danger")
        return redirect(url_for('negocios.crear'))
    
    query = text("""
        SELECT s.ID, s.NombreSucursal, s.Distrito, s.Direccion, 
               s.Correo, s.Celular, s.Estado 
        FROM sucursales s 
        WHERE s.id_negocio = :negocio_id
    """)
    sucursales = db.session.execute(query, {'negocio_id': negocio.id}).fetchall()
    return render_template('index.html', sucursales=sucursales)

@sucursales_blueprint.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_sucursal():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash("Debe tener un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))
    
    if request.method == 'POST':
        try:
            print('POST recibido:', request.form)
            data = {
                'id_negocio': negocio.id,  # está bien, coincide
    'NombreSucursal': request.form['nombre_sucursal'],
    'Distrito': request.form['distrito'],
    'Direccion': request.form['direccion'],
    'Correo': request.form['correo'],
    'Celular': request.form['celular'],
    'Latitud': request.form['latitud'],
    'Longitud': request.form['longitud'],
    'Estado': request.form['estado']

            }
            print('Data lista para crear:', data)
            
            nueva_sucursal = Sucursal(**data)
            db.session.add(nueva_sucursal)
            db.session.commit()
            
            flash('Sucursal creada exitosamente!', 'success')
            return redirect(url_for('sucursales.listar_sucursales'))
        
        except Exception as e:
            db.session.rollback()
            print('ERROR EN CREAR:', e)
            flash(f'Error al crear sucursal: {str(e)}', 'danger')
    
    distritos = db.session.execute(text("SELECT * FROM distritos")).fetchall()
    return render_template('create_sucursal.html', distritos=distritos, negocio=negocio)

@sucursales_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_sucursal(id):
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash("Operación no permitida", "danger")
        return redirect(url_for('sucursales.listar_sucursales'))
    
    
    # Verificar pertenencia
    sucursal = Sucursal.query.filter_by(ID=id, id_negocio=negocio.id).first()

    
    if not sucursal:
        flash("Sucursal no encontrada", "danger")
        return redirect(url_for('sucursales.listar_sucursales'))
    
    if request.method == 'POST':
        try:
            sucursal.NombreSucursal = request.form['nombre_sucursal']
            sucursal.Distrito = request.form['distrito']
            sucursal.Direccion = request.form['direccion']
            sucursal.Correo = request.form['correo']
            sucursal.Celular = request.form['celular']
            sucursal.Latitud = request.form['latitud']
            sucursal.Longitud = request.form['longitud']
            sucursal.Estado = request.form['estado']
            
            db.session.commit()
            flash('Sucursal actualizada!', 'success')
            return redirect(url_for('sucursales.listar_sucursales'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    distritos = db.session.execute(text("SELECT * FROM distritos")).fetchall()
    return render_template(
        'edit_sucursal.html',
        sucursal=sucursal,
        negocio=negocio,  # 🔑 Pasar el negocio al template
        distritos=distritos
    )
    return render_template('edit_sucursal.html', sucursal=sucursal, distritos=distritos)