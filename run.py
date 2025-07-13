from flask import Flask

from app import create_app
from flask_mysqldb import MySQL

from appointment.interfaces.appointment_controller import appointment_api
from schedules.interfaces.schedule_controller import schedule_api
from staff.interfaces.staff_controller import staff_api

app = create_app()

app.config['MYSQL_HOST'] = '74.222.7.89'  # O la dirección IP de tu servidor de base de datos
app.config['MYSQL_USER'] = 'root'       # El usuario de tu base de datos
app.config['MYSQL_PASSWORD'] = ''       # La contraseña de tu base de datos
app.config['MYSQL_DB'] = 'emprende_mas_alquiler'  # El nombre de tu base de datos
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

