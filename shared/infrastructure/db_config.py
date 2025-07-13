# archivo: shared/infrastructure/db_config_peewee.py
from config import Config   # <-- ya existe; NO lo modificamos

DB_CONFIG = {
    'database': Config.MYSQL_DB,
    'user'    : Config.MYSQL_USER,
    # Usa la contraseña sin codificar; la versión “pwd” es solo
    # para la URI de SQLAlchemy.
    'password': Config.MYSQL_PASSWORD,
    'host'    : Config.MYSQL_HOST,
    'port'    : Config.MYSQL_PORT,
}
