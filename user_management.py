# user_management.py
import streamlit as st
import bcrypt
from db_connector import create_connection

# Función para crear un nuevo usuario en la base de datos
def create_user(creado_por, username, password, rol, team_leader_id=None):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO usuarios (username, password_hash, rol, team_leader_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password, rol, team_leader_id))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Usuario creado exitosamente!")
    else:
        st.error("Error al conectar a la base de datos")

# Función para eliminar un usuario (solo accesible para el Gerente)
def delete_user(user, user_id):
    if user['rol'] != 'gerente':
        st.error("Solo el Gerente puede eliminar usuarios.")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Usuario eliminado exitosamente!")
    else:
        st.error("Error al conectar a la base de datos")

# Interfaz para eliminar un usuario (solo accesible para el Gerente)
def delete_user_ui(user):
    if user['rol'] != 'gerente':
        st.error("Solo el Gerente puede eliminar usuarios.")
        return

    st.subheader("Eliminar Usuario")
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, username FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        connection.close()

        if usuarios:
            usuario_options = {u['username']: u['id'] for u in usuarios}
            selected_usuario = st.selectbox("Seleccionar Usuario a Eliminar", list(usuario_options.keys()))
            user_id = usuario_options[selected_usuario]

            if st.button("Eliminar Usuario"):
                delete_user(user, user_id)
                st.rerun()
        else:
            st.error("No hay usuarios para eliminar.")

# Interfaz para crear un nuevo usuario (solo accesible para el Gerente)
def create_user_ui(user):
    if user['rol'] != 'gerente':
        st.error("Solo el Gerente puede crear usuarios.")
        return

    st.subheader("Crear Nuevo Usuario")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["agente_cs", "team_leader", "gerente"])
    team_leader_id = None

    if rol == "agente_cs":
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username FROM usuarios WHERE rol = 'team_leader'")
            team_leaders = cursor.fetchall()
            cursor.close()
            connection.close()

            if team_leaders:
                team_leader_options = {tl['username']: tl['id'] for tl in team_leaders}
                selected_team_leader = st.selectbox("Seleccionar Team Leader", list(team_leader_options.keys()))
                team_leader_id = team_leader_options[selected_team_leader]
            else:
                st.error("No hay Team Leaders disponibles. Primero crea un Team Leader.")
                return

    if st.button("Crear Usuario"):
        if username and password:
            create_user(user['id'], username, password, rol, team_leader_id)
        else:
            st.error("Por favor completa todos los campos.")