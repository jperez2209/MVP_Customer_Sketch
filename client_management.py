# client_management.py
import streamlit as st
import pandas as pd
import datetime
from db_connector import create_connection

# Función para verificar permisos
def check_permissions(user, action, creado_por=None):
    if user['rol'] == 'gerente':
        return True
    elif user['rol'] == 'team_leader':
        if action in ['view', 'edit']:
            return True
    elif user['rol'] == 'agente_cs':
        if action in ['view_self', 'edit_self'] and creado_por == user['id']:
            return True
    return False

# Operación CREATE: Agregar un nuevo cliente
def create_cliente(user, cliente_data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO clientes (
            creado_por, name, phone, address, email, bank_account, transfer, pin, offer, taxes,
            ssn, tax_id, itin, driving_license, driving_license_expiration, passport, passport_expiration,
            birthdate, billing_card, name_card, zip, cvv, expiration_card, state, city
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user['id'], cliente_data['name'], cliente_data['phone'], cliente_data['address'],
            cliente_data['email'], cliente_data['bank_account'], cliente_data['transfer'],
            cliente_data['pin'], cliente_data['offer'], cliente_data['taxes'], cliente_data['ssn'],
            cliente_data['tax_id'], cliente_data['itin'], cliente_data['driving_license'],
            cliente_data['driving_license_expiration'], cliente_data['passport'],
            cliente_data['passport_expiration'], cliente_data['birthdate'], cliente_data['billing_card'],
            cliente_data['name_card'], cliente_data['zip'], cliente_data['cvv'],
            cliente_data['expiration_card'], cliente_data['state'], cliente_data['city']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Cliente creado exitosamente!")
    else:
        st.error("Error al conectar a la base de datos")

# Operación READ: Obtener clientes según el rol del usuario
def get_clientes(user):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if user['rol'] == 'gerente':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            """
            cursor.execute(query)
        elif user['rol'] == 'team_leader':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            WHERE u.team_leader_id = %s
            """
            cursor.execute(query, (user['id'],))
        elif user['rol'] == 'agente_cs':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            WHERE c.creado_por = %s
            """
            cursor.execute(query, (user['id'],))
        clientes = cursor.fetchall()
        cursor.close()
        connection.close()
        return clientes
    return []

# Función para buscar clientes según un criterio
def search_clientes(user, search_term):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if user['rol'] == 'gerente':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            WHERE c.name LIKE %s OR c.email LIKE %s OR c.phone LIKE %s
            """
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        elif user['rol'] == 'team_leader':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            WHERE (u.team_leader_id = %s) AND (c.name LIKE %s OR c.email LIKE %s OR c.phone LIKE %s)
            """
            cursor.execute(query, (user['id'], f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        elif user['rol'] == 'agente_cs':
            query = """
            SELECT c.*, u.username AS creado_por_nombre 
            FROM clientes c
            JOIN usuarios u ON c.creado_por = u.id
            WHERE (c.creado_por = %s) AND (c.name LIKE %s OR c.email LIKE %s OR c.phone LIKE %s)
            """
            cursor.execute(query, (user['id'], f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        clientes = cursor.fetchall()
        cursor.close()
        connection.close()
        return clientes
    return []

# Operación UPDATE: Actualizar un cliente existente
def update_cliente(user, cliente_id, cliente_data):
    if not check_permissions(user, 'edit', cliente_data['creado_por']):
        st.error("No tienes permisos para editar este cliente")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        UPDATE clientes SET
            name = %s, phone = %s, address = %s, email = %s, bank_account = %s, transfer = %s,
            pin = %s, offer = %s, taxes = %s, ssn = %s, tax_id = %s, itin = %s, driving_license = %s,
            driving_license_expiration = %s, passport = %s, passport_expiration = %s, birthdate = %s,
            billing_card = %s, name_card = %s, zip = %s, cvv = %s, expiration_card = %s, state = %s, city = %s
        WHERE id = %s
        """
        cursor.execute(query, (
            cliente_data['name'], cliente_data['phone'], cliente_data['address'],
            cliente_data['email'], cliente_data['bank_account'], cliente_data['transfer'],
            cliente_data['pin'], cliente_data['offer'], cliente_data['taxes'], cliente_data['ssn'],
            cliente_data['tax_id'], cliente_data['itin'], cliente_data['driving_license'],
            cliente_data['driving_license_expiration'], cliente_data['passport'],
            cliente_data['passport_expiration'], cliente_data['birthdate'], cliente_data['billing_card'],
            cliente_data['name_card'], cliente_data['zip'], cliente_data['cvv'],
            cliente_data['expiration_card'], cliente_data['state'], cliente_data['city'], cliente_id
        ))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Cliente actualizado exitosamente!")
    else:
        st.error("Error al conectar a la base de datos")

# Operación DELETE: Eliminar un cliente
def delete_cliente(user, cliente_id):
    if not check_permissions(user, 'edit'):
        st.error("No tienes permisos para eliminar este cliente")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(query, (cliente_id,))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Cliente eliminado exitosamente!")
    else:
        st.error("Error al conectar a la base de datos")

# Interfaz para crear un nuevo cliente
def create_cliente_ui(user):
    st.subheader("Crear Nuevo Cliente")
    cliente_data = {
        'name': st.text_input("Name"),
        'phone': st.number_input("Phone", min_value=0),
        'address': st.text_input("Address"),
        'email': st.text_input("Email"),
        'bank_account': st.number_input("Bank Account", min_value=0),
        'transfer': st.text_input("Transfer"),
        'pin': st.number_input("PIN", min_value=0),
        'offer': st.text_input("Offer"),
        'taxes': st.text_input("Taxes"),
        'ssn': st.number_input("SSN", min_value=0),
        'tax_id': st.number_input("Tax ID", min_value=0),
        'itin': st.number_input("ITIN", min_value=0),
        'driving_license': st.text_input("Driving License"),
        'driving_license_expiration': st.date_input("Driving License Expiration", min_value=datetime.date(1900, 1, 1)),
        'passport': st.text_input("Passport"),
        'passport_expiration': st.date_input("Passport Expiration", min_value=datetime.date(1900, 1, 1)),
        'birthdate': st.date_input("Birthdate", min_value=datetime.date(1900, 1, 1)),
        'billing_card': st.number_input("Billing Card", min_value=0),
        'name_card': st.text_input("Name on Card"),
        'zip': st.number_input("ZIP", min_value=0),
        'cvv': st.number_input("CVV", min_value=0),
        'expiration_card': st.date_input("Card Expiration", min_value=datetime.date(1900, 1, 1)),
        'state': st.text_input("State"),
        'city': st.text_input("City")
    }
    if st.button("Crear Cliente"):
        create_cliente(user, cliente_data)

# Interfaz para ver y editar clientes
def view_edit_clientes_ui(user):
    st.subheader("Clientes")
    
    # Añadir un campo de búsqueda
    search_term = st.text_input("Buscar cliente por nombre, email o teléfono")
    
    if search_term:
        clientes = search_clientes(user, search_term)
    else:
        clientes = get_clientes(user)
    
    if clientes:
        for cliente in clientes:
            with st.expander(f"Cliente ID: {cliente['id']}"):
                st.write(f"**Creado por:** {cliente['creado_por_nombre']}")  # Mostrar quién creó el registro
                st.write(f"**Name:** {cliente['name']}")
                st.write(f"**Phone:** {cliente['phone']}")
                st.write(f"**Email:** {cliente['email']}")
                st.write(f"**Address:** {cliente['address']}")
                st.write(f"**Bank Account:** {cliente['bank_account']}")
                st.write(f"**Transfer:** {cliente['transfer']}")
                st.write(f"**PIN:** {cliente['pin']}")
                st.write(f"**Offer:** {cliente['offer']}")
                st.write(f"**Taxes:** {cliente['taxes']}")
                st.write(f"**SSN:** {cliente['ssn']}")
                st.write(f"**Tax ID:** {cliente['tax_id']}")
                st.write(f"**ITIN:** {cliente['itin']}")
                st.write(f"**Driving License:** {cliente['driving_license']}")
                st.write(f"**Driving License Expiration:** {cliente['driving_license_expiration']}")
                st.write(f"**Passport:** {cliente['passport']}")
                st.write(f"**Passport Expiration:** {cliente['passport_expiration']}")
                st.write(f"**Birthdate:** {cliente['birthdate']}")
                st.write(f"**Billing Card:** {cliente['billing_card']}")
                st.write(f"**Name on Card:** {cliente['name_card']}")
                st.write(f"**ZIP:** {cliente['zip']}")
                st.write(f"**CVV:** {cliente['cvv']}")
                st.write(f"**Card Expiration:** {cliente['expiration_card']}")
                st.write(f"**State:** {cliente['state']}")
                st.write(f"**City:** {cliente['city']}")

                if st.button(f"Editar Cliente {cliente['id']}"):
                    st.session_state['editar_cliente'] = cliente
                if st.button(f"Eliminar Cliente {cliente['id']}"):
                    delete_cliente(user, cliente['id'])
                    st.rerun()

        if 'editar_cliente' in st.session_state:
            cliente = st.session_state['editar_cliente']
            st.subheader(f"Editar Cliente ID: {cliente['id']}")
            cliente_data = {
                'name': st.text_input("Name", value=cliente['name']),
                'phone': st.number_input("Phone", value=cliente['phone'], min_value=0),
                'address': st.text_input("Address", value=cliente['address']),
                'email': st.text_input("Email", value=cliente['email']),
                'bank_account': st.number_input("Bank Account", value=cliente['bank_account'], min_value=0),
                'transfer': st.text_input("Transfer", value=cliente['transfer']),
                'pin': st.number_input("PIN", value=cliente['pin'], min_value=0),
                'offer': st.text_input("Offer", value=cliente['offer']),
                'taxes': st.text_input("Taxes", value=cliente['taxes']),
                'ssn': st.number_input("SSN", value=cliente['ssn'], min_value=0),
                'tax_id': st.number_input("Tax ID", value=cliente['tax_id'], min_value=0),
                'itin': st.number_input("ITIN", value=cliente['itin'], min_value=0),
                'driving_license': st.text_input("Driving License", value=cliente['driving_license']),
                'driving_license_expiration': st.date_input("Driving License Expiration", value=cliente['driving_license_expiration']),
                'passport': st.text_input("Passport", value=cliente['passport']),
                'passport_expiration': st.date_input("Passport Expiration", value=cliente['passport_expiration']),
                'birthdate': st.date_input("Birthdate", value=cliente['birthdate']),
                'billing_card': st.number_input("Billing Card", value=cliente['billing_card'], min_value=0),
                'name_card': st.text_input("Name on Card", value=cliente['name_card']),
                'zip': st.number_input("ZIP", value=cliente['zip'], min_value=0),
                'cvv': st.number_input("CVV", value=cliente['cvv'], min_value=0),
                'expiration_card': st.date_input("Card Expiration", value=cliente['expiration_card']),
                'state': st.text_input("State", value=cliente['state']),
                'city': st.text_input("City", value=cliente['city']),
                'creado_por': cliente['creado_por']
            }
            if st.button("Guardar Cambios"):
                update_cliente(user, cliente['id'], cliente_data)
                del st.session_state['editar_cliente']
                st.rerun()
    else:
        st.write("No hay clientes para mostrar.")

# Función para exportar los datos de clientes a CSV
def exportar_clientes_csv(user):
    if user['rol'] != 'gerente':
        st.error("Solo el Gerente puede exportar datos.")
        return

    # Obtener todos los clientes
    clientes = get_clientes(user)
    if not clientes:
        st.warning("No hay clientes para exportar.")
        return

    # Convertir la lista de clientes en un DataFrame
    df = pd.DataFrame(clientes)

    # Convertir el DataFrame a CSV
    csv = df.to_csv(index=False).encode('utf-8')

    # Botón para descargar el archivo CSV
    st.download_button(
        label="Exportar clientes a CSV",
        data=csv,
        file_name="clientes.csv",
        mime="text/csv",
    )