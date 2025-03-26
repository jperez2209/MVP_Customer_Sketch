# auth.py
import bcrypt
import uuid
import streamlit as st
from db_connector import create_connection

# Función para generar un token de sesión
def generate_session_token():
    return str(uuid.uuid4())

# Función para guardar el token en una cookie
def set_session_cookie(token):
    js = f"""
    <script>
    document.cookie = "session_token={token}; path=/; max-age=86400";  // Cookie válida por 1 día
    </script>
    """
    st.write(js, unsafe_allow_html=True)

# Función para eliminar la cookie al cerrar sesión
def delete_session_cookie():
    js = """
    <script>
    document.cookie = "session_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    </script>
    """
    st.write(js, unsafe_allow_html=True)

# Función para obtener el token de la cookie
def get_session_cookie():
    js = """
    <script>
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    const token = getCookie('session_token');
    window.parent.postMessage({type: 'session_token', token: token}, '*');
    </script>
    """
    st.write(js, unsafe_allow_html=True)

# Función para verificar la contraseña hasheada
def check_password(hashed_password, input_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Función para autenticar al usuario
def login(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, username, password_hash, rol, team_leader_id FROM usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password(user['password_hash'], password):
            return user
    return None