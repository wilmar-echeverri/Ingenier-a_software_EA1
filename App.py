import re
import streamlit as st
from Database.Models.Vehiculo import Vehiculo
from Database.Models.Registro import Registro
from Database.setup import crear_tablas
import datetime

# Crear tablas si no existen
crear_tablas()
st.title("Gestión de Parqueadero Colombia")

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
    tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"])
    usuario = st.text_input("Usuario")
    submit = st.form_submit_button("Registrar Entrada")

    # Validar en tiempo real el formato de la placa
    if placa:
        if not validar_placa(placa, tipo):
            st.error("La placa no es válida para el tipo de vehículo seleccionado.")
        else:
            st.success("La placa es válida.")

    if submit:
        if placa and usuario:
            # Validar el formato de la placa al momento de registrar la entrada
            if not validar_placa(placa, tipo):
                st.error("La placa no es válida para el tipo de vehículo seleccionado.")
            else:
                v = Vehiculo(placa, tipo, usuario)
                v.registrar_entrada()
                st.success("Entrada registrada exitosamente.")
        else:
            st.warning("Por favor, complete todos los campos.")

# Mostrar registros actuales
st.subheader("Registros de Vehículos")

# Cargar los registros y mostrarlos en la tabla
tabla_vacia = st.empty()  # Usamos un contenedor vacío para actualizar la tabla

# Función para mostrar los registros
def mostrar_tabla(registros):
    # Cabeceras de tabla
    cab1, cab2, cab3, cab4, cab5, cab6 = st.columns([2, 2, 2, 2, 2, 1])
    cab1.markdown("**Placa**")
    cab2.markdown("**Tipo**")
    cab3.markdown("**Fecha y Hora Entrada**")
    cab4.markdown("**Fecha y Hora Salida**")
    cab5.markdown("**Registrar Salida**")
    cab6.markdown("**Eliminar**")

    # Filas de registros
    for reg in registros:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

        col1.write(reg.get('placa', 'N/A'))
        col2.write(reg.get('tipo', 'N/A'))

        # Mostrar fecha y hora de entrada
        if reg.get('fecha_entrada') and reg.get('hora_entrada'):
            col3.write(f"{reg['fecha_entrada']} {reg['hora_entrada']}")
        else:
            col3.write("N/A")

        # Mostrar fecha y hora de salida
        if reg.get('fecha_salida') and reg.get('hora_salida'):
            col4.write(f"{reg['fecha_salida']} {reg['hora_salida']}")
        else:
            col4.write("🟥 En parqueadero")

        # Botón para registrar salida
        if not reg['hora_salida']:
            if col5.button("Registrar salida", key=f"salida_{reg['id']}"):
                Registro.registrar_salida(reg['id'])
                st.success(f"Salida registrada para {reg['placa']}")
        else:
            col5.write("✅")

        # Botón para eliminar
        if col6.button("🗑️", key=f"eliminar_{reg['id']}"):
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