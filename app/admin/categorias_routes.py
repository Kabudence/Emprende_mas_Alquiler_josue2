#from flask import render_template, request, redirect, url_for, flash
#from flask_login import login_required, current_user
#from app import db
#from app.models import Categoria, Negocio, Rubro, TipoCategoria
#from . import admin_bp  # Importa la blueprint de admin

# Ruta para listar categorías
#@admin_bp.route('/categorias')
#@login_required
#def categorias_index():
    # Verifica si el usuario tiene permisos para acceder
    #if current_user.id_tipo_usuario != 1:
        #flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        #return redirect(url_for('admin.dashboard'))

    # Obtiene el negocio del usuario actual
    #negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    #query = request.args.get('buscar', '')
    
    # Si el negocio existe, filtra las categorías por rubro y nombre
    #if negocio:
        #rubro_id = negocio.rubro_id
        #categorias_lista = Categoria.query.filter(
            #Categoria.rubro_id == rubro_id,
            #Categoria.nombre.ilike(f'%{query}%')
        #).all()
    #else:
        #categorias_lista = []
    
    # Renderiza la plantilla con la lista de categorías
    #return render_template('admin/listado_categoria.html', categorias=categorias_lista, query=query)

# Ruta para crear categorías
#@admin_bp.route('/categorias/crear', methods=['GET', 'POST'])
#@login_required
#def categorias_crear():
    # Verifica si el usuario tiene permisos para acceder
    #if current_user.id_tipo_usuario != 1:
        #flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        #return redirect(url_for('admin.dashboard'))

    # Obtiene el negocio del usuario actual
    #negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    
    #if request.method == 'POST':
        #nombre = request.form.get('nombre')
        #tipo_categoria_id = request.form.get('tipo_categoria_id')
        
        # Verifica que el negocio, nombre y tipo de categoría no sean nulos
        #if negocio and nombre and tipo_categoria_id:
            #nueva_categoria = Categoria(nombre=nombre, rubro_id=negocio.rubro_id, tipo_id=tipo_categoria_id)
            #db.session.add(nueva_categoria)
            #db.session.commit()
            #flash('Categoría creada con éxito.', 'success')
    #return render_template('admin/crear_categoria.html', rubros=rubros, tipos_categoria=tipos_categoria, negocio=negocio)

# Ruta para actualizar categorías
#@admin_bp.route('/categorias/actualizar/<int:id>', methods=['GET', 'POST'])
#@login_required
#def categorias_actualizar(id):
    #if current_user.id_tipo_usuario != 1:
        #flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        #return redirect(url_for('admin.dashboard'))

    #categoria = Categoria.query.get_or_404(id)
    #if request.method == 'POST':
        #categoria.nombre = request.form['nombre']
        #categoria.rubro_id = request.form['rubro_id']
        #db.session.commit()
        #flash('Categoría actualizada con éxito', 'success')
        #return redirect(url_for('admin.categorias_index'))
    #rubros = Rubro.query.all()
    #return render_template('admin/actualizar_categoria.html', categoria=categoria, rubros=rubros)

# Ruta para eliminar categorías
#@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
#@login_required
#def categorias_eliminar(id):
    #if current_user.id_tipo_usuario != 1:
        #flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        #return redirect(url_for('admin.dashboard'))

    #categoria = Categoria.query.get_or_404(id)
    #negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    #if negocio and categoria.rubro_id == negocio.rubro_id:
        #db.session.delete(categoria)
        #db.session.commit()
        #flash('Categoría eliminada con éxito.', 'success')
    #else:
        #flash('No tienes permisos para eliminar esta categoría o la categoría no existe.', 'danger')
    #return redirect(url_for('admin.categorias_index'))