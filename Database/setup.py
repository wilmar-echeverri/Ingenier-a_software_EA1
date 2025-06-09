def crear_tablas():
    import sqlite3
    
    conn = sqlite3.connect("parqueadero.db")
    cursor = conn.cursor()
    
    # Tabla Usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Telefono TEXT,
            Tipo_Suscripcion TEXT
        )
    ''')
    
    # Tabla Vehiculo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Vehiculo (
        Placa TEXT PRIMARY KEY,
        Tipo TEXT NOT NULL,
        Usuario TEXT NOT NULL
    )
    """)
    
    # Tabla Celda
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Celda (
        ID_Celda INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT UNIQUE,
        Tipo TEXT NOT NULL,
        Estado TEXT NOT NULL DEFAULT 'disponible'
    )
    """)
    
    # Tabla Registro
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
    
    # Tabla Pago
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
