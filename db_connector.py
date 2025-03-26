# db_connector.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Hostname de InfinityFree
            user="root",  # Usuario de MySQL
            password="Alli@096734",  # Contraseña de MySQL
            database="mvp_clientes",  # Nombre de la base de datos
            auth_plugin='mysql_native_password'
            #port=3306  # Puerto de MySQL (opcional)
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None