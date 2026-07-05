import sqlite3

conexion = sqlite3.connect('gastos.db')
basedatos = conexion.cursor()

basedatos.execute('''CREATE TABLE IF NOT EXISTS gastos (id TEXT PRIMARY KEY, nombre TEXT, descripccion TEXT, monto REAL,
categoria TEXT, fecha TEXT, hora TEXT)''')