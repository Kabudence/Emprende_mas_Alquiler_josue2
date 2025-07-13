from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import db, Local, Usuario 
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

locales_bp = Blueprint('locales', __name__, template_folder='templates')

# Formulario con WTForms
class LocalForm(FlaskForm):
    latitud = StringField('Latitud', [validators.DataRequired(), validators.Length(max=50)])
    longitud = StringField('Longitud', [validators.DataRequired(), validators.Length(max=50)])
    numero = StringField('Número', [validators.DataRequired(), validators.Length(max=20)])
    direccion = StringField('Dirección', [validators.DataRequired(), validators.Length(max=255)])
    usuario_id = SelectField('Usuario', coerce=int, validators=[validators.DataRequired()])

@locales_bp.route('/')
def listar_locales():
    locales = Local.query.all()
    return render_template('listar.html', locales=locales)

@locales_bp.route('/crear', methods=['GET', 'POST'])
def crear_local():
    form = LocalForm()
    # Aquí deberías cargar las opciones para usuario_id desde la base de datos
    form.usuario_id.choices = [(u.id, u.nombre) for u in Usuario.query.all()]
    
    if form.validate_on_submit():
        try:
            local = Local(
                latitud=form.latitud.data,
                longitud=form.longitud.data,
                numero=form.numero.data,
                direccion=form.direccion.data,
                usuario_id=form.usuario_id.data
            )
            db.session.add(local)
            db.session.commit()
            flash('Local creado exitosamente', 'success')
            return redirect(url_for('locales.listar_locales'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear local: {str(e)}', 'danger')
    
    return render_template('formulario.html', form=form, titulo='Crear Local')

@locales_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_local(id):
    local = Local.query.get_or_404(id)
    form = LocalForm(obj=local)
    form.usuario_id.choices = [(u.id, u.nombre) for u in Usuario.query.all()]
    
    if form.validate_on_submit():
        try:
            form.populate_obj(local)
            db.session.commit()
            flash('Local actualizado exitosamente', 'success')
            return redirect(url_for('locales.listar_locales'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar local: {str(e)}', 'danger')
    
    return render_template('formulario.html', form=form, titulo='Editar Local')

@locales_bp.route('/eliminar/<int:id>')
def eliminar_local(id):
    local = Local.query.get_or_404(id)
    try:
        db.session.delete(local)
        db.session.commit()
        flash('Local eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar local: {str(e)}', 'danger')
    
    return redirect(url_for('locales.listar_locales'))