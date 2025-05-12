from ..Connection import get_connection
from datetime import datetime

class Vehiculo:
    def __init__(self, placa, tipo, usuario):
        self.placa = placa
        self.tipo = tipo
        self.usuario = usuario

    def registrar_vehiculo(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Vehiculo (Placa, Tipo, Usuario) VALUES (?, ?, ?)",
                       (self.placa, self.tipo, self.usuario))
        conn.commit()
        conn.close()

    def registrar_entrada(self):
        self.registrar_vehiculo()
        conn = get_connection()
        cursor = conn.cursor()
        ahora = datetime.now()
        fecha = ahora.date().isoformat()
        hora = ahora.time().strftime('%H:%M:%S')
        cursor.execute("""
            INSERT INTO Registro (Placa_Vehiculo, Fecha_Entrada, Hora_Entrada)
            VALUES (?, ?, ?)
        """, (self.placa, fecha, hora))
        conn.commit()
        conn.close()
