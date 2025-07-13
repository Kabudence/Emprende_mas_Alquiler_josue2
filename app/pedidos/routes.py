import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..database import db
from ..models import Orden, Cliente, OrdenProducto, Sucursal, Negocio

pedidos_bp = Blueprint('pedidos', __name__, template_folder='templates')

def get_negocio():
    """Obtiene el negocio asociado al usuario actual."""
    return Negocio.query.filter_by(usuario_id=current_user.id).first()
@pedidos_bp.route('/')
@login_required
def index():
    negocio = get_negocio()
    if not negocio:
        flash("No tienes un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))
    ordenes = db.session.query(
        Orden.id,
        Cliente.nombre_completo,
        Orden.fecha,
        Orden.forma_pago,
        Orden.estado,
        db.func.coalesce(db.func.sum(OrdenProducto.total), 0).label('total_orden')
    ).join(Cliente, Orden.orden_client_id == Cliente.id) \
     .filter(Cliente.id_negocio == negocio.id) \
     .outerjoin(OrdenProducto, Orden.id == OrdenProducto.orden_id) \
     .group_by(Orden.id, Cliente.nombre_completo, Orden.fecha, Orden.forma_pago, Orden.estado) \
     .order_by(Orden.fecha.desc()) \
     .all()

    return render_template('ordenes.html', ordenes=ordenes)

@pedidos_bp.route('/get_orden/<int:orden_id>')
@login_required
def get_orden(orden_id):
    negocio = get_negocio()
    if not negocio:
        flash("No tienes un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))
    orden = db.session.query(
        Orden.id,
        Cliente.nombre_completo,
        Orden.fecha,
        Orden.forma_pago,
        Orden.estado,
        Orden.costo_envio,
        db.func.coalesce(Orden.comision_culqui, 0).label('comision_culqui'),
        db.func.coalesce(Sucursal.NombreSucursal, 'No asignado').label('sucursal'),
        db.func.coalesce(Orden.distrito, 'No asignado').label('distrito'),
        db.func.coalesce(db.func.sum(OrdenProducto.total), 0).label('subtotal'),
        (db.func.coalesce(db.func.sum(OrdenProducto.total), 0) + Orden.costo_envio + db.func.coalesce(Orden.comision_culqui, 0)).label('total')
    ).join(Cliente, Orden.orden_client_id == Cliente.id) \
     .filter(Orden.id == orden_id, Cliente.id_negocio == negocio.id) \
     .outerjoin(OrdenProducto, Orden.id == OrdenProducto.orden_id) \
     .outerjoin(Sucursal, Orden.sucursal_id == Sucursal.ID) \
     .group_by(Orden.id, Cliente.nombre_completo, Orden.fecha, Orden.forma_pago, Orden.estado, Orden.costo_envio, Orden.comision_culqui, Sucursal.NombreSucursal, Orden.distrito) \
     .first()

    productos = OrdenProducto.query.filter_by(orden_id=orden_id).all()
    productos_json = [{'nombre': p.nombre, 'tamaño': p.tamaño, 'color': p.color, 'precio': p.precio, 'cantidad': p.cantidad, 'total': p.total} for p in productos]

    return jsonify({'orden': orden._asdict() if orden else {}, 'productos': productos_json})

@pedidos_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_orden():
    negocio = get_negocio()
    if not negocio:
        flash("No tienes un negocio registrado", "danger")
        return redirect(url_for('negocios.crear'))

    clientes = Cliente.query.with_entities(Cliente.id, Cliente.nombre_completo, Cliente.whatsapp)\
                 .filter(Cliente.id_negocio == negocio.id).all()
    sucursales = Sucursal.query.with_entities(Sucursal.ID, Sucursal.NombreSucursal).all()

    formas_pago = ['Tarjeta', 'Yape', 'En Local']
    estados = ['Pagado', 'Pendiente', 'Por pagar']

    if request.method == 'POST':
        try:
            cliente_id = request.form['cliente']
            # Verificar que el cliente seleccionado pertenezca al negocio actual
            cliente_obj = Cliente.query.filter_by(id=cliente_id, id_negocio=negocio.id).first()
            if not cliente_obj:
                flash("El cliente seleccionado no pertenece a tu negocio", "danger")
                return redirect(url_for('pedidos.agregar_orden'))

            forma_pago = request.form['forma_pago']
            costo_envio = float(request.form.get('costo_envio') or 0)
            comision_culqui = float(request.form.get('comision_culqui') or 0)
            estado = request.form['estado']
            sucursal_id = request.form['sucursal_id']
            distrito = request.form['distrito']
            productos_json = request.form.get('productos_json', '[]')
            
            productos = json.loads(productos_json)
            subtotal = sum(float(prod['precio']) * int(prod['cantidad']) for prod in productos)
            total = subtotal + costo_envio + comision_culqui

            nueva_orden = Orden(
                orden_client_id=cliente_id,
                forma_pago=forma_pago,
                costo_envio=costo_envio,
                comision_culqui=comision_culqui,
                estado=estado,
                sucursal_id=sucursal_id,
                distrito=distrito,
                subtotal=subtotal,
                total=total,
                id_negocio=negocio.id,  # Asigna el negocio actual
                fecha=datetime.now()
            )
            db.session.add(nueva_orden)
            db.session.flush()  # Para obtener el ID de la nueva orden

            for producto in productos:
                total_producto = float(producto['precio']) * int(producto['cantidad'])
                nuevo_producto = OrdenProducto(
                    orden_id=nueva_orden.id,
                    nombre=producto['nombre'],
                    tamaño=producto['tamaño'],
                    color=producto['color'],
                    precio=producto['precio'],
                    cantidad=producto['cantidad'],
                    total=total_producto,
                    id_negocio=negocio.id  # Asigna también el id_negocio en cada producto
                )
                db.session.add(nuevo_producto)

            db.session.commit()
            flash("Orden y productos agregados correctamente", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Ocurrió un error: {str(e)}", "danger")

        return redirect(url_for('pedidos.index'))

    return render_template('agregar_orden.html', clientes=clientes, sucursales=sucursales, formas_pago=formas_pago, estados=estados)


@pedidos_bp.route('/get_whatsapp/<int:cliente_id>')
@login_required
def get_whatsapp(cliente_id):
    negocio = get_negocio()
    if not negocio:
        return jsonify({'whatsapp': ''})
    cliente = Cliente.query.filter_by(id=cliente_id, id_negocio=negocio.id).first()
    return jsonify({'whatsapp': cliente.whatsapp if cliente else ''})

@pedidos_bp.route('/get_productos')
@login_required
def get_productos():
    productos = db.session.execute("SELECT id, nombre FROM productos").fetchall()
    productos_json = [{"id": p.id, "nombre": p.nombre} for p in productos]
    return jsonify(productos_json)

@pedidos_bp.route('/get_tamanos/<int:producto_id>')
@login_required
def get_tamanos(producto_id):
    tamanos = db.session.execute("""
        SELECT DISTINCT d.tamanio_id, t.nombre 
        FROM detalles d
        JOIN tamanios t ON d.tamanio_id = t.id
        WHERE d.producto_id = :producto_id
    """, {"producto_id": producto_id}).fetchall()
    tamanos_json = [{'id': t.tamanio_id, 'nombre': t.nombre} for t in tamanos]
    return jsonify(tamanos_json)
