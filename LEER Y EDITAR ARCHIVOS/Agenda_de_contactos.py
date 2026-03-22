#Proyexto elaborado el 16 de marzo del 2026 y terminado y testeado el 20 de marzo del 2026

import os
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_agenda = os.path.join(ruta_script, "agenda.json")

#se importa la libreria json
import json


#se intenta abrir el archivo .json denominado "agenda"
try:
    with open(ruta_agenda, "r") as archivo:
        contactos = json.load(archivo)
#si no se encuentra, se hace el diccionario "contactos"
except FileNotFoundError:
    contactos = {}

#Aquí se trabaja con el diccionario.
#-----------------------------------------------------------------------------------------


def agregar_contacto():
    print("Escriba la información del nuevo contacto")
    nombre = input("Nombre: ")
    numero_telefonico = input("Numero Telefonico: ")
    email = input("Email: ")
    contactos[nombre] = {"Numero de telefono":numero_telefonico, "Email":email}
    print(f"Contacto de {nombre} agregado exitosamente")
    with open(ruta_agenda, "w") as archivo:
        json.dump(contactos, archivo, indent=4)


def seleccionar_contacto(funcion):
    while True:
        print("Escriba el nombre del contacto")
        nombre = input("Nombre: ")
        try:
            funcion(nombre)
            break
        except KeyError:
            print(f"El contacto de {nombre} no existe")
            continuar = input("Desea intentar otra vez? [SI/NO] ").lower()
            while continuar not in ["si", "no"]:
                print("Opcción incorrecta, intente de nuevo")
                continuar = input("Desea intentar otra vez? [SI/NO] ").lower()
            if continuar == "si":
                pass
            else:
                break
    with open(ruta_agenda, "w") as archivo:
        json.dump(contactos, archivo, indent=4)

def buscar_contacto(nombre):
    contacto = contactos[nombre]
    print("Aquí está la información de: ", nombre)
    print(contacto)

def eliminar_contacto(nombre):
    del contactos[nombre]
    print(f"El contacto de {nombre} ha sido eliminado")

def listar_contactos():
    if not contactos:
        print("No hay contactos guardados")
    else:
        print(contactos)

operaciones = {
    "agregar contacto": agregar_contacto,
    "buscar contacto por su nombre": lambda: seleccionar_contacto(buscar_contacto),
    "eliminar contacto": lambda: seleccionar_contacto(eliminar_contacto),
    "listar todos sus contactos":listar_contactos,
}


print("Agenda de contactos\n")

print("Usted puede hacer las siguientes operaciones:\n")
for acciones in operaciones:
    print(acciones)
while True:
    operacion = input("Qué desea hacer con esta agenda?: ").lower()
    while operacion not in operaciones:
        print("Operacion no valida, vuelva a intentar")
        operacion = input("Qué desea hacer con esta agenda?: ").lower()
    operaciones[operacion]()
    continuarprograma = input("Desea seguir trabajando con su agenda? [SI/NO] ").lower()
    while continuarprograma not in ["si", "no"]:
        print("Operacion no valida, vuelva a intentar")
        continuarprograma = input("Desea seguir trabajando con su agenda? [SI/NO] ").lower()
    if continuarprograma == "no":
        break

#-----------------------------------------------------------------------------------------

#Se guarda contactos en el archivo .json con 4 identaciones para que sea más legible.
with open(ruta_agenda, "w") as archivo:
    json.dump(contactos, archivo, indent=4)