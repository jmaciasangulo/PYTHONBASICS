#Proyecto iniciado el 20 de marzo del 2026
#-------------------------IMPORTS---------------------------------------------------------------------
from colorama import Fore, init
import uuid
import json
import os
#----------------------------PREPARATIVOS-------------------------------------------------------------
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_tareas = os.path.join(ruta_script, "tareas.json")
init(autoreset=True)

try:
    with open(ruta_tareas, "r") as archivo:
        lista_de_recordatorios = json.load(archivo)
except FileNotFoundError:
    lista_de_recordatorios = {
    }

#-----------------------------DICCIONARIOS------------------------------------------------------------

operaciones = {
    "agregar recordatorio": lambda: agregar_recordatorio(),
    "marcar pendiente como completado": lambda: marcar_pendientes(),
    "eliminar recordatorio": "funcionsindesarrollar" ,
    "listar recordatorios": lambda: imprimir_recordatorios(),
    "consultar informacion de como trabaja su lista": lambda: menu_informacion()
    }
menu_ayuda = {
    "agregar recordatorio": lambda: informacion_agregar_recordatorio(),
    "marcar pendiente como completado": "funcionsindesarrollar",
    "eliminar recordatorio": "funcionsindesarrollar",
    "listar recordatorios": "funcionsindesarrollar"

}
ejemplo = {}


#-----------------------------FUNCIONES---------------------------------------------------------------

def validar_fecha():
    while True:
        fecha = input("Recordar el día (SOLO FORMATO DD/MM/AAAA): ")
        try:
            if len(fecha) != 10:
                print("Fecha con cantidad de caracteres incorrecta, vuelva a intentar...")
                continue
            if int(fecha[0:2]) not in range(1,32):
                print("El día no está en el límite permitido, vuelva a intentar...")
                continue
            if int(fecha[3:5]) not in range(1,13):
                print("El mes no está en el límite permitido, vuelva a intentar...")
                continue
            if int(fecha[6:10]) not in range(1,3000):
                print("El año no está en el límite permitido, vuelva a intentar...")
                continue
            if fecha[2] != "/" or fecha[5] != "/":
                print('La separación de fechas no es valida, debe ser "/" Vuelva a intentar...')
                continue
            break
        except ValueError:
            print("Fecha digitada de manera incorrecta, solo introduzca números. Vuelva a intentar...")
            continue

    dias = int(fecha[0:2])
    meses = int(fecha[3:5])
    anos = int(fecha[6:10])

    fecha_en_dias = (dias*1) + (meses*31) + (anos*365)
    return fecha_en_dias, fecha

def validar_hora():
    while True:
        hora = input("Recordar a la hora (SOLO FORMATO HH:MM y RELOJ DE 24 HRS): ")
        try:
            if len(hora) != 5:
                print("Hora con cantidad de caracteres incorrecta, vuelva a intentar...")
                continue
            if int(hora[0:2]) not in range(0,24):
                print("La hora no está dentro del límite de 0 a 23 hrs, vuelva a intentar... ")
                continue
            if int(hora[3:5]) not in range(0,60):
                print("Los minutos no están dentro del límite de 0 a 59 min, vuelva a intentar... ")
                continue
            if hora[2] != ":":
                print('La separación entre horas y minutos no es valida, debe ser ":" Vuelva a intentar...')
                continue
            break
        except ValueError:
            print("Hora digitada de manera incorrecta, vuelva a intentar...")

    horas = int(hora[0:2])
    minutos = int(hora[3:5])

    hora_en_minutos = (horas*60) + (minutos*1)
    return hora_en_minutos, hora

def validar_prioridad():
    prioridad = input("Nivel de prioridad (SOLO BAJA, MEDIA, ALTA): ").upper()
    while prioridad not in ["BAJA", "MEDIA", "ALTA"]:
        print("Opcción incorrecta, vuelva a intentar...")
        prioridad = input("Nivel de prioridad (SOLO BAJA, MEDIA, ALTA): ").upper()
    return prioridad

def guardar_cambios():
    with open(ruta_tareas, "w") as archivo:
        json.dump(lista_de_recordatorios, archivo, indent=4)

def agregar_recordatorio():
    print("\nEscriba como lo denominará ")
    nombre = input("Denominación: ")
    descripccion = input("Agrege una breve descripción: ")
    fecha_en_dias, fecha  = validar_fecha()
    hora_en_minutos, hora = validar_hora()
    prioridad = validar_prioridad()
    estado = "pendiente"
    id = str(uuid.uuid4())

    lista_de_recordatorios[id] = {
        "nombre": nombre,
        "descripccion": descripccion,
        "fecha": (fecha,fecha_en_dias),
        "hora": (hora, hora_en_minutos),
        "prioridad": prioridad,
        "estado": estado,
        "id": id

    }
    print(f"Taread denominada como {nombre} agregada")
    guardar_cambios()

def imprimir_recordatorios():
    for i, datos in enumerate(lista_de_recordatorios.values(), 1):
        print(f"Tarea {i}:")
        for clave, valor in datos.items():
            print(f"    {clave.capitalize()}: {valor}")
        print()

def buscar_pendientes():

    while True:
        identifica_id =  input("Escribe el id del pendiente: ")
        try:
            print("\n",lista_de_recordatorios[identifica_id])
            lista_de_recordatorios[identifica_id].update({"estado": "completado"})
            print(f"\nRecordatorio denominado como: {lista_de_recordatorios[identifica_id]["nombre"]}, ha sido completado")
            guardar_cambios()
            break
        except KeyError:
            print("El id del pendiente no existe")
            repetir = input("Deseas volverlo a intentar? [SI/NO] ").lower()
            while repetir not in ["si", "no"]:
                print("Opcción invalida...")
                repetir = input("Deseas volverlo a intentar? [SI/NO] ").lower()
            if  repetir == "si":
                pass
            else:
                break

