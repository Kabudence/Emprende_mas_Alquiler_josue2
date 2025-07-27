from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from ..models import Local, Servicio, Negocio, Categoria, ServicioCompleto, TipoServicio
from ..database import db
from . import servicios
import re


@servicios.app_template_filter('youtube_id')
def youtube_id_filter(url):
    if not url:
        return ''

    m = re.search(r'(?:v=|youtu\.be/)([^&?/]+)', url)
    return m.group(1) if m else ''


# Configura la carpeta de carga
UPLOAD_FOLDER = 'app/static/uploads/servicios'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_business():
    """Obtiene el negocio actual del usuario autenticado"""
    if hasattr(current_user, 'negocio') and current_user.negocio:
        return current_user.negocio
    elif hasattr(current_user, 'negocios') and current_user.negocios:
        return current_user.negocios[0]
    return None


@servicios.route('/')
@login_required
def index():
    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio.', 'danger')
        return redirect(url_for('servicios.index'))
    locales = Local.query.filter_by(usuario_id=current_user.id).all()
    # Traer todos los tipos de servicio
    tipos_servicio = TipoServicio.query.order_by(TipoServicio.nombre_servicio).all()

    # Leer filtro de tipo de servicio desde la query string
    tipo_seleccionado = request.args.get('tipo_servicio_id', type=int)

    # Filtrar categorías del rubro y tipo servicio
    categorias = Categoria.query.filter_by(
        rubro_id=negocio.rubro_id,
        tipo_id=2
    ).all()

    # Construir la query base de servicios del negocio
    q = Servicio.query.filter(
        Servicio.categoria_id.in_([c.id for c in categorias]),
        Servicio.id_negocio == negocio.id
    )

    # Aplicar filtro por tipo de servicio si se proporcionó
    if tipo_seleccionado:
        q = q.filter(Servicio.tipo_servicio_id == tipo_seleccionado)

    servicios_lista = q.all()

    return render_template(
        'servicios/index.html',
        servicios=servicios_lista,
        tipos_servicio=tipos_servicio,
        locales=locales,
        tipo_seleccionado=tipo_seleccionado
    )


@servicios.route('/crear', methods=['GET'])
@login_required
def crear():
    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    # Obtener las categorías del rubro con tipo_id = 2 (servicios)
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id, tipo_id=2).all()

    return render_template('servicios/crear_servicio.html', categorias=categorias)


