from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone, timedelta

appointment_api = Blueprint('appointment_api', __name__)

_WEEKDAYS_ES = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]

@appointment_api.route('/appointments', methods=['POST'])
def create_appointment():
    logger = current_app.logger      # usa el logger propio de Flask

    data = request.get_json(silent=True) or {}
    logger.info("POST /appointments - payload: %s", data)

    try:
        start_time  = datetime.fromisoformat(data['start_time'])
        end_time    = datetime.fromisoformat(data['end_time'])
        client_id   = data['client_id']
        negocio_id  = data['negocio_id']
        staff_id    = data['staff_id']
        business_id = data['business_id']
        service_id  = data['service_id']

        logger.debug(
            "Parsed params → start=%s end=%s client=%s negocio=%s staff=%s "
            "business=%s service=%s",
            start_time, end_time, client_id, negocio_id, staff_id, business_id, service_id
        )

        appointment_command_service = current_app.config["appointment_command_service"]
        appointment = appointment_command_service.create(
            start_time=start_time,
            end_time=end_time,
            client_id=client_id,
            negocio_id=negocio_id,
            staff_id=staff_id,
            business_id=business_id,
            service_id=service_id,
        )

        logger.info("Appointment created: id=%s", appointment.id)
        return jsonify(appointment.to_dict()), 201

    except Exception as e:
        logger.exception("Error creating appointment")   # stack-trace incluido
        return jsonify({'error': str(e)}), 400

# Obtener una cita por ID
@appointment_api.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment_query_service = current_app.config["appointment_query_service"]
    appointment = appointment_query_service.get_by_id(appointment_id)
    if appointment:
        return jsonify(appointment.__dict__), 200
    else:
        return jsonify({'error': 'Appointment not found'}), 404

# Listar citas por día y negocio o staff
@appointment_api.route('/appointments-by-day', methods=['GET'])
def list_appointments():
    day = request.args.get('day')
    negocio_id = request.args.get('negocio_id', type=int)
    staff_id = request.args.get('staff_id', type=int)

    appointment_query_service = current_app.config["appointment_query_service"]

    if staff_id and day:
        appointments = appointment_query_service.list_by_staff_and_day(staff_id, day)
    elif day and negocio_id:
        appointments = appointment_query_service.list_by_day_and_negocio(day, negocio_id)
    else:
        return jsonify({'error': 'Missing required query params'}), 400

    result = [a.__dict__ for a in appointments]
    return jsonify(result), 200

# Cancelar cita
@appointment_api.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment_command_service = current_app.config["appointment_command_service"]
    try:
        appointment = appointment_command_service.cancel(appointment_id)
        return jsonify(appointment.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Actualizar estado
@appointment_api.route('/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    appointment_command_service = current_app.config["appointment_command_service"]
    data = request.get_json()
    try:
        new_status = data['status']
        appointment = appointment_command_service.update_status(appointment_id, new_status)
        return jsonify(appointment.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Completar cita (poner en CONFIRMED)
@appointment_api.route('/appointments/<int:appointment_id>/complete', methods=['POST'])
def complete_appointment(appointment_id):
    appointment_command_service = current_app.config["appointment_command_service"]
    try:
        # Cambia el estado directamente a CONFIRMED
        appointment_command_service.update_status(appointment_id, "CONFIRMED")
        return jsonify(True), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointment_api.route('/appointments/last-pending-by-client/<int:client_id>', methods=['GET'])
def last_pending_by_client(client_id):
    appointment_query_service = current_app.config["appointment_query_service"]
    appointment = appointment_query_service.get_last_pending_by_client(client_id)
    if appointment:
        return jsonify(appointment.to_dict()), 200
    else:
        return jsonify({'error': 'No pending appointment found'}), 404


@appointment_api.route('/available-slots', methods=['GET'])
def get_available_slots():
    negocio_id  = request.args.get('negocio_id',  type=int)
    business_id = request.args.get('business_id', type=int)
    day         = request.args.get('day')                     # '2025-07-22'
    duration    = request.args.get('service_duration_min', type=int, default=60)

    if not (negocio_id and day):
        return jsonify({"error": "Missing required params"}), 400

    try:
        weekday_name = weekday_es_peru(day)
        print(f"[AVAIL] Día solicitado: {day} → {weekday_name}")
    except ValueError:
        return jsonify({"error": "Invalid day format, expected YYYY-MM-DD"}), 400

    availability_query_service = current_app.config["availability_query_service"]
    slots = availability_query_service.get_available_slots(
        negocio_id, business_id, weekday_name, duration
    )

    # Devuelve también el nombre del día para que el front pueda mostrarlo
    return jsonify({
        "weekday": weekday_name,
        "available_slots": slots
    }), 200

def zone_pe():
    """
    Devuelve la zona horaria de Perú, usando tzdata si está
    disponible y UTC-5 fijo si no.
    """
    try:
        return ZoneInfo("America/Lima")
    except ZoneInfoNotFoundError:
        return timezone(timedelta(hours=-5))  # Respaldo

def weekday_es_peru(date_str: str) -> str:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves",
            "Viernes", "Sábado", "Domingo"]
    dt_pe = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=zone_pe())
    return dias[dt_pe.weekday()]