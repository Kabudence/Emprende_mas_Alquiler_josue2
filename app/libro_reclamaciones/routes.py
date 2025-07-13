from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from config import Config
from ..models import Negocio, db  # Importar db para usar SQLAlchemy
from sqlalchemy import text


# Crear Blueprint
reclamos_bp = Blueprint('reclamos', __name__, template_folder='templates')

UPLOAD_FOLDER = 'app/static/uploads/libroreclamaciones'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_negocio():
    """Obtiene el negocio del usuario actual usando SQLAlchemy"""
    return Negocio.query.filter_by(usuario_id=current_user.id).first()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------------
#                       LISTAR RECLAMOS
# ---------------------------------------------------------------
@reclamos_bp.route('/')
@login_required
def index():
    negocio = get_negocio()
    if not negocio:
        flash("Primero debe crear un negocio", "danger")
        return redirect(url_for('negocios.crear'))

    try:
        # Usar SQLAlchemy para la consulta
        from sqlalchemy import text
        reclamos = db.session.execute(
            text("""
                SELECT id, tipo_documento, numero_documento, nombres_completos, 
                       apellidos, fecha, tipo_respuesta, direccion, telefono, email, 
                       orden_compra, bien_contratado, monto_reclamado, descripcion, 
                       tipo, motivo, detalle_reclamo, pedido, imagen
                FROM libro_reclamos
                WHERE id_negocio = :id_negocio
                ORDER BY fecha DESC
            """), {'id_negocio': negocio.id}
        ).fetchall()

        return render_template('libro_reclamaciones.html', reclamos=reclamos)
    
    except Exception as e:
        flash(f"Error al cargar reclamos: {str(e)}", "danger")
        return redirect(url_for('reclamos.index'))  # Corregido endpoint válido

# ---------------------------------------------------------------
#                       CREAR RECLAMO
# ---------------------------------------------------------------
@reclamos_bp.route('/crear_reclamo', methods=['GET', 'POST'])
@login_required
def crear_reclamo():
    negocio = get_negocio()
    if not negocio:
        flash("Debe tener un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))

    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            campos_requeridos = ['fecha', 'fecha_comunicacion', 'tipo_documento', 
                                'numero_documento', 'nombres_completos', 'apellidos']
            for campo in campos_requeridos:
                if campo not in request.form:
                    raise ValueError(f"Campo requerido faltante: {campo}")

            # Convertir fechas
            fecha = datetime.strptime(request.form['fecha'], "%d/%m/%Y").date()
            fecha_comunicacion = datetime.strptime(
                request.form['fecha_comunicacion'], "%d/%m/%Y"
            ).date()
            
            # Procesar imagen
            nombre_imagen = None
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen and imagen.filename != '' and allowed_file(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    nombre_imagen = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                    imagen.save(os.path.join(UPLOAD_FOLDER, nombre_imagen))

            # Insertar usando SQLAlchemy
            db.session.execute(
                text("""
                    INSERT INTO libro_reclamos 
                    (tipo_documento, numero_documento, nombres_completos, apellidos, fecha, 
                     tipo_respuesta, direccion, departamento, provincia, distrito, telefono, 
                     email, orden_compra, bien_contratado, monto_reclamado, descripcion, 
                     tipo, motivo, detalle_reclamo, pedido, fecha_comunicacion, imagen, id_negocio)
                    VALUES (:tipo_documento, :numero_documento, :nombres, :apellidos, :fecha,
                            :tipo_respuesta, :direccion, :departamento, :provincia, :distrito,
                            :telefono, :email, :orden_compra, :bien_contratado, :monto,
                            :descripcion, :tipo, :motivo, :detalle, :pedido, :fecha_com, 
                            :imagen, :id_negocio)
                """), {
                    'tipo_documento': request.form['tipo_documento'],
                    'numero_documento': request.form['numero_documento'],
                    'nombres': request.form['nombres_completos'],
                    'apellidos': request.form['apellidos'],
                    'fecha': fecha,
                    'tipo_respuesta': request.form.get('tipo_respuesta', ''),
                    'direccion': request.form.get('direccion', ''),
                    'departamento': "Lima",
                    'provincia': "Lima",
                    'distrito': request.form.get('distrito', ''),
                    'telefono': request.form.get('telefono', ''),
                    'email': request.form.get('email', ''),
                    'orden_compra': request.form.get('orden_compra', ''),
                    'bien_contratado': request.form.get('bien_contratado', ''),
                    'monto': request.form.get('monto_reclamado', 0),
                    'descripcion': request.form.get('descripcion', ''),
                    'tipo': request.form.get('tipo', ''),
                    'motivo': request.form.get('motivo', ''),
                    'detalle': request.form.get('detalle_reclamo', ''),
                    'pedido': request.form.get('pedido', ''),
                    'fecha_com': fecha_comunicacion,
                    'imagen': nombre_imagen,
                    'id_negocio': negocio.id
                }
            )
            db.session.commit()
            flash('Reclamo registrado correctamente', 'success')
            return redirect(url_for('reclamos.index'))

        except Exception as e:
            db.session.rollback()
            print("ERROR REGISTRO RECLAMO:", e)  # <-- Así lo ves en la consola/logs
            flash(f'Error al registrar reclamo: {str(e)}', 'danger')
            return redirect(url_for('reclamos.crear_reclamo'))

    else:  # GET
        try:
            # Obtener distritos usando SQLAlchemy
            distritos = db.session.execute(text("SELECT id, nombre FROM distritos")).fetchall()
            return render_template('crear_reclamo.html', distritos=distritos)
        
        except Exception as e:
            flash(f"Error al cargar distritos: {str(e)}", "danger")
            return redirect(url_for('reclamos.index'))