@servicios.route('/crear', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    categoria_id = request.form.get('categoria_id')
    archivo_imagen = request.files.get('imagen')
    video = request.form.get('video')

    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    if archivo_imagen and allowed_file(archivo_imagen.filename):
        # Generar un nombre único para la imagen
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(archivo_imagen.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        archivo_imagen.save(filepath)
        imagen_nombre = unique_filename
    else:
        imagen_nombre = None

    # Importante: asignar el id del negocio al servicio
    nuevo_servicio = Servicio(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        precio_oferta=precio_oferta,
        imagen=imagen_nombre,
        video=video if video else None,
        telefono=telefono,
        correo=correo,
        categoria_id=categoria_id,
        id_negocio=negocio.id  # Se asigna el negocio actual
    )
    db.session.add(nuevo_servicio)
    db.session.commit()

    flash('Servicio creado con éxito', 'success')
    return redirect(url_for('servicios.index'))


@servicios.route('/editar/<int:id>', methods=['GET'])
@login_required
def editar(id):
    servicio = Servicio.query.get_or_404(id)
    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    # Obtener las categorías del rubro con tipo_id = 2 (servicios)
    categorias = Categoria.query.filter_by(rubro_id=negocio.rubro_id, tipo_id=2).all()

    return render_template('servicios/editar_servicio.html', servicio=servicio, categorias=categorias)


@servicios.route('/editar/<int:id>', methods=['POST'])
@login_required
def actualizar(id):
    servicio = Servicio.query.get_or_404(id)
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    precio_oferta = request.form.get('precio_oferta')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    categoria_id = request.form.get('categoria_id')
    archivo_imagen = request.files.get('imagen')
    video = request.form.get('video')

    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio asociado al usuario.', 'danger')
        return redirect(url_for('servicios.index'))

    servicio.nombre = nombre
    servicio.descripcion = descripcion
    servicio.precio = precio
    servicio.precio_oferta = precio_oferta
    servicio.telefono = telefono
    servicio.correo = correo
    servicio.categoria_id = categoria_id
    servicio.video = video

    if archivo_imagen and allowed_file(archivo_imagen.filename):
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(archivo_imagen.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        archivo_imagen.save(filepath)
        servicio.imagen = unique_filename

    db.session.commit()

    flash('Servicio actualizado con éxito', 'success')
    return redirect(url_for('servicios.index'))


@servicios.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()

    flash('Servicio eliminado con éxito', 'success')
    return redirect(url_for('servicios.index'))


@servicios.route('/crear_completo', methods=['GET', 'POST'])
def crear_completo():
    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio', 'danger')
        return redirect(url_for('servicios.index'))

    locales = Local.query.filter_by(usuario_id=current_user.id).all()
    tipos_servicio = TipoServicio.query.all()

    if request.method == 'POST':
        from decimal import Decimal

        # ---------- DATOS DEL FORM ----------
        titulo  = request.form['titulo_publicacion']
        estado  = request.form['estado']
        tipo_id = request.form['tipo_servicio_id']

        precio          = Decimal(request.form.get('precio') or 0)
        precio_oferta   = request.form.get('precio_oferta')
        porcentaje_desc = request.form.get('porcentaje_descuento')
        tipo_oferta     = request.form.get('tipo_oferta', 'Oferta')

        # --- calcular precio_oferta según tipo_oferta ---
        if tipo_oferta == '2x1':
            precio_oferta = precio
        elif tipo_oferta == 'Descuento' and porcentaje_desc:
            precio_oferta = precio - (precio * Decimal(porcentaje_desc) / 100)
        else:  # Oferta libre o sin oferta
            precio_oferta = Decimal(precio_oferta or 0)

        # … (resto de campos sin cambios) …

        nuevo = ServicioCompleto(
            titulo_publicacion=titulo,
            estado=estado,
            tipo_servicio_id=tipo_id,
            # …otros campos…,
            precio=precio,
            precio_oferta=precio_oferta,
            tipo_oferta=tipo_oferta,
            id_negocio=negocio.id,
            en_venta=bool(int(request.form.get('en_venta', '1'))),
            # …etc…
        )
        # locales…
        db.session.add(nuevo)
        db.session.commit()
        flash('Servicio completo creado exitosamente', 'success')
        return redirect(url_for('servicios.completo_index'))

    return render_template('servicios/crear_servicio_completo.html',
                           tipos_servicio=tipos_servicio,
                           locales=locales)


@servicios.route('/completos')
@login_required
def completo_index():
    negocio = get_current_business()
    if not negocio:
        flash('No se encontró un negocio.', 'danger')
        return redirect(url_for('servicios.index'))

    servicios_completos = ServicioCompleto.query.filter_by(id_negocio=negocio.id).all()
    return render_template('servicios/index_servicio_completo.html', servicios=servicios_completos)


@servicios.route('/editar_completo/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_completo(id):
    print(f"[DEBUG] Entrando a editar_completo con id={id}")
    servicio = ServicioCompleto.query.get_or_404(id)
    negocio = get_current_business()
    locales = Local.query.filter_by(usuario_id=current_user.id).all()
    tipos_servicio = TipoServicio.query.all()
    if request.method == 'POST':
        print(f"[DEBUG] Método POST recibido en editar_completo para id={id}")
        try:
            # Actualizar campos básicos
            print("[DEBUG] Actualizando campos básicos del servicio...")
            servicio.titulo_publicacion = request.form['titulo_publicacion']
            servicio.estado = request.form['estado']
            servicio.tipo_servicio_id = request.form['tipo_servicio_id']
            servicio.subtitulo1 = request.form['subtitulo1']
            servicio.descripcion1 = request.form['descripcion1']
            servicio.subtitulo2 = request.form.get('subtitulo2')
            servicio.descripcion2 = request.form.get('descripcion2')
            servicio.subtitulo3 = request.form.get('subtitulo3')
            servicio.descripcion3 = request.form.get('descripcion3')
            servicio.precio = request.form.get('precio') or 0
            servicio.precio_oferta = request.form.get('precio_oferta') or None
            servicio.en_venta = bool(int(request.form.get('en_venta', '1')))
            print(
                f"[DEBUG] Campos básicos actualizados: {servicio.titulo_publicacion}, {servicio.estado}, {servicio.precio}")

            # Nuevos campos
            servicio.precio_promocion = int(request.form.get('precio_promocion', 0))
            servicio.tiempo_duracion = request.form.get('tiempo_duracion')
            print(
                f"[DEBUG] Nuevos campos: precio_promocion={servicio.precio_promocion}, tiempo_duracion={servicio.tiempo_duracion}")

            # Manejo de locales
            print("[DEBUG] Actualizando locales del servicio...")
            nuevos_locales_ids = request.form.getlist('locales[]')
            print(f"[DEBUG] IDs de nuevos locales: {nuevos_locales_ids}")
            locales_actuales_ids = [str(local.id) for local in servicio.locales]
            print(f"[DEBUG] IDs de locales actuales: {locales_actuales_ids}")

            for local_id in nuevos_locales_ids:
                if local_id not in locales_actuales_ids:
                    local = Local.query.get(local_id)
                    if local:
                        print(f"[DEBUG] Agregando local con id={local_id}")
                        servicio.locales.append(local)

            for local_id in locales_actuales_ids:
                if local_id not in nuevos_locales_ids:
                    local = Local.query.get(local_id)
                    if local:
                        print(f"[DEBUG] Quitando local con id={local_id}")
                        servicio.locales.remove(local)

            # Manejo de imagen principal
            imagen_file = request.files.get('imagen')
            if imagen_file and allowed_file(imagen_file.filename):
                print(f"[DEBUG] Procesando nueva imagen: {imagen_file.filename}")
                if servicio.imagen:
                    try:
                        print(f"[DEBUG] Eliminando imagen anterior: {servicio.imagen}")
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], servicio.imagen))
                    except Exception as e:
                        print(f"[ERROR] Error eliminando imagen anterior: {str(e)}")
                filename = f"{uuid.uuid4().hex}_{secure_filename(imagen_file.filename)}"
                imagen_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                servicio.imagen = filename
                print(f"[DEBUG] Nueva imagen guardada: {filename}")

            # Función para manejar medios
            def procesar_media(numero):
                print(f"[DEBUG] Procesando media{numero}...")
                tipo_medio = request.form.get(f'tipo_medio{numero}')
                media_file = request.files.get(f'media{numero}_imagen')
                video_url = request.form.get(f'media{numero}_video_url')
                if tipo_medio == 'imagen' and media_file and allowed_file(media_file.filename):
                    filename = f"{uuid.uuid4().hex}_{secure_filename(media_file.filename)}"
                    media_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    print(f"[DEBUG] Imagen media{numero} guardada: {filename}")
                    return filename
                elif tipo_medio == 'video' and video_url:
                    print(f"[DEBUG] URL video media{numero}: {video_url}")
                    return video_url
                print(f"[DEBUG] Ningún medio válido para media{numero}")
                return None

            servicio.media1 = procesar_media('1')
            servicio.media2 = procesar_media('2')

            print("[DEBUG] Intentando guardar cambios en la base de datos...")
            db.session.commit()
            print("[DEBUG] Servicio actualizado exitosamente")
            flash('Servicio actualizado exitosamente', 'success')
            return redirect(url_for('servicios.completo_index'))

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error al actualizar el servicio: {str(e)}")
            flash(f'Error al actualizar el servicio: {str(e)}', 'danger')

    return render_template('servicios/editar_servicio_completo.html',
                           servicio=servicio,
                           tipos_servicio=tipos_servicio,
                           locales=locales)


@servicios.route('/completos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_completo(id):
    servicio = ServicioCompleto.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    flash('Servicio completo eliminado', 'success')
    return redirect(url_for('servicios.completo_index'))