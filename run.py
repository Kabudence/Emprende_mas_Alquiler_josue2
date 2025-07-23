
from app import create_app
from flask_mysqldb import MySQL


app = create_app()

app.config['MYSQL_HOST'] = '74.222.7.89'  # O la dirección IP de tu servidor de base de datos
app.config['MYSQL_USER'] = 'root'       # El usuario de tu base de datos
app.config['MYSQL_PASSWORD'] = ''       # La contraseña de tu base de datos
app.config['MYSQL_DB'] = 'emprende_mas_alquiler'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

