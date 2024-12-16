import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required
from ..models import Producto, Categoria, ProductoDetalle, Tamanio, Color, Negocio
from ..database import db
from . import productos


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# Index de productos con filtro por rubro y búsqueda
@productos.route('/', methods=['GET'])
@login_required
def index():
    busqueda = request.args.get('busqueda', '').strip()
    negocio = Negocio.query.first()

    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('productos.index'))

    # Filtrar productos por todas las categorías dentro del rubro del negocio
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id).all()
    categoria_ids = [categoria.id for categoria in categorias]

    productos_query = Producto.query.filter(Producto.categoria_id.in_(categoria_ids))

    # Búsqueda por nombre del producto
    if busqueda:
        productos_query = productos_query.filter(Producto.nombre.ilike(f'%{busqueda}%'))

    productos_lista = productos_query.all()
    return render_template('productos/index.html', productos=productos_lista)

@productos.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            # Datos principales del producto
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            categoria_id = request.form.get('categoria_id')

            # Validación de campos obligatorios
            if not all([nombre, categoria_id]):
                flash('Por favor, complete todos los campos obligatorios.', 'danger')
                return redirect(url_for('productos.crear'))

            # Crear el producto principal
            nuevo_producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                categoria_id=categoria_id
            )
            db.session.add(nuevo_producto)
            db.session.commit()

            # Configuración de límites
            max_tamanios = 4
            max_variantes = 3
            
            # Depuración: imprimir qué variantes están activadas o desactivadas
            variantes_estado = []
            for tamanio_index in range(1, max_tamanios + 1):
                for variante_index in range(1, max_variantes + 1):
                    status = request.form.get(f'variant_{tamanio_index}_{variante_index}_status')
                    variantes_estado.append({
                        'tamanio': tamanio_index,
                        'variante': variante_index,
                        'status': status
                    })

            # Iterar por tamaños y variantes habilitados
            for tamanio_index in range(1, max_tamanios + 1):
                tamanio_id = request.form.get(f'size_{tamanio_index}')
                
                # Si no hay tamaño definido, pasar al siguiente
                if not tamanio_id:
                    continue

                for variante_index in range(1, max_variantes + 1):
                    # Verificar si la variante está habilitada
                    variant_status = request.form.get(f'variant_{tamanio_index}_{variante_index}_status')
                    if variant_status != 'active':
                        continue

                    # Obtener datos de la variante habilitada
                    color_id = request.form.get(f'color_{tamanio_index}_{variante_index}')
                    stock = request.form.get(f'stock_{tamanio_index}_{variante_index}')
                    precio = request.form.get(f'precio_{tamanio_index}_{variante_index}')
                    capacidad = request.form.get(f'capacidad_{tamanio_index}_{variante_index}')
                    image_file = request.files.get(f'image_{tamanio_index}_{variante_index}')
                    
                    if not (color_id and stock):  # Si faltan datos, ignorar la variante
                        flash(f'Falta información en la variante {variante_index} del tamaño {tamanio_index}.', 'warning')
                        continue

                    # Procesar la imagen
                    filename = None
                    if image_file and allowed_file(image_file.filename):
                        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                            os.makedirs(current_app.config['UPLOAD_FOLDER'])
                        image_file.save(filepath)
                        filename = unique_filename

                    # Guardar el detalle del producto
                    detalle = ProductoDetalle(
                        producto_id=nuevo_producto.id,
                        tamanio_id=tamanio_id,
                        color_id=color_id,
                        stock=int(stock),
                        precio=precio,
                        capacidad=capacidad,
                        imagen=filename
                    )
                    db.session.add(detalle)

            # Guardar cambios en la base de datos
            db.session.commit()
            flash('Producto creado correctamente.', 'success')
            return redirect(url_for('productos.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {e}', 'danger')
            return redirect(url_for('productos.crear'))

    negocio_actual = Negocio.query.first()
    
    if not negocio_actual:
        flash('No se encontró un negocio en la base de datos','danger')
        return redirect(url_for('productos.index'))

    # Cargar datos para el formulario
    categorias = Categoria.query.filter_by(rubro_id=negocio_actual.rubro_id, tipo_id=1).all()  # Solo categorías tipo 'producto'
    colores = Color.query.all()

    colores_serializables = [{'id': color.id, 'nombre': color.nombre, 'hexadecimal': color.hexadecimal} for color in colores]

    return render_template(
        'productos/crear_producto.html',
        categorias=categorias,
        colores=colores_serializables
    )


@productos.route('/tamanios_por_categoria/<int:categoria_id>', methods=['GET'])
@login_required
def tamanios_por_categoria(categoria_id):
    tamanios = Tamanio.query.filter_by(categoria_id=categoria_id).all()
    tamanios_json = [{'id': t.id, 'nombre': t.nombre} for t in tamanios]
    return jsonify(tamanios_json)

@productos.route('/ver/<int:id>')
def ver_producto(id):
    producto = Producto.query.get_or_404(id)

    producto_modificado = {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'detalles': []
    }

    colores_unicos = {}

    for detalle in producto.detalles:
        color_id = detalle.color_id
        if color_id not in colores_unicos:
            colores_unicos[color_id] = detalle
            
    producto_modificado['detalles'] = list(colores_unicos.values())
    
    return render_template('productos/ver_producto.html', producto=producto_modificado)


@productos.route('/capacidades/<int:id>', methods=['GET'])
def obtener_capacidades(id):
    producto = Producto.query.get_or_404(id)
    color = request.args.get('color')

    detalles = ProductoDetalle.query.filter_by(producto_id=producto.id, color_id=Color.query.filter_by(nombre=color).first().id).all()

    capacidades = {detalle.capacidad: {'precio': detalle.precio, 'stock': detalle.stock} for detalle in detalles}

    return jsonify(capacidades)

@productos.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    negocio_actual = Negocio.query.first()
    # Filtrar las categorías de acuerdo al rubro del negocio y tipo_id = 1
    categorias = Categoria.query.filter_by(rubro_id=negocio_actual.rubro_id, tipo_id=1).all()

    tamanios = Tamanio.query.filter_by(categoria_id=producto.categoria_id).all()
    colores = Color.query.all()

    detalles = ProductoDetalle.query.filter_by(producto_id=producto.id).all()

    if request.method == 'POST':
        # Actualizar información del producto
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.categoria_id = request.form['categoria_id']

        # Guardar cambios en el producto
        try:
            db.session.commit()
            flash('Producto actualizado exitosamente!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto. Intente nuevamente.', 'danger')

        # Actualizar detalles de las variantes (stock, precio, capacidad y color)
        for detalle in detalles:
            detalle.stock = request.form.get(f'stock_{detalle.id}')
            detalle.precio = request.form.get(f'precio_{detalle.id}')
            detalle.capacidad = request.form.get(f'capacidad_{detalle.id}')
            detalle.tamanio_id = request.form.get(f'size_{detalle.id}')
            detalle.color_id = request.form.get(f'color_{detalle.id}')

            # Subir imagen si se cargó una nueva
            image_file = request.files.get(f'image_{detalle.id}')
            if image_file:
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])
                image_file.save(filepath)
                filename = unique_filename
                detalle.imagen = filename

            # Guardar cambios en la variante
            try:
                db.session.commit()
                flash(f'Variante {detalle.id} actualizada correctamente!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar la variante {detalle.id}. Intente nuevamente.', 'danger')

        return redirect(url_for('productos.index', producto_id=producto.id))

    return render_template('productos/editar_producto.html', producto=producto, categorias=categorias, tamanios=tamanios, colores=colores, detalles=detalles)


@productos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    try:
        # Eliminar los detalles asociados al producto
        ProductoDetalle.query.filter_by(producto_id=id).delete()
        
        # Eliminar el producto
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Producto eliminado correctamente.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar el producto: {str(e)}'}), 500
