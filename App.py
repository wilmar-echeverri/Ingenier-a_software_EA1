import re
import streamlit as st
from Database.Models.Vehiculo import Vehiculo
from Database.Models.Registro import Registro
from Database.Models.Usuario import Usuario
from Database.Models.Celda import Celda
from Database.Models.Pago import Pago
from Database.setup import crear_tablas
import datetime

# Inicializar celdas en la base de datos
def inicializar_celdas():
    import sqlite3
    conn = sqlite3.connect("parqueadero.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Celda")
    cantidad = cursor.fetchone()[0]
    if cantidad == 0:
        # Insertar celdas de carros A1-A40
        for i in range(1, 41):
            nombre = f"A{i}"
            cursor.execute("INSERT INTO Celda (Nombre, Tipo, Estado) VALUES (?, ?, ?)", (nombre, "carro", "disponible"))
        # Insertar celdas de motos M1-M60
        for i in range(1, 61):
            nombre = f"M{i}"
            cursor.execute("INSERT INTO Celda (Nombre, Tipo, Estado) VALUES (?, ?, ?)", (nombre, "moto", "disponible"))
        conn.commit()
    conn.close()

# Crear tablas si no existen
def setup_app():
    crear_tablas()
    inicializar_celdas()
setup_app()

st.title("Gestión de Parqueadero Colombia")

# --- Sección para crear y eliminar usuarios ---
st.subheader("Registrar nuevo usuario")
with st.form("form_usuario"):
    nombre_usuario = st.text_input("Nombre del usuario")
    telefono_usuario = st.text_input("Teléfono")
    tipo_suscripcion = st.selectbox("Tipo de suscripción", ["Mensual", "Diario", "Otro"])
    submit_usuario = st.form_submit_button("Registrar Usuario")
    if submit_usuario:
        if nombre_usuario and telefono_usuario and tipo_suscripcion:
            try:
                u = Usuario(nombre_usuario, telefono_usuario, tipo_suscripcion)
                u.registrar_usuario()
                st.success(f"Usuario '{nombre_usuario}' registrado exitosamente.")
            except ValueError as ve:
                st.error(str(ve))
        else:
            st.warning("Por favor, complete todos los campos del usuario.")

# Mostrar y eliminar usuarios existentes
st.subheader("Usuarios registrados")
usuarios_registrados = Usuario.obtener_todos()
if usuarios_registrados:
    for usuario in usuarios_registrados:
        col1, col2 = st.columns([4,1])
        col1.write(usuario)
        if col2.button("Eliminar", key=f"eliminar_usuario_{usuario}"):
            Usuario.eliminar_usuario(usuario)
            st.warning(f"Usuario '{usuario}' eliminado.")
            st.experimental_rerun()
else:
    st.info("No hay usuarios registrados.")

# Cargar registros desde la base de datos
def cargar_registros():
    registros = Registro.obtener_todos()
    return registros


# Validar formato de placa
def validar_placa(placa, tipo):
    # Eliminar espacios y convertir a mayúsculas
    placa = placa.replace(" ", "").upper()
    
    # Expresiones regulares para validar las placas
    if tipo == "Carro":
        # Placa para carro: tres letras seguidas de tres números (ABC 123)
        patron = r"^[A-Z]{3}\d{3}$"
    elif tipo == "Moto":
        # Placa para moto: tres letras, dos números y una letra al final (ABC 12A)
        patron = r"^[A-Z]{3}\d{2}[A-Z]{1}$"
    else:
        return False

    # Validar la placa con el patrón
    return bool(re.match(patron, placa))

# Formulario para registrar entrada
with st.form("form_entrada"):
    placa = st.text_input("Placa", key="placa_input")
    tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"], key="tipo_vehiculo")
    usuario = st.selectbox("Usuario", usuarios_registrados) if usuarios_registrados else st.text_input("Usuario")
    tipo_celda = "carro" if tipo == "Carro" else "moto"
    disponibles = Celda.obtener_disponibles(tipo_celda)
    # Filtrar solo celdas realmente disponibles (no ocupadas)
    opciones = {nombre: nombre for _, nombre in disponibles if Celda.esta_disponible(nombre)}
    celda_nombre = st.selectbox("Celda disponible", list(opciones.keys()), key="celda_input") if opciones else None
    submit = st.form_submit_button("Registrar Entrada")

    # Validar en tiempo real el formato de la placa
    if placa:
        if not validar_placa(placa, tipo):
            st.error("La placa no es válida para el tipo de vehículo seleccionado.")
        else:
            st.success("La placa es válida.")

    if submit:
        if placa and usuario and celda_nombre:
            # Validar el formato de la placa al momento de registrar la entrada
            if not validar_placa(placa, tipo):
                st.error("La placa no es válida para el tipo de vehículo seleccionado.")
            else:
                # Validar que la celda no esté ocupada por otro vehículo
                disponibles_actual = [nombre for _, nombre in Celda.obtener_disponibles(tipo_celda)]
                if celda_nombre not in disponibles_actual:
                    st.error("La celda seleccionada ya está ocupada. Actualiza la página.")
                else:
                    # Validar que la placa no esté ya en el parqueadero
                    registros = cargar_registros()
                    placas_en_parqueo = [r['placa'] for r in registros if not r['hora_salida']]
                    if placa in placas_en_parqueo:
                        st.error("Este vehículo ya está registrado en el parqueadero.")
                    else:
                        v = Vehiculo(placa, tipo, usuario)
                        v.registrar_vehiculo()
                        ahora = datetime.datetime.now()
                        fecha = ahora.date().isoformat()
                        hora = ahora.time().strftime('%H:%M:%S')
                        Registro.registrar_entrada_celda(placa, fecha, hora, celda_nombre)
                        Celda.ocupar_celda(celda_nombre)
                        st.success(f"Entrada registrada exitosamente en celda {celda_nombre}.")
        else:
            st.warning("Por favor, complete todos los campos y seleccione una celda.")

