from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Oferta, ProductoDetalle, ofertas_detalles, DetalleVenta, Producto, Negocio, Tamanio, Color

import os

# Configuración de subida de archivos
dir_base = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(dir_base, '..', 'static', 'uploads', 'promociones')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

promociones_bp = Blueprint(
    'promociones', __name__,
    template_folder='templates',
    static_folder='static/promociones'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@promociones_bp.before_request
@login_required
def require_negocio():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'danger')
        return redirect(url_for('negocios.crear'))
    return None

# --------------------- LISTAR PROMOCIONES ---------------------
@promociones_bp.route('/')
def index():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    current_app.logger.info(f"[PROMOS][GET] Negocio encontrado: {negocio.id if negocio else 'None'}")

    try:
        promos = (
            Oferta.query
            .options(
                db.joinedload(Oferta.detalles)
                .joinedload(ProductoDetalle.producto),
                db.joinedload(Oferta.detalles)
                .joinedload(ProductoDetalle.tamanio),
                db.joinedload(Oferta.detalles)
                .joinedload(ProductoDetalle.color)
            )
            .filter(Oferta.id_negocio == negocio.id)
            .order_by(Oferta.id.desc())
            .all()
        )
        current_app.logger.info(f"[PROMOS][GET] Promos recuperadas: {len(promos)}")
        for i, promo in enumerate(promos):
            current_app.logger.info(f"Promo[{i}]: {promo.id} - {promo.nombre} - detalles: {len(promo.detalles)}")
            if promo.detalles:
                for d in promo.detalles:
                    current_app.logger.info(
                        f"Detalle: {d.id} | Producto: {getattr(d, 'producto', None)} | Tamanio: {getattr(d, 'tamanio', None)} | Color: {getattr(d, 'color', None)}"
                    )
        return render_template('promociones.html', promociones=promos)
    except Exception as e:
        current_app.logger.error(f'Error cargando promociones: {str(e)}', exc_info=True)
        flash('No se pudieron cargar las promociones', 'danger')
        return render_template('promociones.html', promociones=[])

# --------------------- CREAR PROMOCIÓN ---------------------

# @promociones_bp.route('/crear', methods=['GET', 'POST'])
# def crear():
#     negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
#     if request.method == 'POST':
#         nombre = request.form.get('nombre', 'Oferta de Prueba')
#         tipo = request.form.get('tipo', 'Oferta')
#         estado = request.form.get('estado', 'Activo')
#         detalle_id = request.form.get('detalle_id')
#         cantidad = request.form.get('cantidad')  # <---- ESTA LÍNEA FALTABA

#         detalle = ProductoDetalle.query.filter_by(id=detalle_id).first()
#         print("Detalle encontrado:", detalle)
#         if not detalle:
#             return "Detalle no encontrado", 400

#         oferta = Oferta(
#             nombre=nombre,
#             tipo=tipo,
#             estado=estado,
#             cantidad=int(cantidad) if cantidad else 1,   # <---- CORRECCIÓN FINAL
#             stock=1,
#             id_producto=detalle.producto_id,
#             id_negocio=negocio.id
#         )
#         db.session.add(oferta)
#         db.session.flush()

#         oferta.detalles.append(detalle)
#         db.session.commit()

#         print("Oferta creada:", oferta.id)
#         print("Detalles de la oferta:", [d.id for d in oferta.detalles])

#         return redirect(url_for('promociones.index'))

