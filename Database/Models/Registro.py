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
                   Registro.Fecha_Entrada, Registro.Hora_Entrada, Registro.Fecha_Salida, Registro.Hora_Salida, Registro.ID_Celda
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
                'hora_salida': row[7],
                'id_celda': row[8]
            }
            for row in rows
        ]

    @staticmethod
    def registrar_entrada_celda(placa, fecha, hora, nombre_celda):
        conn = get_connection()
        cursor = conn.cursor()
        # Buscar el ID_Celda por el nombre
        cursor.execute("SELECT ID_Celda FROM Celda WHERE Nombre = ?", (nombre_celda,))
        row = cursor.fetchone()
        id_celda = row[0] if row else None
        cursor.execute("""
            INSERT INTO Registro (Placa_Vehiculo, Fecha_Entrada, Hora_Entrada, ID_Celda)
            VALUES (?, ?, ?, ?)
        """, (placa, fecha, hora, id_celda))
        conn.commit()
        conn.close()

    @staticmethod
    def registrar_salida(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Obtener la celda asignada
        cursor.execute("SELECT Celda.Nombre FROM Registro JOIN Celda ON Registro.ID_Celda = Celda.ID_Celda WHERE Registro.ID_Registro = ?", (id_registro,))
        row = cursor.fetchone()
        nombre_celda = row[0] if row else None
        # Actualizar la hora de salida en la tabla Registro
        cursor.execute("""
            UPDATE Registro 
            SET Fecha_Salida = ?, Hora_Salida = ? 
            WHERE ID_Registro = ?
        """, (now.split()[0], now.split()[1], id_registro))
        conn.commit()
        conn.close()
        # Liberar la celda si corresponde
        if nombre_celda:
            from Database.Models.Celda import Celda
            Celda.liberar_celda(nombre_celda)

    @staticmethod
    def eliminar_registro(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        # Eliminar el registro de la tabla Registro
        cursor.execute("DELETE FROM Registro WHERE ID_Registro = ?", (id_registro,))
        conn.commit()
        conn.close()
