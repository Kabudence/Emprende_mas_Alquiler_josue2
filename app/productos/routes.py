import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required
from ..models import Producto, Categoria, ProductoDetalle, Tamanio, Color
from ..database import db
from . import productos


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@productos.route('/')
@login_required
def index():
    productos_lista = Producto.query.all()
    return render_template('productos/index.html', productos=productos_lista)


@productos.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            # Datos principales del producto
            nombre = request.form.get('nombre')
            precio = request.form.get('precio')
            descripcion = request.form.get('descripcion')
            categoria_id = request.form.get('categoria_id')

            # Validación de campos obligatorios
            if not all([nombre, precio, categoria_id]):
                flash('Por favor, complete todos los campos obligatorios.', 'danger')
                return redirect(url_for('productos.crear'))

            # Crear el producto principal
            nuevo_producto = Producto(
                nombre=nombre,
                precio=precio,
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

            print("Estado de variantes:", variantes_estado)  # Esto mostrará el estado en la consola del servidor


            # Iterar por tamaños y variantes habilitados
            for tamanio_index in range(1, max_tamanios + 1):
                tamanio_id = request.form.get(f'size_{tamanio_index}')
                
                print("El tamanio_id es GAAA: ",tamanio_id)

                # Si no hay tamaño definido, pasar al siguiente
                if not tamanio_id:
                    continue

                for variante_index in range(1, max_variantes + 1):
                    # Verificar si la variante está habilitada
                    variant_status = request.form.get(f'variant_{tamanio_index}_{variante_index}_status')
                    if variant_status != 'active':
                        continue

                    color_name = f'color_{tamanio_index}_{variante_index}'
                    stock_name = f'stock_{tamanio_index}_{variante_index}'
                    image_name = f'image_{tamanio_index}_{variante_index}'

                    # Obtener datos de la variante habilitada
                    color_id = request.form.get(f'color_{tamanio_index}_{variante_index}')
                    print(f"Evaluando el color con name='{color_name}', valor={color_id}")
                    stock = request.form.get(f'stock_{tamanio_index}_{variante_index}')
                    print(f"Evaluando el stock con name='{stock_name}', valor={stock}")
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

    # Cargar datos para el formulario
    categorias = Categoria.query.all()
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
    return render_template('productos/ver_producto.html', producto=producto)
