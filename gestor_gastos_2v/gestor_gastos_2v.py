import sqlite3

conexion = sqlite3.connect('gastos.db')
basedatos = conexion.cursor()