# Mostrar registros actuales
st.subheader("Registros de Vehículos")

# Cargar los registros y mostrarlos en la tabla
tabla_vacia = st.empty()  # Usamos un contenedor vacío para actualizar la tabla

# Función para mostrar los registros
def mostrar_tabla(registros):
    cab1, cab2, cab3, cab4, cab5, cab6, cab7, cab8 = st.columns([2, 2, 2, 2, 2, 2, 1, 2])
    cab1.markdown("**Placa**")
    cab2.markdown("**Tipo**")
    cab3.markdown("**Usuario**")
    cab4.markdown("**Celda**")
    cab5.markdown("**Fecha y Hora Entrada**")
    cab6.markdown("**Fecha y Hora Salida**")
    cab7.markdown("**Registrar Salida**")
    cab8.markdown("**Eliminar**")

    for reg in registros:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 2, 2, 2, 2, 2, 1, 2])
        col1.write(reg.get('placa', 'N/A'))
        col2.write(reg.get('tipo', 'N/A'))
        col3.write(reg.get('usuario', 'N/A'))
        col4.write(reg.get('celda', 'N/A'))
        if reg.get('fecha_entrada') and reg.get('hora_entrada'):
            col5.write(f"{reg['fecha_entrada']} {reg['hora_entrada']}")
        else:
            col5.write("N/A")
        if reg.get('fecha_salida') and reg.get('hora_salida'):
            col6.write(f"{reg['fecha_salida']} {reg['hora_salida']}")
        else:
            col6.write("🟥 En parqueadero")
        if not reg['hora_salida']:
            if col7.button("Registrar salida", key=f"salida_{reg['id']}"):
                Registro.registrar_salida(reg['id'])
                st.success(f"Salida registrada para {reg['placa']}")
        else:
            col7.write("✅")
        if col8.button("🗑️", key=f"eliminar_{reg['id']}"):
            Registro.eliminar_registro(reg['id'])
            st.warning(f"Registro de {reg['placa']} eliminado.")

# Mostrar la tabla inicialmente
registros = cargar_registros()  # Cargamos los registros al inicio
mostrar_tabla(registros)

# Actualizar la tabla después de cada acción
if st.session_state.get('updated', False):
    registros = cargar_registros()
    mostrar_tabla(registros)
    st.session_state.updated = False

# --- Sección de gestión de pagos ---
st.subheader("Gestión de Pagos")

# Registrar un nuevo pago
st.markdown("### Registrar pago")
usuarios_registrados = Usuario.obtener_todos()
usuario_pago = st.selectbox("Usuario", usuarios_registrados, key="usuario_pago") if usuarios_registrados else None
monto_pago = st.number_input("Monto del pago", min_value=0.0, step=0.01, format="%.2f")
metodo_pago = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia"], key="metodo_pago")
registrar_pago_btn = st.button("Registrar Pago")

if registrar_pago_btn:
    if usuario_pago and monto_pago > 0 and metodo_pago:
        id_usuario = Usuario.obtener_id_por_nombre(usuario_pago)
        try:
            id_pago = Pago.registrar_pago(id_usuario, monto_pago, metodo_pago)
            comprobante = Pago.generar_comprobante(id_pago)
            st.success(f"Pago registrado exitosamente para {usuario_pago}.")
            if comprobante:
                st.markdown("""
                <div style='border:2px solid #4CAF50; border-radius:10px; padding:20px; background-color:#fff; margin-top:20px;'>
                    <h3 style='color:#222;'>Factura de Pago</h3>
                    <b style='color:#222;'>ID Pago:</b> {idPago}<br>
                    <b style='color:#222;'>Fecha de Pago:</b> {fechaPago}<br>
                    <b style='color:#222;'>Usuario:</b> {nombreUsuario} (ID: {idUsuario})<br>
                    <b style='color:#222;'>Tipo de Suscripción:</b> {tipoSuscripcion}<br>
                    <b style='color:#222;'>Monto:</b> <span style='color:#222;'>${monto:.2f}</span><br>
                    <b style='color:#222;'>Método de Pago:</b> {metodoPago}<br>
                </div>
                """.format(
                    idPago=comprobante['idPago'],
                    fechaPago=comprobante['fechaPago'],
                    nombreUsuario=comprobante['nombreUsuario'],
                    idUsuario=comprobante['idUsuario'],
                    tipoSuscripcion=comprobante['tipoSuscripcion'],
                    monto=comprobante['monto'],
                    metodoPago=comprobante['metodoPago']
                ), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al registrar el pago: {str(e)}")
    else:
        st.warning("Por favor, complete todos los campos para registrar el pago.")

# Consultar historial de pagos
st.markdown("### Historial de pagos por usuario")
usuario_historial = st.selectbox("Usuario para historial", usuarios_registrados, key="usuario_historial") if usuarios_registrados else None
consultar_historial_btn = st.button("Consultar Historial")

if consultar_historial_btn and usuario_historial:
    id_usuario = Usuario.obtener_id_por_nombre(usuario_historial)
    pagos = Pago.historial_pagos(id_usuario)
    if pagos:
        st.write(f"Historial de pagos para {usuario_historial}:")
        for pago in pagos:
            st.write(f"ID: {pago[0]}, Fecha: {pago[1]}, Monto: ${pago[2]:.2f}, Método: {pago[3]}")
    else:
        st.info("No hay pagos registrados para este usuario.")
