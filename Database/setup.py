def crear_tablas():
    import sqlite3
    
    conn = sqlite3.connect("parqueadero.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuario (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL UNIQUE,
        Telefono TEXT NOT NULL,
        Tipo_Suscripcion TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Vehiculo (
        Placa TEXT PRIMARY KEY,
        Tipo TEXT NOT NULL,
        Usuario TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Celda (
        ID_Celda INTEGER PRIMARY KEY AUTOINCREMENT,
        Tipo TEXT NOT NULL,
        Estado TEXT NOT NULL DEFAULT 'disponible'
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Registro (
        ID_Registro INTEGER PRIMARY KEY AUTOINCREMENT,
        Placa_Vehiculo TEXT NOT NULL UNIQUE,
        Fecha_Entrada DATE NOT NULL,
        Hora_Entrada TIME NOT NULL,
        Fecha_Salida DATE,
        Hora_Salida TIME,
        ID_Celda INTEGER,
        FOREIGN KEY (Placa_Vehiculo) REFERENCES Vehiculo(Placa),
        FOREIGN KEY (ID_Celda) REFERENCES Celda(ID_Celda)
    )
    """)
    
    conn.commit()
    conn.close()
