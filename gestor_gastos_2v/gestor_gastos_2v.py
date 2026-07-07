import datetime
import sqlite3
import uuid
from dataclasses import dataclass


@dataclass
class Gasto:
     id_gasto: str
     nombre: str
     descripcion: str
     monto: float
     categoria: str
     fecha: str
     hora: str

conexion = sqlite3.connect('gastos.db')
basedatos = conexion.cursor()

basedatos.execute('''CREATE TABLE IF NOT EXISTS gastos (id TEXT PRIMARY KEY, nombre TEXT, descripcion TEXT, monto REAL,
categoria TEXT, fecha TEXT, hora TEXT)''')


def menu_principal():
     print("Bienvenido a su gestor de gastos PyRe")
     print()
     print("----------------------MENÚ PRINCIPAL----------------------")
     print()
     print("Usted puede hacer las siguientes operaciones:")
     print("Registrar gasto----------------------------------------[1]")
     print("Listar gastos------------------------------------------[2]")
     print()
     opcion = input("¿Qué desea hacer? R: ")

     while opcion not in ["1", "2"]:
          print("Opción invalida, vuelva a intentar...")
          opcion = input("¿Qué desea hacer? R: ")

     match opcion:
          case "1":
               print("**********************REGISTRAR GASTO*********************")
               print()
               id_gasto = str(uuid.uuid7())
               nombre = input("Escriba el nombre del gasto: ")
               descripcion = input("Añada una descripción del gasto: ")
               monto = float(input("Escriba el monto del gasto (MXN): "))
               categoria = input("Escriba el tipo de gasto que se registra: ")
               fecha, hora = registrar_fecha_hora()

               basedatos.execute("INSERT INTO gastos VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (id_gasto, nombre, descripcion, monto, categoria, fecha, hora))
               conexion.commit()


          case "2":

               basedatos.execute("SELECT * FROM gastos ORDER BY fecha DESC, hora DESC")
               gastos_lista = basedatos.fetchall()

               print("**********************LISTAR GASTOS***********************")
               print()
               print("A continuación se presentan todos los gastos, ")
               print("ordenados con base a la fecha más reciente y hora más reciente")
               print()

               for gasto in gastos_lista:

                    g = Gasto(gasto[0], gasto[1], gasto[2], gasto[3], gasto[4], gasto[5],gasto[6])

                    print(f"NOMBRE:       {g.nombre}")
                    print(f"DESCRIPCCIÓN: {g.descripcion}")
                    print(f"MONTO:        {g.monto}")
                    print(f"CATEGORIA:    {g.categoria}")
                    print(f"FECHA:        {g.fecha}")
                    print(f"HORA:         {g.hora}")
                    print()

def registrar_fecha_hora():
     momento_actual = datetime.datetime.now()
     fecha_actual = momento_actual.strftime("%Y-%m-%d")
     hora_actual = momento_actual.strftime("%I:%M %p")
     return fecha_actual, hora_actual

menu_principal()