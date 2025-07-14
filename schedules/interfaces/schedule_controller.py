from http.client import HTTPException

from flask import Blueprint, request, jsonify, current_app, flash, redirect, url_for, render_template
from flask_login import current_user
from sqlalchemy.sql import text
from app.database import db

schedule_api = Blueprint('schedule', __name__)



@schedule_api.route('/api/schedules', methods=['GET'])
def get_all_schedules():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)

    if not negocio_id:
        return jsonify({"error": "Missing negocio_id"}), 400

    schedule_query_service = current_app.config["schedule_query_service"]
    schedules = schedule_query_service.get_all_days_by_negocio_business(
        negocio_id=negocio_id,
        business_id=business_id
    )
    return jsonify({"schedules": [schedule.to_dict() for schedule in schedules]}), 200


@schedule_api.route('/schedule-with-staff', methods=['GET'])
def get_schedule_with_staff():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)
    day = request.args.get('day', type=str)

    if not (negocio_id and business_id and day):
        return jsonify({"error": "Missing one or more required params (negocio_id, business_id, day)"}), 400

    schedule_query_service = current_app.config["schedule_query_service"]

    try:
        result = schedule_query_service.get_schedule_with_staff_by_negocio_business_and_day(
            negocio_id=negocio_id,
            business_id=business_id,
            day=day
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@schedule_api.route('/schedule', methods=['GET'])
def get_schedule():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)
    day = request.args.get('day', type=str)

    if not (negocio_id and business_id and day):
        return jsonify({"error": "Missing one or more required params (negocio_id, business_id, day)"}), 400

    schedule_query_service = current_app.config["schedule_query_service"]

    try:
        result = schedule_query_service.get_by_negocio_business_and_day(
            negocio_id=negocio_id,
            business_id=business_id,
            day=day
        )
        return jsonify(result.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@schedule_api.route('/create-schedule', methods=['POST'])
def create_schedule():
    data = request.get_json()

    print("Entró a create_schedule")  # ¿Entra aquí?
    print("Headers:", dict(request.headers))
    print("Request data:", request.data)
    print("Request form:", request.form)
    print("Request json:", request.get_json())

    data = request.get_json()
    print("DATA RECIBIDA:", data)
    print("DATA RECIBIDA:", data)   # <-- YA LO TIENES

    if not data or not all(key in data for key in ['negocio_id', 'business_id', 'day', 'start_time', 'end_time', 'staff_ids']):
        print("Faltan campos")
        return jsonify({"error": "Missing required fields"}), 400

    staff_ids = data['staff_ids']
    if not (isinstance(staff_ids, list) or isinstance(staff_ids, int)):
        print("Tipo de staff_ids inválido:", type(staff_ids))
        return jsonify({"error": "'staff_ids' must be a list or an integer"}), 400

    schedule_command_service = current_app.config["schedule_command_service"]

    try:
        print("Intentando crear el horario...")
        schedule = schedule_command_service.create(
            negocio_id=data['negocio_id'],
            business_id=data['business_id'],
            day=data['day'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            staff_ids=staff_ids
        )
        print("Horario creado:", schedule)
        return jsonify(schedule.to_dict()), 201
    except Exception as e:
        print("ERROR AL CREAR:", e)
        return jsonify({"error": str(e)}), 400


@schedule_api.route('/update-schedule', methods=['PUT'])
def update_schedule():
    data = request.get_json()

    if not data or not all(key in data for key in ['id', 'negocio_id', 'business_id', 'day', 'start_time', 'end_time', 'staff_ids']):
        return jsonify({"error": "Missing required fields"}), 400

    staff_ids = data['staff_ids']

    if not (isinstance(staff_ids, list) or isinstance(staff_ids, int)):
        return jsonify({"error": "'staff_ids' must be a list or an integer"}), 400

    schedule_command_service = current_app.config["schedule_command_service"]

    try:
        schedule = schedule_command_service.update(
            schedule_id=data['id'],
            negocio_id=data['negocio_id'],
            business_id=data['business_id'],
            day=data['day'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            staff_ids=staff_ids
        )
        return jsonify(schedule.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@schedule_api.route('/schedules')
def schedules_index():
    sucursales = get_sucursales_by_negocio()
    if not sucursales:
        flash("Primero debe crear un negocio y sucursales/locales.", "danger")
        return redirect(url_for('negocios.crear'))

    schedule_query_service = current_app.config["schedule_query_service"]
    sucursales_con_horarios = []
    for sucursal in sucursales:
        horarios = schedule_query_service.get_all_days_by_negocio_business(
            negocio_id=sucursal["id_negocio"],
            business_id=sucursal["ID"]
        )
        sucursales_con_horarios.append({
            "sucursal": sucursal,
            "horarios": [h.to_dict() for h in horarios]
        })

    return render_template('slider/index_schedule.html', sucursales_con_horarios=sucursales_con_horarios)



@schedule_api.route('/schedules/agregar/<int:sucursal_id>', methods=['GET'])
def agregar_schedule(sucursal_id):
    # Busca la sucursal con el id (puedes cambiar esto por ORM si quieres)
    sucursal = next((s for s in get_sucursales_by_negocio() if s["ID"] == sucursal_id), None)
    if not sucursal:
        flash("Sucursal no encontrada.", "danger")
        return redirect(url_for('schedule.schedules_index'))

    # Trae el staff asociado al negocio para el combo múltiple
    staff_query_service = current_app.config["staff_query_service"]
    staff_list = staff_query_service.list_all_by_negocio(sucursal["id_negocio"])

    # Puedes limitar los días aquí si quieres un select fijo en el frontend
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return render_template('slider/agregar_schedule.html', sucursal=sucursal, staff_list=staff_list, dias_semana=dias_semana)



def get_sucursales_by_negocio():

    """Devuelve todas las sucursales (locales) del negocio del usuario actual"""
    negocio_actual = get_current_business()
    print('negocio_actual DESDE SESION:', negocio_actual)

    negocio_id = negocio_actual.id
    print('negocio_actual DESDE SESION:', negocio_actual)

    query = text("""
        SELECT s.ID, s.NombreSucursal, s.Distrito, s.Direccion, 
               s.Correo, s.Celular, s.Estado, s.id_negocio
        FROM sucursales s 
        WHERE s.id_negocio = :negocio_id
    """)
    sucursales = db.session.execute(query, {'negocio_id': negocio_id}).fetchall()
    sucursales = [dict(row._mapping) for row in sucursales]

    return sucursales

def get_current_business():

    """Obtiene el negocio actual del usuario"""
    if hasattr(current_user, 'negocio') and current_user.negocio:
        return current_user.negocio
    elif hasattr(current_user, 'negocios') and current_user.negocios:
        return current_user.negocios[0]
    return None


@schedule_api.errorhandler(Exception)
def schedule_errors(err):
    # Si ya es HTTPException conserva el código, si no => 500
    code = err.code if isinstance(err, HTTPException) else 500
    current_app.logger.exception(err)
    return jsonify(error=str(err)), code