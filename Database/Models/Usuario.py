from ..Connection import get_connection

class Usuario:
    def __init__(self, nombre, telefono, tipo_suscripcion):
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_suscripcion = tipo_suscripcion

    def registrar_usuario(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuario (Nombre, Telefono, Tipo_Suscripcion) VALUES (?, ?, ?)",
                       (self.nombre, self.telefono, self.tipo_suscripcion))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM Usuario")
        usuarios = [row[0] for row in cursor.fetchall()]
        conn.close()
        return usuarios

    @staticmethod
    def eliminar_usuario(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE Nombre = ?", (nombre,))
        conn.commit()
        conn.close()