#     productos = Producto.query.filter_by(id_negocio=negocio.id).all()
#     return render_template('crear.html', productos=productos)
@promociones_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if request.method == 'POST':
        try:
            # Obtén datos del formulario
            nombre = request.form.get('nombre', 'Oferta de Prueba')
            descripcion = request.form.get('descripcion')
            tipo = request.form.get('tipo', 'Oferta')
            estado = request.form.get('estado', 'Activo')
            detalle_id = request.form.get('detalle_id')
            cantidad = request.form.get('cantidad')
            # Precios
            precio_oferta = request.form.get('precio_oferta')
            precio_2x1 = request.form.get('precio_2x1')
            descuento = request.form.get('descuento')
            precio_desc = request.form.get('precio_desc')
            precio_paquete = request.form.get('precio_paquete')
            precio_seg = request.form.get('precio_seg')

            # Validación básica
            if not nombre or not tipo:
                flash('Nombre y tipo son campos obligatorios', 'danger')
                return redirect(url_for('promociones.crear'))

            # Manejo de imagen
            foto = request.files.get('foto_producto')
            foto_nombre = None
            if foto and allowed_file(foto.filename):
                foto_nombre = secure_filename(foto.filename)
                foto.save(os.path.join(UPLOAD_FOLDER, foto_nombre))

            # Busca el detalle
            detalle = ProductoDetalle.query.filter_by(id=detalle_id).first()
            if not detalle:
                flash('Detalle no encontrado', 'danger')
                return redirect(url_for('promociones.crear'))

            # Crea la oferta
            oferta = Oferta(
                nombre=nombre,
                descripcion=descripcion,
                tipo=tipo,
                estado=estado,
                cantidad=int(cantidad) if cantidad else 1,
                stock=1,
                id_producto=detalle.producto_id,
                id_negocio=negocio.id,
                precio_oferta=float(precio_oferta) if precio_oferta else None,
                precio_2x1=float(precio_2x1) if precio_2x1 else None,
                descuento=float(descuento) if descuento else None,
                precio_desc=float(precio_desc) if precio_desc else None,
                precio_paquete=float(precio_paquete) if precio_paquete else None,
                precio_seg=float(precio_seg) if precio_seg else None,
                foto_producto=foto_nombre
            )
            db.session.add(oferta)
            db.session.flush()

            oferta.detalles.append(detalle)
            db.session.commit()

            flash('Promoción creada exitosamente', 'success')
            return redirect(url_for('promociones.index'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creando promoción: {str(e)}', exc_info=True)
            flash(f'Error al crear promoción: {str(e)}', 'danger')
            return redirect(url_for('promociones.crear'))

    # GET request
    productos = Producto.query.filter_by(id_negocio=negocio.id).all()
    return render_template('crear.html', productos=productos)




# --------------------- OBTENER DETALLES AJAX ---------------------
@promociones_bp.route('/detalles/<int:producto_id>')
def obtener_detalles_producto(producto_id):
    detalles = db.session.query(
        ProductoDetalle.id,
        Tamanio.nombre.label('tamanio'),
        Color.nombre.label('color'),
        ProductoDetalle.precio
    ).join(Tamanio, ProductoDetalle.tamanio_id == Tamanio.id
    ).join(Color, ProductoDetalle.color_id == Color.id
    ).filter(ProductoDetalle.producto_id == producto_id).all()

    resultados = [{
        'id': detalle.id,
        'tamanio_color': f"{detalle.tamanio} - {detalle.color}",
        'precio': float(detalle.precio)
    } for detalle in detalles]

    return jsonify(resultados)

# --------------------- ELIMINAR PROMOCIÓN ---------------------
@promociones_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    oferta = Oferta.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    try:
        # Borrar la relación en la tabla intermedia
        delete_stmt = ofertas_detalles.delete().where(ofertas_detalles.c.id_oferta == id)
        db.session.execute(delete_stmt)

        db.session.delete(oferta)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False}), 500

# --------------------- EDITAR PROMOCIÓN ---------------------
@promociones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    oferta = Oferta.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    if request.method == 'POST':
        oferta.nombre = request.form.get('nombre')
        oferta.descripcion = request.form.get('descripcion')
        oferta.tipo = request.form.get('tipo')
        oferta.stock = int(request.form.get('stock', oferta.stock))
        oferta.estado = request.form.get('estado')
        # Aquí puedes añadir lógica para actualizar la imagen si es necesario

        try:
            db.session.commit()
            flash('Promoción actualizada', 'success')
            return redirect(url_for('promociones.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar', 'danger')
    return render_template('editar.html', promocion=oferta)
