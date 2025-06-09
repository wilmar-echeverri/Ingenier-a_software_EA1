import sqlite3
from Database.Models.Usuario import Usuario
import datetime

class Pago:
    def __init__(self, idUsuario, monto, metodo_pago, fecha_pago=None):
        self.idUsuario = idUsuario
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def crear_tabla():
        conn = sqlite3.connect('parqueadero.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pago (
                idPago INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER,
                fechaPago TEXT,
                monto REAL,
                metodoPago TEXT,
                FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def registrar_pago(idUsuario, monto, metodo_pago):
        # Validar usuario y suscripción activa
        usuario = Usuario.obtener_por_id(idUsuario)
        if not usuario:
            raise ValueError('Usuario no existe')
        if usuario['tipo_suscripcion'] not in ['Mensual', 'Diario', 'Otro']:
            raise ValueError('Usuario no tiene suscripción activa')
        fecha_pago = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('parqueadero.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Pago (idUsuario, fechaPago, monto, metodoPago)
            VALUES (?, ?, ?, ?)
        ''', (idUsuario, fecha_pago, monto, metodo_pago))
        conn.commit()
        id_pago = cursor.lastrowid
        conn.close()
        return id_pago

    @staticmethod
    def historial_pagos(idUsuario):
        conn = sqlite3.connect('parqueadero.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT idPago, fechaPago, monto, metodoPago FROM Pago WHERE idUsuario = ? ORDER BY fechaPago DESC
        ''', (idUsuario,))
        pagos = cursor.fetchall()
        conn.close()
        return pagos

    @staticmethod
    def generar_comprobante(idPago):
        conn = sqlite3.connect('parqueadero.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Pago.idPago, Pago.fechaPago, Pago.monto, Pago.metodoPago, Usuario.idUsuario, Usuario.nombre, Usuario.tipo_suscripcion
            FROM Pago JOIN Usuario ON Pago.idUsuario = Usuario.idUsuario WHERE Pago.idPago = ?
        ''', (idPago,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        comprobante = {
            'idPago': row[0],
            'fechaPago': row[1],
            'monto': row[2],
            'metodoPago': row[3],
            'idUsuario': row[4],
            'nombreUsuario': row[5],
            'tipoSuscripcion': row[6]
        }
        return comprobante
