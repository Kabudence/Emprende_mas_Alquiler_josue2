from datetime import date
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
    business_id = request.args.get('business_id', default=None, type=int)
    day = request.args.get('day', default=None, type=str)

    if not negocio_id:
        return jsonify({"error": "Missing required param: negocio_id"}), 400

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
    staff_query_service = current_app.config["staff_query_service"]
    sucursales_con_horarios = []

    for sucursal in sucursales:
        horarios = schedule_query_service.get_all_days_by_negocio_business(
            negocio_id=sucursal["id_negocio"],
            business_id=sucursal["ID"]
        )
        horarios_out = []
        for h in horarios:
            h_dict = h.to_dict()
            staff_ids = schedule_query_service.get_staff_by_schedule_query(h.id)
            # Si get_by_id devuelve None si no existe, filtra con if s
            staff_list = [
                staff_query_service.get_by_id(sid).to_dict()
                for sid in staff_ids
                if staff_query_service.get_by_id(sid)
            ]
            h_dict['staff'] = staff_list
            horarios_out.append(h_dict)

        sucursales_con_horarios.append({
            "sucursal": sucursal,
            "horarios": horarios_out
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


# ---- EDITAR HORARIO (GET y POST) ----
@schedule_api.route('/schedules/editar/<int:horario_id>', methods=['GET', 'POST'])
def editar_horario(horario_id):
    schedule_query_service = current_app.config["schedule_query_service"]
    staff_query_service = current_app.config["staff_query_service"]

    horario = schedule_query_service.get_by_id(horario_id)
    if not horario:
        flash("Horario no encontrado.", "danger")
        return redirect(url_for('schedule.schedules_index'))

    sucursal = next((s for s in get_sucursales_by_negocio() if s["ID"] == horario.business_id), None)
    if not sucursal:
        flash("Sucursal no encontrada.", "danger")
        return redirect(url_for('schedule.schedules_index'))

    staff_list = staff_query_service.list_all_by_negocio(sucursal["id_negocio"])
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    if request.method == 'POST':
        day        = request.form.get('day')
        start_time = request.form.get('start_time')
        end_time   = request.form.get('end_time')
        staff_ids  = request.form.getlist('staff_ids')
        staff_ids  = [int(sid) for sid in staff_ids]

        schedule_command_service = current_app.config["schedule_command_service"]

        try:
            updated = schedule_command_service.update(
                schedule_id=horario.id,
                negocio_id=horario.negocio_id,
                business_id=horario.business_id,
                day=day,
                start_time=start_time,
                end_time=end_time,
                staff_ids=staff_ids
            )
            flash("Horario actualizado correctamente.", "success")
            return redirect(url_for('schedule.schedules_index'))
        except Exception as e:
            flash(f"Error al actualizar horario: {e}", "danger")

    # staff_ids seleccionados para el template (debe ser lista de ints)
    horario_dict = horario.to_dict()
    horario_dict['staff_ids'] = [s['id'] for s in horario_dict.get('staff', [])]
    return render_template('slider/editar_schedule.html',
                           horario=horario_dict,
                           sucursal=sucursal,
                           staff_list=staff_list,
                           dias_semana=dias_semana)

# ---- ELIMINAR HORARIO (POST) ----
@schedule_api.route('/schedules/eliminar/<int:horario_id>', methods=['POST'])
def eliminar_horario(horario_id):
    schedule_command_service = current_app.config["schedule_command_service"]
    try:
        schedule_command_service.delete_schedule(horario_id)
        flash("Horario eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar horario: {e}", "danger")
    return redirect(url_for('schedule.schedules_index'))



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

# --------------------------- CALENDARIO ---------------------------
@schedule_api.route("/calendar")
def calendar_view():
    negocio_id = request.args.get("negocio_id", type=int)
    if not negocio_id: return "Falta negocio_id", 400

    today  = date.today()
    year   = int(request.args.get("year",  today.year))
    month  = int(request.args.get("month", today.month))

    appt_qs = current_app.config["appointment_query_service"]
    # ► citas del mes
    appts   = appt_qs.list_by_month_and_negocio(year=year, month=month, negocio_id=negocio_id)

    print ("Total de citas en el mes:", len(appts))
    print ("Citas:", [a.to_dict() for a in appts])
    days_with_appointments = {a.start_time.day for a in appts}   # {1, 7, 15, …}
    print("Días con citas:", days_with_appointments)
    return render_template(
        "slider/calendar.html",
        year=year, month=month,
        negocio_id=negocio_id,
        days_with_appointments=list(days_with_appointments),   # → Jinja2
    )


@schedule_api.route("/calendar/details")
def calendar_details():
    negocio_id = request.args.get("negocio_id", type=int)
    year  = int(request.args["year"]);  month = int(request.args["month"]);  day = int(request.args["day"])

    appt_qs  = current_app.config["appointment_query_service"]
    iso_date = f"{year:04d}-{month:02d}-{day:02d}"
    appts    = appt_qs.list_by_day_and_negocio(iso_date, negocio_id)

    # añade (opcional) nombre de staff si tu entidad ya lo trae
    for a in appts:
        # a.staff   → relación lazy?
        a.staff_names = [getattr(a, "staff").name] if getattr(a, "staff", None) else []

    return jsonify({"appointments": [a.to_dict() | {"staff_names": a.staff_names} for a in appts]})
