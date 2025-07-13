import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date

from ..models import Empresa, colorv, Imagen, RedSocial, Video, Negocio
from ..database import db
from . import Info_Empresa

# Carpeta de subida y tipos de archivos permitidos
UPLOAD_FOLDER = 'app/static/uploads/infoempresa'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def eliminar_imagen_anterior(empresa, tipo_imagen):
    # Buscar y eliminar la imagen anterior, si existe
    imagenes = empresa.imagenes
    for imagen in imagenes:
        if imagen.tipo_imagen == tipo_imagen:
            try:
                os.remove(os.path.join(current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER), imagen.filename))
            except FileNotFoundError:
                pass
            db.session.delete(imagen)
            break

# Ruta para redirigir desde /informacionempresa a /informacion_empresa/listar
@Info_Empresa.route('/informacionempresa')
@login_required
def informacion_empresa():
    return redirect(url_for('informacion_empresa.listar_empresas'))

# Ruta para listar empresas (filtrando por el negocio del usuario)
@Info_Empresa.route('/listar', methods=['GET'])
@login_required
def listar_empresas():
    try:
        # Obtener el negocio del usuario actual
        negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
        if not negocio:
            flash('Primero debe crear un negocio', 'warning')
            return redirect(url_for('negocios.crear'))
        
        # Cargar solo las empresas asociadas al negocio del usuario
        empresas = Empresa.query.options(
            db.joinedload(Empresa.negocio),
            db.joinedload(Empresa.imagenes),
            db.joinedload(Empresa.colores)
        ).filter_by(idNegocio=negocio.id).all()
        
        # Debug: Verificar datos
        for empresa in empresas:
            print(f"\nEmpresa ID: {empresa.idEmpresa}")
            print(f"Negocio: {empresa.negocio.nombre if empresa.negocio else 'None'}")
            print(f"Misión: {empresa.Mision}")
            print(f"Visión: {empresa.Vision}")
            print(f"Objetivos: {empresa.Objetivos}")
            print(f"Imágenes: {len(empresa.imagenes)}")
            print(f"Color: {empresa.colores.Nombre_hexadecimal_principal if empresa.colores else 'None'}")
        
        return render_template('InformacionEmpresa/listado.html', empresas=empresas)          
    except Exception as e:
        current_app.logger.error(f"Error al cargar información: {str(e)}", exc_info=True)
        flash("Error al cargar información", "danger")
        return render_template('InformacionEmpresa/listado.html', empresas=[])

# Ruta para crear una empresa (asociándola al negocio del usuario)
@Info_Empresa.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_empresa():
    # Obtener el negocio del usuario actual
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash("Primero debe crear un negocio", "warning")
        return redirect(url_for('negocios.crear'))

    if request.method == 'POST':
        print("Datos recibidos:", request.form)
        try:
            idNegocio = negocio.id
            
            mision = request.form.get('mision')
            vision = request.form.get('vision')
            objetivos = request.form.get('objetivos')
            color_prim = request.form.get('color_prim')
            color_hexadecimal_prim = request.form.get('color_hexadecimal_prim')
            color_sec = request.form.get('color_sec')
            color_hexadecimal_sec = request.form.get('color_hexadecimal_sec')

            nueva_empresa = Empresa(
                idNegocio=idNegocio,
                Mision=mision,
                Vision=vision,
                Objetivos=objetivos
            )
            db.session.add(nueva_empresa)
            db.session.flush()  # Para obtener el idEmpresa asignado
            
            print(f"Nueva empresa ID: {nueva_empresa.idEmpresa}")

            if color_hexadecimal_prim:
                nuevo_color = colorv(
                    Nombre_principal=color_prim,
                    Nombre_hexadecimal_principal=color_hexadecimal_prim,
                    Nombre_secundario=color_sec,
                    Nombre_hexadecimal_secundario=color_hexadecimal_sec,
                    idNegocio=idNegocio
                )
                db.session.add(nuevo_color)

            # Manejo de imágenes (logo e icono)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
            if 'logo' in request.files:
                logo = request.files['logo']
                if logo and allowed_file(logo.filename):
                    logo_filename = f"logo_{nueva_empresa.idEmpresa}_{uuid.uuid4().hex}.png"
                    logo_path = os.path.join(upload_folder, logo_filename)
                    logo.save(logo_path)
                    imagen_logo = Imagen(
                        tipo_imagen='logo',
                        filename=logo_filename,
                        idNegocio=idNegocio
                    )
                    db.session.add(imagen_logo)

            if 'icono' in request.files:
                icono = request.files['icono']
                if icono and allowed_file(icono.filename):
                    icono_filename = f"icono_{nueva_empresa.idEmpresa}_{uuid.uuid4().hex}.png"
                    icono_path = os.path.join(upload_folder, icono_filename)
                    icono.save(icono_path)
                    imagen_icono = Imagen(
                        tipo_imagen='icono',
                        filename=icono_filename,
                        idNegocio=idNegocio
                    )
                    db.session.add(imagen_icono)

            # Manejo de redes sociales
            if request.form.get('facebook_url'):
                facebook_url = request.form.get('facebook_url')
                red_facebook = RedSocial(
                    nombre_red='Facebook',
                    url_red=facebook_url,
                    idNegocio=idNegocio
                )
                db.session.add(red_facebook)

            if request.form.get('instagram_url'):
                instagram_url = request.form.get('instagram_url')
                red_instagram = RedSocial(
                    nombre_red='Instagram',
                    url_red=instagram_url,
                    idNegocio=idNegocio
                )
                db.session.add(red_instagram)

            # Manejo de videos de YouTube
            if request.form.get('youtube_url_1'):
                youtube_url_1 = request.form.get('youtube_url_1')
                video_1 = Video(
                    tipo='YouTube',
                    url=youtube_url_1,
                    idNegocio=idNegocio
                )
                db.session.add(video_1)

            if request.form.get('youtube_url_2'):
                youtube_url_2 = request.form.get('youtube_url_2')
                video_2 = Video(
                    tipo='YouTube',
                    url=youtube_url_2,
                    idNegocio=idNegocio
                )
                db.session.add(video_2)

            db.session.commit()
            flash('Empresa creada exitosamente.', 'success')
            return redirect(url_for('informacion_empresa.listar_empresas'))

        except Exception as e:
            db.session.rollback()
            print(f"Error en crear_empresa: {str(e)}")
            flash(f"Error al crear empresa: {str(e)}", 'danger')

    return render_template('InformacionEmpresa/formulario.html', empresa=None, negocio=negocio)

