import os
import json
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
            nombre = request.form.get('nombre')
            precio = request.form.get('precio')
            descripcion = request.form.get('descripcion')
            categoria_id = request.form.get('categoria_id')

            if not all([nombre, precio, categoria_id]):
                flash('Por favor, complete todos los campos obligatorios.', 'danger')
                return redirect(url_for('productos.crear'))

            nuevo_producto = Producto(
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                categoria_id=categoria_id
            )
            db.session.add(nuevo_producto)
            db.session.commit()

            tamanio_index = 1
            while True:
                tamanio_id = request.form.get(f'size_{tamanio_index}')
                
                if not tamanio_id:
                    break

                variante_index = 1
                while True:
                    color_id = request.form.get(f'color_{tamanio_index}_{variante_index}')
                    stock = request.form.get(f'stock_{tamanio_index}_{variante_index}')
                    image_file = request.files.get(f'image_{tamanio_index}_{variante_index}')
                    
                    print(color_id)
                    print(stock)
                    
                    if not color_id:
                        break

                    filename = None
                    if image_file and allowed_file(image_file.filename):
                        filename = secure_filename(image_file.filename)
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                            os.makedirs(current_app.config['UPLOAD_FOLDER'])
                        image_file.save(filepath)

                    detalle = ProductoDetalle(
                        producto_id=nuevo_producto.id,
                        tamanio_id=tamanio_id,
                        color_id=color_id,
                        stock=int(stock),
                        imagen=filename
                    )
                    db.session.add(detalle)
                    variante_index += 1

                tamanio_index += 1

            db.session.commit()
            flash('Producto creado correctamente.', 'success')
            return redirect(url_for('productos.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {e}', 'danger')
            return redirect(url_for('productos.crear'))

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
