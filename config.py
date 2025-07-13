from urllib.parse import quote_plus

class Config:
    SECRET_KEY = 'ozxcXkasdnM'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'gitano200J@@J@@'
    MYSQL_HOST     = '127.0.0.1'
    MYSQL_DB       = 'emprende_mas_alquiler'
    MYSQL_PORT     = 3306
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'

    # Codifica la contraseña para evitar problemas con caracteres especiales
    pwd = quote_plus(MYSQL_PASSWORD)
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{pwd}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