# Ruta para editar una empresa (solo si pertenece al negocio del usuario)
@Info_Empresa.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_empresa(id):
    # Obtener el negocio del usuario actual
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'warning')
        return redirect(url_for('negocios.crear'))
    
    # Cargar la empresa y verificar que pertenezca al negocio del usuario
    empresa = Empresa.query.options(db.joinedload(Empresa.negocio)).get_or_404(id)
    if empresa.idNegocio != negocio.id:
        flash('No tiene permisos para editar esta empresa', 'danger')
        return redirect(url_for('informacion_empresa.listar_empresas'))
    
    color = colorv.query.filter_by(idNegocio=empresa.idNegocio).first()
    redes_sociales = RedSocial.query.filter_by(idNegocio=empresa.idNegocio).all()
    videos = Video.query.filter_by(idNegocio=empresa.idNegocio).all()

    if request.method == 'POST':
        try:
            empresa.Mision = request.form.get('mision')
            empresa.Vision = request.form.get('vision')
            empresa.Objetivos = request.form.get('objetivos')

            # Actualizar colores si existen
            if color:
                color_prim = request.form.get('color_prim')
                color_sec = request.form.get('color_sec')

                # Actualiza los valores solo si hay cambios
                if color_prim and color_prim != color.Nombre_hexadecimal_principal:
                    color.Nombre_principal = color_prim
                    color.Nombre_hexadecimal_principal = color_prim

                if color_sec and color_sec != color.Nombre_hexadecimal_secundario:
                    color.Nombre_secundario = color_sec
                    color.Nombre_hexadecimal_secundario = color_sec

            # Manejo de imágenes (Logo e Ícono)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
            if 'logo' in request.files:
                logo = request.files['logo']
                if logo and allowed_file(logo.filename):
                    eliminar_imagen_anterior(empresa, 'logo')
                    logo_filename = secure_filename(logo.filename)
                    logo_path = os.path.join(upload_folder, logo_filename)
                    logo.save(logo_path)
                    nueva_imagen = Imagen(tipo_imagen='logo', filename=logo_filename, idNegocio=empresa.idNegocio)
                    db.session.add(nueva_imagen)

            if 'icono' in request.files:
                icono = request.files['icono']
                if icono and allowed_file(icono.filename):
                    eliminar_imagen_anterior(empresa, 'icono')
                    icono_filename = secure_filename(icono.filename)
                    icono_path = os.path.join(upload_folder, icono_filename)
                    icono.save(icono_path)
                    nueva_imagen = Imagen(tipo_imagen='icono', filename=icono_filename, idNegocio=empresa.idNegocio)
                    db.session.add(nueva_imagen)

            # Actualización de redes sociales y videos:
            # Se eliminan los existentes y se crean nuevos registros
            RedSocial.query.filter_by(idNegocio=empresa.idNegocio).delete()
            facebook_url = request.form.get('facebook_url')
            instagram_url = request.form.get('instagram_url')
            if facebook_url:
                db.session.add(RedSocial(nombre_red='Facebook', url_red=facebook_url, idNegocio=empresa.idNegocio))
            if instagram_url:
                db.session.add(RedSocial(nombre_red='Instagram', url_red=instagram_url, idNegocio=empresa.idNegocio))

            Video.query.filter_by(idNegocio=empresa.idNegocio).delete()
            youtube_url_1 = request.form.get('youtube_url_1')
            youtube_url_2 = request.form.get('youtube_url_2')
            if youtube_url_1:
                db.session.add(Video(tipo='YouTube', url=youtube_url_1, idNegocio=empresa.idNegocio))
            if youtube_url_2:
                db.session.add(Video(tipo='YouTube', url=youtube_url_2, idNegocio=empresa.idNegocio))

            db.session.commit()
            flash('Empresa actualizada exitosamente.', 'success')
            return redirect(url_for('informacion_empresa.listar_empresas'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar empresa: {e}", 'danger')

    return render_template('InformacionEmpresa/formulario.html', empresa=empresa, color=color, redes_sociales=redes_sociales, videos=videos)

# Ruta para eliminar una empresa (solo si pertenece al negocio del usuario)
@Info_Empresa.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_empresa(id):
    try:
        # Obtener el negocio del usuario actual
        negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
        if not negocio:
            flash('Primero debe crear un negocio', 'warning')
            return redirect(url_for('negocios.crear'))
        
        empresa = Empresa.query.get_or_404(id)
        if empresa.idNegocio != negocio.id:
            flash('No tiene permisos para eliminar esta empresa', 'danger')
            return redirect(url_for('informacion_empresa.listar_empresas'))
        
        db.session.delete(empresa)
        db.session.commit()
        flash('Empresa eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar empresa: {e}", 'danger')
        return redirect(url_for('informacion_empresa.listar_empresas'))
    
    return redirect(url_for('informacion_empresa.listar_empresas'))
