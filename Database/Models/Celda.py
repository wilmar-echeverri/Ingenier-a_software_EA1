from ..Connection import get_connection

class Celda:
    def __init__(self, id_celda, tipo, estado="disponible"):
        self.id_celda = id_celda
        self.tipo = tipo
        self.estado = estado

    @staticmethod
    def obtener_disponible(tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Celda FROM Celda WHERE Tipo = ? AND Estado = 'disponible' LIMIT 1", (tipo,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def ocupar_celda(id_celda):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Celda SET Estado = 'ocupada' WHERE ID_Celda = ?", (id_celda,))
        conn.commit()
        conn.close()

    @staticmethod
    def liberar_celda(id_celda):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Celda SET Estado = 'disponible' WHERE ID_Celda = ?", (id_celda,))
        conn.commit()
        conn.close()
