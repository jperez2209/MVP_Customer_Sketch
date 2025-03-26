# app.py
import streamlit as st
from auth import login, get_session_cookie, delete_session_cookie, generate_session_token, set_session_cookie
from user_management import create_user_ui, delete_user_ui
from client_management import view_edit_clientes_ui, create_cliente_ui, exportar_clientes_csv

st.set_page_config(page_title="Customer Sketch", page_icon="icon.ico", layout="wide")

# Interfaz de inicio de sesión
def login_ui():
    st.title("Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        user = login(username, password)
        if user:
            # Generar un token de sesión
            session_token = generate_session_token()
            # Guardar el token en una cookie
            set_session_cookie(session_token)
            # Guardar el token en st.session_state
            st.session_state['user'] = user
            st.session_state['session_token'] = session_token
            st.success(f"Bienvenido, {user['username']}!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# Interfaz principal de la aplicación
def main_app():
    user = st.session_state.get('user')
    if not user:
        st.warning("Por favor inicia sesión para continuar")
        return

    st.title(f"Panel de {user['rol'].capitalize()}")
    st.write(f"Bienvenido, {user['username']}!")

    if st.sidebar.button("Cerrar Sesión"):
        # Eliminar la cookie
        delete_session_cookie()
        # Limpiar la sesión
        st.session_state.pop('user', None)
        st.session_state.pop('session_token', None)
        st.success("Has cerrado sesión correctamente.")
        st.rerun()

    # Menú de opciones
    menu = ["Ver Clientes", "Crear Cliente"]
    if user['rol'] == 'gerente':
        menu.append("Crear Usuario")
        menu.append("Eliminar Usuario")  # Nueva opción para el Gerente
        menu.append("Exportar Clientes a CSV")

    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Ver Clientes":
        view_edit_clientes_ui(user)
    elif choice == "Crear Cliente":
        create_cliente_ui(user)
    elif choice == "Crear Usuario":
        create_user_ui(user)
    elif choice == "Eliminar Usuario":
        delete_user_ui(user)
    elif choice == "Exportar Clientes a CSV":
        exportar_clientes_csv(user)

# Punto de entrada de la aplicación
def main():
    # Verificar la cookie al cargar la página
    get_session_cookie()

    if 'user' not in st.session_state:
        login_ui()
    else:
        main_app()

if __name__ == "__main__":
    main()