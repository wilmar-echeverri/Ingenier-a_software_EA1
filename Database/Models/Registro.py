import sqlite3
from ..Connection import get_connection
import datetime

class Registro:
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Registro.ID_Registro, Vehiculo.Placa, Vehiculo.Tipo, Vehiculo.Usuario, 
                   Registro.Fecha_Entrada, Registro.Hora_Entrada, Registro.Fecha_Salida, Registro.Hora_Salida
            FROM Registro
            JOIN Vehiculo ON Registro.Placa_Vehiculo = Vehiculo.Placa
            ORDER BY Registro.Hora_Entrada DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                'id': row[0],  # ID_Registro
                'placa': row[1],
                'tipo': row[2],
                'usuario': row[3],
                'fecha_entrada': row[4],
                'hora_entrada': row[5],
                'fecha_salida': row[6],
                'hora_salida': row[7]
            }
            for row in rows
        ]


    @staticmethod
    def registrar_salida(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Actualizar la hora de salida en la tabla Registro
        cursor.execute("""
            UPDATE Registro 
            SET Fecha_Salida = ?, Hora_Salida = ? 
            WHERE ID_Registro = ?
        """, (now.split()[0], now.split()[1], id_registro))
        
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar_registro(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Eliminar el registro de la tabla Registro
        cursor.execute("DELETE FROM Registro WHERE ID_Registro = ?", (id_registro,))
        
        conn.commit()
        conn.close()