def marcar_pendiente(idtag):
    print("\n", lista_de_recordatorios[idtag])
    lista_de_recordatorios[idtag].update({"estado": "completado"})
    print(f"\nRecordatorio denominado como: {lista_de_recordatorios[idtag]["nombre"]}, ha sido completado")

def menu_informacion():
    print("\nMENÚ DE INFORMACIÓN")
    print("\nUsted puede hacer las siguientes operaciones:\n")
    for clave in menu_ayuda:
        print(clave.capitalize())
    mostar_info_de = input("Sobre que operación desea saber más?: ").lower()
    while mostar_info_de not in menu_ayuda:
        print("Opcción incorrecta, vuelva a intentar...")
        mostar_info_de = input("Sobre que operación desea saber más?: ").lower()
    menu_ayuda[mostar_info_de]()

def informacion_agregar_recordatorio():
    print("\nCon esta operación usted puede agregar un recordatorio como lo indica su nombre."
    "\n\nEn el paso #1 se le pedirá que le asigne un título o nombre a su pendiente, usted puede poner el"
    "\nnombre que le sea de su agrado, no importa si mezcla números, letras, o caracteres especiales."
    "\nEn pantalla aparecerá así:")
    nombre = input("Denominación: ")
    print("\n\nDespués, el paso #2 se le pedirá que agrege una descripcción. Aqui puede poner notas, una explicación de"
    "\nsu pendiente, etc. En este apartado tambien puede escribir lo que usted guste en la forma que"
    "\nquiera al igual que en paso #1"
    "\nEn pantalla aparecerá así:")
    descripccion = input("Agrege una breve descripción: ")
    print("\n\nAhora bien, en el paso #3 se le pedirá una fecha límite. Usted solo puede escribir la fecha de la siguiente"
    "\nmanera: DD/MM/AAAA. Por ejemplo si usted dice que la fecha límite es el 1 de julio del 2026, usted tiene que escribir"
    "\n01/07/2026. Si usted escribe de forma en que no se respete este formato, el programa no se lo permitirá y se le" 
    "\nvolverá a solicitar que ingrese la fecha. Adicional a esto, el programa traduce la fecha a días transcurridos"
    "\ndesde la fecha 01/01/0001 de manera automática, esto para comprar fechas y ordenarlas."
    "\nEn pantalla aparecerá así:")
    fecha_en_dias, fecha = validar_fecha()
    print("\n\nEn el paso #4, se le pide una hora límite o la hora a recordar. Esta información se valida de la misma forma"
    "\nque en el paso #3, respetando el formato HH:MM."
    "\nEn pantalla aparecerá así:")
    hora_en_minutos, hora = validar_hora()
    print("\n\nEn el paso #5, y el último, se solicita que agrege una prioridad o la importancia de ese recordatorio. Usted"
    "\nsolo puede digitar 3 opcciones: BAJA, MEDIA, ALTA. De no ser así, el programa le pedirá que lo intente de nuevo."
    "\nEn pantalla aparecerá algo así:")
    prioridad = validar_prioridad()
    print("\nINFORMACIÓN ADICIONAL\n")
    print("\nID DEL RECORDATORIO:\n"
    "\nAl terminar esta secuencia de pasos, a cada tarea se le asignará un ID. Esto para que si usted llega a completar"
    "\nuna tarea, y tiempo después agrega otra tarea con el mismo nombre, al momento que usted quiera seleccionar una terea en"
    "\nespecifico para editarla, marcarla o eliminarla; el programa le solicitará el nombre y el ID único perteneciente a"
    "\nesa tarea."
    "\n\nESTATUS DEL RECORDATORIO:\n"
    "\nAl igual que el ID, se le asignará de manera automatica el estatus de 'pendiente' a cada nuevo recordatorio o tarea"
    "\nque usted agrege. Cuando ese recordatorio haya cumplido su proposito, usted puede marcarla como completado y su estatus"
    "\ncambiara de 'pendiente' a 'completado' ")

    estado = "pendiente"
    id = str(uuid.uuid4())

    ejemplo[id] = {
        "nombre": nombre,
        "descripccion": descripccion,
        "fecha": (fecha, fecha_en_dias),
        "hora": (hora, hora_en_minutos),
        "prioridad": prioridad,
        "estado": estado,
        "id": id
    }
    print("\nAsí quedará guardado en la memoria\n")
    for i, datos in enumerate(ejemplo.values(), 1):
        print(f"Tarea {i}:")
        for clave, valor in datos.items():
            print(f"    {clave.capitalize()}: {valor}")
        print()
    print(Fore.YELLOW + "ACLARACIÓN: LA INFORMACIÓN ESCRITA ES SOLO PARA UN EJEMPLO, NO SE GUARDARÁ EN EL DISCO DURO.")

#-----------------------------UNIDAD LÓGICA-----------------------------------------------------------
while True:
    print("LISTA DE RECORDATORIOS")
    print("Aquí podras gestionar todos tus pendientes\n"
          "\nCon esta lista puedes hacer:\n")
    for accion in operaciones:
        print(accion)
    operacion = input("\n¿Que desea hacer con su lista?: ").lower()
    while operacion not in operaciones:
        print("\nOpcción incorrecta, vuelva a intentar.")
        operacion = input("¿Que desea hacer con su lista?: ").lower()

    operaciones[operacion]()

    continuar = input("Desea seguir trabajando con su agenda? [SI/NO]").lower()
    while continuar not in ["si", "no"]:
        print("Opcción incorrecta, vuelva a intentar...")
        continuar = input("Desea seguir trabajando con su agenda? [SI/NO] ").lower()
    if continuar == "si":
        continue
    else:
        break
        



