import sqlite3
import uuid

conexion = sqlite3.connect('gastos.db')
basedatos = conexion.cursor()

basedatos.execute('''CREATE TABLE IF NOT EXISTS gastos (id TEXT PRIMARY KEY, nombre TEXT, descripccion TEXT, monto REAL,
categoria TEXT, fecha TEXT, hora TEXT)''')

def menu_principal():
     print("Bienvenido a su gestor de gastos PyRe")
     print()
     print("----------------------MENÚ PRINCIPAL----------------------")
     print()
     print("Usted puede hacer las siguientes operaciones:")
     print("Registrar gasto----------------------------------------[1]")
     print("Eliminar gasto-----------------------------------------[2]")
     print()
     opcion = input("¿Qué desea hacer? R: ")

     while opcion not in ["1", "2"]:
          print("Opción invalida, vuelva a intentar...")
          opcion = input("¿Qué desea hacer? R: ")

     match opcion:
          case "1":
               print("**********************REGISTRAR GASTO*********************")
               print()
               nombre = input("Escriba el nombre del gasto: ")
               descripcion = input("Añada una descripción del gasto: ")
               monto = input("Escriba el monto del gasto (MXN): ")
               categoria = input("Escriba el tipo de gasto que se registra: ")
               id_gasto = str(uuid.uuid7())
               

               basedatos.execute("INSERT INTO gastos VALUES (id, nombre, descripcion, monto, categoria, fecha, hora)",
                                  (id_gasto, nombre, descripcion, monto, categoria))