from flask import Blueprint, request, jsonify, current_app, render_template, abort, redirect, url_for, session
from flask_login import current_user

staff_api = Blueprint('staff', __name__)

# -------- API JSON --------
def get_current_business():
    """Obtiene el negocio actual del usuario"""
    if hasattr(current_user, 'negocio') and current_user.negocio:
        return current_user.negocio
    elif hasattr(current_user, 'negocios') and current_user.negocios:
        return current_user.negocios[0]
    return None



@staff_api.route('/create-staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff = staff_command_service.create(
            speciality=data['speciality'],
            name=data['name'],
            negocio_id=data['negocio_id'],
            max_capacity=data['max_capacity'],
            dni=data['dni']
        )
        return jsonify(staff_to_json(staff)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_api.route('/update-staff', methods=['PUT'])
def update_staff():
    data = request.get_json()
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff = staff_command_service.update(
            id=data['id'],
            speciality=data['speciality'],
            name=data['name'],
            negocio_id=data['negocio_id'],
            max_capacity=data['max_capacity'],
            dni=data['dni']
        )
        return jsonify(staff_to_json(staff)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_api.route('/get-staff', methods=['GET'])
def get_staff():
    staff_id = request.args.get('id', type=int)
    if not staff_id:
        return jsonify({"error": "Missing staff ID"}), 400
    staff_query_service = current_app.config["staff_query_service"]
    staff = staff_query_service.get_by_id(staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff_to_json(staff)), 200

@staff_api.route('/list-staff', methods=['GET'])
def get_staff_list():
    staff_query_service = current_app.config["staff_query_service"]
    staff_list = staff_query_service.list_all()
    return jsonify([staff_to_json(staff) for staff in staff_list]), 200

@staff_api.route('/get-staff-by-dni', methods=['GET'])
def get_staff_by_dni():
    staff_dni = request.args.get('dni', type=str)
    if not staff_dni:
        return jsonify({"error": "Missing staff DNI"}), 400
    staff_query_service = current_app.config["staff_query_service"]
    staff = staff_query_service.get_by_dni(staff_dni)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff_to_json(staff)), 200

@staff_api.route('/delete-staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff_command_service.delete(staff_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def staff_to_json(staff):
    return {
        "id": staff.id,
        "speciality": staff.speciality,
        "name": staff.name,
        "negocio_id": staff.negocio_id,
        "max_capacity": staff.max_capacity,
        "dni": staff.dni
    }

# -------- HTML para administración --------

@staff_api.route('/staff')
def index():
    staff_query_service = current_app.config["staff_query_service"]
    staff_list = staff_query_service.list_all()
    # AJUSTA esta ruta según donde esté tu template!
    return render_template('slider/index_staff.html', staffs=staff_list)
@staff_api.route('/staff/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        data = request.form
        staff_command_service = current_app.config["staff_command_service"]
        negocio_actual = get_current_business()

        print('negocio_actual DESDE SESION:', negocio_actual)

        if not negocio_actual or not hasattr(negocio_actual, 'id'):
            # Si por algún motivo no existe, muestra error
            return render_template('slider/crear_staff.html', error="No se pudo determinar el negocio actual.")

        negocio_id = negocio_actual.id  # <-- Aquí está el id correcto

        try:
            staff_command_service.create(
                speciality=data['speciality'],
                name=data['name'],
                negocio_id=negocio_id,
                max_capacity=data['max_capacity'],
                dni=data['dni']
            )
            return redirect(url_for('staff.index'))
        except Exception as e:
            return render_template('slider/crear_staff.html', error=str(e))
    # GET
    return render_template('slider/crear_staff.html')

@staff_api.route('/staff/editar/<int:staff_id>', methods=['GET', 'POST'])
def editar(staff_id):
    staff_query_service = current_app.config["staff_query_service"]
    staff_command_service = current_app.config["staff_command_service"]
    staff = staff_query_service.get_by_id(staff_id)
    if not staff:
        abort(404)
    error = None
    if request.method == 'POST':
        data = request.form
        try:
            staff_command_service.update(
                id=staff_id,
                speciality=data['speciality'],
                name=data['name'],
                negocio_id=staff.negocio_id,
                max_capacity=data['max_capacity'],
                dni=data['dni']
            )
            return redirect(url_for('staff.index'))
        except Exception as e:
            error = str(e)
            # Vuelve a cargar los datos editados para que el usuario no los pierda
            staff.name = data['name']
            staff.speciality = data['speciality']
            staff.max_capacity = data['max_capacity']
            staff.dni = data['dni']
    return render_template('slider/editar_staff.html', staff=staff, error=error)


@staff_api.route('/staff/eliminar/<int:staff_id>', methods=['POST'])
def eliminar(staff_id):
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff_command_service.delete(staff_id)
        print("Eliminando staff con id:", staff_id)

        return redirect(url_for('staff.index'))
    except Exception as e:
        # ... renderiza el index con error si quieres
        print("Eliminando staff con id:", staff_id)

        staff_query_service = current_app.config["staff_query_service"]
        staff_list = staff_query_service.list_all()
        return render_template('slider/index_staff.html', staffs=staff_list, error=str(e))
