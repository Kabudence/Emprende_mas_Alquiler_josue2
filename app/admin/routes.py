from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.InformacionEmpresa.routes import allowed_file
from app.models import Categoria, TipoCategoria, TipoMembresia, TipoModelo, Usuario, Negocio, TipoUsuario, Rubro
from werkzeug.utils import secure_filename
import os
from sqlalchemy.orm import joinedload

UPLOAD_FOLDER = 'app/static/uploads/dni_usuarios'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe


admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Dashboard del administrador
@admin_bp.route('/')
@login_required
def dashboard():
    if current_user.id_tipo_usuario != 1:  # Suponiendo que 1 es el ID para administradores
        flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        return redirect(url_for('auth.login')) 
    return render_template('admin/admin_dashboard.html', user=current_user)

# Registro de Usuario
@admin_bp.route('/registrar_usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form.get('dni', '')
        correo = request.form['correo']
        celular = request.form['celular']
        contrasena = request.form['contrasena']
        username = ''.join(nombre.split()).lower()
        id_tipo_usuario = request.form.get('id_tipo_usuario')
        if not id_tipo_usuario:
            flash('Debes seleccionar un tipo de usuario.', 'danger')
            return redirect(url_for('admin.registrar_usuario'))

        try:
            id_tipo_usuario = int(id_tipo_usuario)
        except ValueError:
            flash('Tipo de usuario inválido.', 'danger')
            return redirect(url_for('admin.registrar_usuario'))

        if id_tipo_usuario not in [1, 2]:
            flash('Tipo de usuario no válido.', 'danger')
            return redirect(url_for('admin.registrar_usuario'))


        

          # Cambios aquí ⬇
        foto_dni_frontal = request.files.get('foto_dni_frontal')
        foto_dni_posterior = request.files.get('foto_dni_posterior')

        frontal_filename = posterior_filename = None
        if foto_dni_frontal and allowed_file(foto_dni_frontal.filename):
            frontal_filename = secure_filename(foto_dni_frontal.filename)
            foto_dni_frontal.save(os.path.join(UPLOAD_FOLDER, frontal_filename))

        if foto_dni_posterior and allowed_file(foto_dni_posterior.filename):
            posterior_filename = secure_filename(foto_dni_posterior.filename)
            foto_dni_posterior.save(os.path.join(UPLOAD_FOLDER, posterior_filename))

        nuevo_usuario = Usuario(
            nombre=nombre,
            dni=dni,
            email=correo,
            celular=celular,
            username=username,
            password=contrasena,
            id_tipo_usuario=id_tipo_usuario,
            foto_dni_frontal=frontal_filename,       # Cambio aquí ⬅
            foto_dni_posterior=posterior_filename    # Cambio aquí ⬅
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado con éxito.', 'success')
        return redirect(url_for('admin.dashboard'))

    tipos = TipoUsuario.query.all()
    return render_template('admin/registro_usuario.html', tipos=tipos)


@admin_bp.route('/negocios/<int:negocio_id>/toggle-bloqueo', methods=['POST'])
def toggle_bloqueo(negocio_id):
    negocio = Negocio.query.get(negocio_id)
    if not negocio:
        return jsonify({'status': 'error', 'message': 'Negocio no encontrado'}), 404

    # Cambiar el estado de bloqueo
    negocio.bloqueado = not negocio.bloqueado
    db.session.commit()

    return jsonify({'status': 'success', 'bloqueado': negocio.bloqueado})

# Registro de Negocio
@admin_bp.route('/registrar_negocio', methods=['GET', 'POST'])
@login_required
def registrar_negocio():
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        # ——— 1) Campos obligatorios de texto ———
        nombre       = request.form.get('nombre_negocio', '').strip()
        ruc          = request.form.get('ruc', '').strip()
        razon_social = request.form.get('razon_social', '').strip()
        direccion    = request.form.get('direccion', '').strip()
        departamento = request.form.get('departamento', '').strip()
        provincia    = request.form.get('provincia', '').strip()
        distrito     = request.form.get('distrito', '').strip()

        # ——— 2) Campos de relaciones y casting ———
        try:
            rubro_id       = int(request.form['rubro_id'])
            usuario_id     = int(request.form['usuario_id'])
            tipo_modelo_id = int(request.form['tipo_modelo'])
        except (KeyError, ValueError):
            flash('Faltan datos o IDs inválidos.', 'danger')
            return redirect(url_for('admin.registrar_negocio'))

        # ——— 3) Validaciones de existencia ———
        rubro   = Rubro.query.get(rubro_id)
        usuario = Usuario.query.get(usuario_id)
        modelo  = TipoModelo.query.get(tipo_modelo_id)
        if not rubro or not usuario or usuario.id_tipo_usuario != 2 or not modelo:
            flash('Rubro, dueño o modelo inválido.', 'danger')
            return redirect(url_for('admin.registrar_negocio'))

        # ——— 4) Si es alquiler, procesar membresía ———
        fecha_fin    = None
        membresia_id = None
        if modelo.nombre == 'alquiler':
            try:
                membresia_id = int(request.form['membresia_id'])
                membresia    = TipoMembresia.query.get(membresia_id)
            except (KeyError, ValueError):
                flash('Debes elegir una membresía para alquiler.', 'danger')
                return redirect(url_for('admin.registrar_negocio'))
            if not membresia:
                flash('Membresía inválida.', 'danger')
                return redirect(url_for('admin.registrar_negocio'))
            fecha_fin = datetime.now() + timedelta(days=membresia.cant_dias)

        # ——— 5) Insertar el negocio ———
        nuevo = Negocio(
            nombre            = nombre,
            ruc               = ruc,
            razon_social      = razon_social,
            direccion         = direccion,
            telefono          = usuario.celular or '',
            departamento      = departamento,
            provincia         = provincia,
            distrito          = distrito,
            rubro_id          = rubro_id,
            usuario_id        = usuario_id,
            tipo_modelo_id    = tipo_modelo_id,
            membresia_id      = membresia_id,
            fecha_fin_alquiler= fecha_fin,
            bloqueado         = False
        )
        db.session.add(nuevo)
        db.session.commit()

        # ——— 6) Guardar colores asociados ———
        color_primario   = request.form.get('color_primario', '#000000')
        color_secundario = request.form.get('color_secundario', '#000000')
        from app.models import colorv  # Asegúrate que el import es correcto según tu estructura

        nuevo_color = colorv(
            Nombre_principal=color_primario,
            Nombre_hexadecimal_principal=color_primario,
            Nombre_secundario=color_secundario,
            Nombre_hexadecimal_secundario=color_secundario,
            idNegocio=nuevo.id
        )
        db.session.add(nuevo_color)
        db.session.commit()
        # ——— Fin de guardar colores ———

        flash('Negocio registrado con éxito.', 'success')
        return redirect(url_for('admin.dashboard'))

    # GET: preparar datos para el formulario
    rubros       = Rubro.query.all()
    usuarios     = Usuario.query.filter_by(id_tipo_usuario=2).all()
    tipo_modelos = TipoModelo.query.all()
    membresias   = TipoMembresia.query.all()
    alquiler_id  = TipoModelo.query.filter_by(nombre='alquiler').first().id

    return render_template(
        'admin/registro_negocio.html',
        rubros           = rubros,
        usuarios         = usuarios,
        tipo_modelos     = tipo_modelos,
        membresias       = membresias,
        tipo_alquiler_id = alquiler_id
    )

# Consultar Usuario
@admin_bp.route('/consultar_usuarios/<int:user_id>')
@login_required
def consultar_usuario(user_id):
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('admin.dashboard'))

    usuarios = Usuario.query.all()  # Obtener todos los usuarios
    return render_template('admin/consultar_usuarios.html', usuarios=usuarios)

# Consultar Negocio
@admin_bp.route('/consultar_negocios')
@login_required
def consultar_negocios():
    # Cargar negocios con relaciones
    negocios = Negocio.query.options(
        joinedload(Negocio.tipo_modelo),
        joinedload(Negocio.membresia)
    ).all()

    negocios_serializables = []
    for negocio in negocios:
        negocios_serializables.append({
            'id': negocio.id,
            'nombre': negocio.nombre,
            'ruc': negocio.ruc,
            'direccion': negocio.direccion,
            'tipo_modelo': negocio.tipo_modelo.nombre if negocio.tipo_modelo else None,
            'membresia': {
                'nombre': negocio.membresia.nombre if negocio.membresia else None,
                'cant_dias': negocio.membresia.cant_dias if negocio.membresia else None
            },
            'fecha_registro': negocio.fecha_registro.strftime('%Y-%m-%d') if negocio.fecha_registro else None,
            'fecha_fin_alquiler': negocio.fecha_fin_alquiler.strftime('%Y-%m-%d') if negocio.fecha_fin_alquiler else None,
            'bloqueado': negocio.bloqueado
        })
    
    ahora = datetime.now()
    return render_template('admin/consultar_negocios.html', 
                         negocios=negocios,  # Pasamos los objetos Negocio directamente
                         ahora=ahora)


@admin_bp.route('/categorias/', methods=['GET'])
@login_required
def categorias_index():
    query = request.args.get('buscar', '')
    if current_user.id_tipo_usuario == 1:
        # Admin: mostrar todas las categorías que coincidan con la búsqueda
        categorias_lista = Categoria.query.filter(
            Categoria.nombre.ilike(f'%{query}%')
        ).all()
    else:
        negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
        if negocio:
            categorias_lista = Categoria.query.filter(
                Categoria.rubro_id == negocio.rubro_id,
                Categoria.nombre.ilike(f'%{query}%')
            ).all()
        else:
            categorias_lista = []
    return render_template('admin/listado_categoria.html', categorias=categorias_lista, query=query)

@admin_bp.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
def categorias_crear():
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # Intentamos obtener el negocio asociado
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    rubros = Rubro.query.all()
    tipos_categoria = TipoCategoria.query.all()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo_categoria_id = request.form.get('tipo_categoria_id')

        # Si existe un negocio, usamos su rubro; de lo contrario, se toma del formulario.
        if negocio:
            rubro_id = negocio.rubro_id
        else:
            rubro_id = request.form.get('rubro_id')

        if rubro_id and nombre and tipo_categoria_id:
            nueva_categoria = Categoria(nombre=nombre, rubro_id=rubro_id, tipo_id=tipo_categoria_id)
            db.session.add(nueva_categoria)
            db.session.commit()
            flash('Categoría creada con éxito.', 'success')
            return redirect(url_for('admin.categorias_index'))
        else:
            flash('Error al crear la categoría. Verifique los datos ingresados.', 'danger')
    
    return render_template('admin/crear_categoria.html', rubros=rubros, tipos_categoria=tipos_categoria, negocio=negocio)


@admin_bp.route('/categorias/actualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def categorias_actualizar(id):
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado. No tienes permisos para ver este panel.', 'danger')
        return redirect(url_for('admin.dashboard'))

    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.rubro_id = request.form['rubro_id']
        db.session.commit()
        flash('Categoría actualizada con éxito', 'success')
        return redirect(url_for('admin.categorias_index'))
    rubros = Rubro.query.all()
    return render_template('admin/actualizar_categoria.html', categoria=categoria, rubros=rubros)

@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
def categorias_eliminar(id):
    if current_user.id_tipo_usuario != 1:
        flash('Acceso denegado. No tienes permisos para esta acción.', 'danger')
        return redirect(url_for('admin.categorias_index'))

    categoria = Categoria.query.get_or_404(id)
    
    # Verificar si hay negocios asociados
    negocios_relacionados = Negocio.query.filter_by(categoria_id=id).count()
    
    if negocios_relacionados > 0:
        flash(f'No se puede eliminar "{categoria.nombre}" porque está siendo usada por {negocios_relacionados} negocios', 'warning')
        return redirect(url_for('admin.categorias_index'))
    
    try:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'danger')
    
    return redirect(url_for('admin.categorias_index'))


@admin_bp.route('/rubros/')
@login_required
def rubros_index():  # Renombra la función para evitar conflictos
    rubros = Rubro.query.all()
    return render_template('admin/index.html', rubros=rubros)

@admin_bp.route('/rubros/search')
@login_required
def rubros_search():
    search_term = request.args.get('q', '')
    rubros = Rubro.query.filter(
        db.or_(
            Rubro.nombre.ilike(f'%{search_term}%'),
            Rubro.descripcion.ilike(f'%{search_term}%')
        )
    ).all()
    return jsonify([{
        'id': r.id,
        'nombre': r.nombre,
        'descripcion': r.descripcion
    } for r in rubros])

@admin_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        # Aquí obtienes la fecha del formulario si lo deseas, aunque en muchos casos se puede asignar automáticamente
        fecha = request.form.get('fecha')
        nombre = request.form.get('nombre')
        descripcion=request.form.get('descripcion', '')
        estado = request.form.get('estado')
        if not nombre:
            flash('El nombre es requerido.', 'danger')
            return redirect(url_for('admin.crear'))
        # Crear el rubro (ajusta según tu modelo)
        nuevo_rubro = Rubro(nombre=nombre,descripcion=descripcion, fecha=fecha, estado=True if estado == 'activo' else False)
        db.session.add(nuevo_rubro)
        db.session.commit()
        flash('Rubro creado con éxito.', 'success')
        return redirect(url_for('admin.rubros_index'))
    now = datetime.utcnow().strftime('%Y-%m-%d')
    return render_template('admin/crear.html', now=now)

@admin_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    rubro = Rubro.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        rubro.descripcion = request.form.get('descripcion', '')
        estado_form = request.form.get('estado')
        if not nombre:
            flash('El nombre es requerido.', 'danger')
            return redirect(url_for('admin.editar', id=id))
        if not estado_form:
            flash('El estado es requerido.', 'danger')
            return redirect(url_for('admin.editar', id=id))
        rubro.nombre = nombre
        
        rubro.estado = estado_form  
        db.session.commit()
        flash('Rubro actualizado con éxito.', 'success')
        return redirect(url_for('admin.rubros_index'))
    return render_template('admin/editar.html', rubro=rubro)

@admin_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    rubro = Rubro.query.get_or_404(id)
    db.session.delete(rubro)
    db.session.commit()
    flash('Rubro eliminado con éxito.', 'success')
    return redirect(url_for('admin.rubros_index'))



@admin_bp.route('/api/usuarios/crear', methods=['POST'])
# @login_required
def api_crear_usuario():
    if current_user.id_tipo_usuario != 1:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.json
    campos_requeridos = ['nombre', 'dni', 'email', 'celular', 'username', 'password', 'id_tipo_usuario']
    if not all(k in data for k in campos_requeridos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    # Validación de unicidad (opcional)
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El username ya existe'}), 409
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 409

    try:
        nuevo_usuario = Usuario(
            nombre = data['nombre'],
            dni = data['dni'],
            email = data['email'],
            celular = data['celular'],
            username = data['username'],
            password = data['password'],
            id_tipo_usuario = data['id_tipo_usuario'],
            foto_dni_frontal = data.get('foto_dni_frontal'),
            foto_dni_posterior = data.get('foto_dni_posterior'),
            user_inviter = data.get('user_inviter'),
            role = data.get('role', 'COMPRADOR')
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario creado', 'id': nuevo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/usuarios/<int:user_id>', methods=['GET'])
# @login_required
def api_usuario_por_id(user_id):
    if current_user.id_tipo_usuario != 1:
        return jsonify({'error': 'No autorizado'}), 403

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'dni': usuario.dni,
        'email': usuario.email,
        'celular': usuario.celular,
        'username': usuario.username,
        'id_tipo_usuario': usuario.id_tipo_usuario,
        'foto_dni_frontal': usuario.foto_dni_frontal,
        'foto_dni_posterior': usuario.foto_dni_posterior,
        'user_inviter': usuario.user_inviter,
        'role': usuario.role,
        'created_at': usuario.created_at.strftime('%Y-%m-%d %H:%M:%S') if usuario.created_at else None
    }
    return jsonify(data)
