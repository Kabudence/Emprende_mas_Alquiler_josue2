import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from ..models import Slider, Negocio
from ..database import db
from . import slider

# Configuración de la carpeta de carga
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Función para validar el tipo de archivo permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta principal para ver los sliders (filtrados por el negocio del usuario)
@slider.route('/', methods=['GET'])
@login_required
def index():
    try:
        # Obtener el negocio del usuario
        negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
        if not negocio:
            flash('Primero debe crear un negocio', 'warning')
            return redirect(url_for('negocios.crear'))  # Redirige a la creación de negocio

        busqueda = request.args.get('busqueda', '').strip()
        
        # Query base filtrado por id_negocio
        query = Slider.query.filter_by(id_negocio=negocio.id)
        if busqueda:
            query = query.filter(Slider.titulo.ilike(f"%{busqueda}%"))
            
        sliders = query.all()
        return render_template('slider/index.html', sliders=sliders, busqueda=busqueda)
        
    except Exception as e:
        flash(f'Error al obtener sliders: {e}', 'danger')
        return render_template('slider/index.html', sliders=[], busqueda='')

# # Ruta para agregar un nuevo slider (se asocia al negocio del usuario)
# @slider.route('/agregar', methods=['GET', 'POST'])
# @login_required
# def agregar():
    # Verificar que el usuario tenga un negocio
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'warning')
        return redirect(url_for('negocios.crear'))

    if request.method == 'POST':
        try:
            titulo = request.form.get('titulo')
            estado = request.form.get('estado')
            image_file = request.files.get('imagen')
            
            # Validación de campos obligatorios
            if not titulo or not estado:
                flash('El título y el estado son obligatorios.', 'danger')
                return redirect(url_for('slider.agregar'))
            
            filename = None
            if image_file and allowed_file(image_file.filename):
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
                # Se usa la carpeta definida en current_app o la constante UPLOAD_FOLDER
                upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
                filepath = os.path.join(upload_folder, unique_filename)
                
                # Asegurarse de que la carpeta existe
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                image_file.save(filepath)
                filename = unique_filename

            # Crear el nuevo slider, asignándole el negocio del usuario
            nuevo_slider = Slider(
                titulo=titulo,
                imagen=filename,  # Puede ser None si no se subió imagen
                estado=estado,
                id_negocio=negocio.id
            )
            
            db.session.add(nuevo_slider)
            db.session.commit()
            
            flash('Slider agregado correctamente.', 'success')
            return redirect(url_for('slider.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar el slider. Por favor, intente nuevamente.', 'danger')
            return redirect(url_for('slider.agregar'))
    
    return render_template('slider/agregar.html')

@slider.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Primero debe crear un negocio', 'warning')
        return redirect(url_for('negocios.crear'))

    if request.method == 'POST':
        try:
            print("🔧 POST recibido en /agregar")
            titulo = request.form.get('titulo')
            estado = request.form.get('estado')
            image_file = request.files.get('imagen')

            print(f"📌 Título: {titulo}")
            print(f"📌 Estado: {estado}")
            print(f"📎 Imagen recibida: {image_file.filename if image_file else 'No'}")

            if not titulo or not estado:
                flash('El título y el estado son obligatorios.', 'danger')
                return redirect(url_for('slider.agregar'))

            filename = None
            if image_file and allowed_file(image_file.filename):
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
                upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
                filepath = os.path.join(upload_folder, unique_filename)

                print(f"📂 Ruta de guardado de imagen: {filepath}")
                
                os.makedirs(upload_folder, exist_ok=True)
                image_file.save(filepath)
                filename = unique_filename
                print(f"✅ Imagen guardada como: {filename}")
            else:
                print("⚠️ No se subió imagen o tipo de archivo no permitido.")

            nuevo_slider = Slider(
                titulo=titulo,
                imagen=filename,
                estado=estado,
                id_negocio=negocio.id
            )

            db.session.add(nuevo_slider)
            db.session.commit()

            print("✅ Slider agregado con éxito.")
            flash('Slider agregado correctamente.', 'success')
            return redirect(url_for('slider.index'))

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al agregar slider: {e}")
            flash(f'Error al agregar el slider. Por favor, intente nuevamente. ({e})', 'danger')
            return redirect(url_for('slider.agregar'))

    return render_template('slider/agregar.html')





# Ruta para editar un slider existente (filtrado por negocio)
@slider.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # Verificar que el usuario tenga un negocio
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('No tiene permisos para editar sliders', 'danger')
        return redirect(url_for('slider.index'))

    # Filtrar el slider por ID y por el negocio del usuario
    slider_item = Slider.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()
    
    if request.method == 'POST':
        try:
            slider_item.titulo = request.form.get('titulo')
            slider_item.estado = request.form.get('estado')
            
            # Procesar nueva imagen si se proporciona
            imagen = request.files.get('imagen')
            if imagen and imagen.filename and allowed_file(imagen.filename):
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(imagen.filename)}"
                upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
                filepath = os.path.join(upload_folder, unique_filename)
                
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Eliminar la imagen anterior si existe
                if slider_item.imagen:
                    old_filepath = os.path.join(upload_folder, slider_item.imagen)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                imagen.save(filepath)
                slider_item.imagen = unique_filename

            db.session.commit()
            flash('Slider actualizado correctamente.', 'success')
            return redirect(url_for('slider.index'))

        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el slider. Por favor, intente nuevamente.', 'danger')

    return render_template('slider/agregar.html', slider=slider_item)

# Ruta para eliminar un slider (filtrado por negocio)
@slider.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    # Verificar que el usuario tenga un negocio
    negocio = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if not negocio:
        flash('Operación no permitida', 'danger')
        return redirect(url_for('slider.index'))

    slider_item = Slider.query.filter_by(id=id, id_negocio=negocio.id).first_or_404()

    try:
        # Eliminar la imagen asociada si existe
        if slider_item.imagen:
            upload_folder = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
            filepath = os.path.join(upload_folder, slider_item.imagen)
            if os.path.exists(filepath):
                os.remove(filepath)

        db.session.delete(slider_item)
        db.session.commit()
        flash('Slider eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el slider: {e}', 'danger')

    return redirect(url_for('slider.index'))
