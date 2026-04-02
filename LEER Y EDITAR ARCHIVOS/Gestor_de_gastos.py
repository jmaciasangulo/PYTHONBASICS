#Proyecto iniciado el 28 de marzo del 2026.
#-------------------------------IMPORTS--------------------------------------
import msvcrt
import os
import json
import uuid
#----------------------------PREPARATIVOS------------------------------------
ruta_script= os.path.dirname(os.path.abspath(__file__))
ruta_tareas = os.path.join(ruta_script, "gastos.json")

try:
    with open(ruta_tareas, "r", encoding="utf-8") as archivo:
        diccionarios: dict = json.load(archivo)
    categorias_de_gastos = diccionarios["categorias_de_gastos"]
    lista_de_gastos = diccionarios["lista_de_gastos"]
except FileNotFoundError:
    lista_de_gastos = {}
    categorias_de_gastos = []
    diccionarios = {
        "lista_de_gastos":lista_de_gastos,
        "categorias_de_gastos":categorias_de_gastos
    }
#----------------------------DICCIONARIOS------------------------------------
operaciones = {
    "agregar categoria de gastos": lambda: agregar_categoria_de_gastos(),
    "eliminar categoria de gastos": lambda: "funcion no definida",
    "registrar gasto": lambda: "función no definida",
    "listar gasto": lambda: "función no definida",
    "eliminar gasto": lambda: "función no definida",
    "ver resumen de gastos": lambda: "función no definida"
}
#----------------------------FUNCIONES---------------------------------------
def guardar_cambios():
    with open(ruta_tareas, "w", encoding="utf-8") as archivo_escritura:
        json.dump(diccionarios, archivo_escritura, indent=4, ensure_ascii=False)

def agregar_categoria_de_gastos():
    while True:
        nueva_categoria = input("\nEscriba como se llamará su nueva categoría de gastos: ")
        diccionarios["categorias_de_gastos"].append(nueva_categoria)
        guardar_cambios()
        print(f'Categoría denominada como "{nueva_categoria}" agregada con éxito.')
        repetir_registro = input("¿Desea agregar otra categoría? [SI/NO]: ").lower()
        if not repetir_bucle(repetir_registro):
            break

def eliminar_categoria_de_gastos():
    while True:
        categoria = validar_categoria_eliminar()

        elimina_categoria_seleccionada(categoria)

        eliminar_otravez = input("Desea eliminar otra categoría?: [SI/NO]: ").lower()
        if not repetir_bucle(eliminar_otravez):
            break
def validar_categoria_eliminar():
    categoria = input("Escriba el nombre de la categoría: ")
    while categoria not in categorias_de_gastos:
        print("Opcción incorrecta, vuelva a intentar...")
        categoria = input("Escriba el nombre de la categoría: ")
    return categoria
def elimina_categoria_seleccionada(eliminaestacategoria):
    del diccionarios["categorias_de_gastos"][eliminaestacategoria]
    guardar_cambios()
    print(f'Categoría denominada como "{eliminaestacategoria}" ha sido eliminada.')
    
def registrar_gasto():
    while True:
        nombre = input("\nEscriba el concepto del gasto: ")
        descripcion = input("Agrege una breve descripción: ")
        monto = validar_monto()
        fecha, fecha_en_dias = validar_fecha()
        categoria = validar_categoria()
        id_gasto = str(uuid.uuid4())

        lista_de_gastos[id_gasto] = {
            "nombre": nombre,
            "descripcion": descripcion,
            "monto": monto,
            "fecha": [fecha,fecha_en_dias],
            "categoria": categoria,
            "ID del gasto": id_gasto
        }
        guardar_cambios()
        print(f'Gasto con concepto de "{nombre}" agregado.')
        repetir_registro = input("¿Desea volver a registrar otro gasto? [SI/NO]: ").lower()
        if not repetir_bucle(repetir_registro):
            break
def validar_monto():
    monto = 0
    while True:
        try:
            monto = float(input("Escriba el monto del gasto: $"))
            break
        except ValueError:
            print("Escriba el monto en números, vuelva a intentar...")
            continue
    return monto
def validar_fecha():
    while True:
        fecha = input("Escriba el fecha del gasto (SOLO FORMATO DD/MM/AAAA): ")
        try:
            if len(fecha) !=10 :
                print("La fecha debe estar digitada en 10 caracteres, vuélvalo a intentar...")
                continue
            if int(fecha[0:2]) not in range(1,32):
                print("El día no está dentro del límite establecido, vuélvalo a intentar...")
                continue
            if int(fecha[3:5]) not in range(1,13):
                print("El mes no está dentro del límite establecido, vuélvalo a intentar...")
                continue
            if int(fecha[6:10]) not in range(1,3000):
                print("El año no está dentro del límite establecido, vuélvalo a intentar...")
                continue
            if fecha[2] != "/" or fecha[5] != "/":
                print('El separador entre fechas no es correcto, use exclusivamente "/"')
                continue
            break
        except ValueError:
            print("La fecha ha sido digitada de manera incorrecta, solo use números. Vuélvalo a intentar...")
            continue
    dias = int(fecha[0:2])
    meses = int(fecha[3:5])
    anos = int(fecha[6:10])
    fecha_en_dias = dias + (meses*31) + (anos*365)
    return fecha, fecha_en_dias
def validar_categoria():
    print("Usted tiene registradas todas estas categorías.")
    for categoria in diccionarios["categorias_de_gastos"]:
        print(f"-{categoria}.")
    print("Usted solo puede registrarla a una de esas categorías.")
    categoria = input("¿A que categoría registrará este gasto?: ")
    while categoria not in diccionarios["categorias_de_gastos"]:
        print("Esta categoría no existe, vuélvalo a intentar...")
        categoria = input("¿A que categoría registrará este gasto?: ")
    return categoria

def eliminar_gasto():
    while True:
        id_gasto = validar_id_gasto()
        if not id_gasto:
            break
        elif id_gasto == True:
            continue
        else:
            pass
        eliminar_gasto_seleccionado(id_gasto)
        guardar_cambios()
        eliminar_otravez = input("¿Desea eliminar otro gasto? [SI/NO]: ").lower()
        if not repetir_bucle(eliminar_otravez):
            break
        else:
            continue
def validar_id_gasto():
    id_gasto = input("Escriba el ID del gasto: ")
    if id_gasto not in diccionarios["lista_de_gastos"]:
        print("Este ID no existe.")
        repetirbucle = input("¿Desea eliminar otro gasto? [SI/NO]: ").lower()
        return repetir_bucle(repetirbucle)
    else:
        return id_gasto
def eliminar_gasto_seleccionado(eliminaestegasto):
    for clave, valor in diccionarios["lista_de_gastos"][eliminaestegasto].items():
        print(f"{clave.capitalize()}: {valor}")
    print(f'\nGasto con concepto de {diccionarios["lista_de_gastos"][eliminaestegasto]["nombre"]} ha sido eliminado.')
    del diccionarios["lista_de_gastos"][eliminaestegasto]

def escoge_listar_gastos():
    print("Usted filtrar los gastos que se mostrarán en pantalla de la siguiente manera:")
    for filtro in listar_gastos:
        print(f"-{filtro.capitalize()}")

    filtrar = input("¿Que filtro desea aplicar?: ").lower()

    while filtrar not in listar_gastos:
        print("Opcción incorrecta, vuelva a intentar...")
        filtrar = input("¿Que filtro desea aplicar?: ").lower()

    listar_gastos[filtrar]()

def listar_por_categoria():
    print("Las categorías disponibles para consulta son:")
    for categoria in categorias_de_gastos:
        print(f"-{categoria}.")

    categoria = input("Que categoria desea ver?: ")

    haygastosencategoria = False

    while categoria not in categorias_de_gastos:
        print("Opcción invalida, vuelva a intentar...")
        categoria = input("Que categoria desea ver?: ")

    for id_gasto in diccionarios["lista_de_gastos"]:
        if diccionarios["lista_de_gastos"][id_gasto]["categoria"] == categoria:
            for clave, valor in diccionarios["lista_de_gastos"][id_gasto].items():
                print(f"{clave.capitalize()}: {valor}")
                haygastosencategoria = True

    if not haygastosencategoria:
        print("No hay gastos registrados con esta categoria.")



def repetir_bucle(respuesta):
    while respuesta not in ["si", "no"]:
        print("Opcion invalida, vuelva a intentar...")
        respuesta = input("SOLO [SI/NO]: ").lower()
    return respuesta == "si"

#----------------------------UNIDAD LOGICA-----------------------------------
if categorias_de_gastos:
    print("GESTOR DE GASTOS PERSONALES\n")
    while True:
        print("Usted puede hacer lo siguiente:\n")

        for operacion in operaciones:
            print(f"-{operacion.capitalize()}")

        operacion = input("\n¿Que desea hacer con su gestor?: ").lower()
        while operacion not in operaciones:
            print("Opcion invalida, vuelva a intentar...")
            operacion = input("¿Que desea hacer con su gestor?: ").lower()

        operaciones[operacion]()

        repetir = input("Desea volver a trabajar con su gestor? [SI/NO]: ").lower()
        if not repetir_bucle(repetir):
            break
else:
    print("¡Bienvenido a su gestor de gastos!\n")
    print("Usted puede hacer lo siguiente con su gestor:\n")
    for operacion in operaciones:
        print(f"-{operacion.capitalize()}")
    print("\nPara empezar a usar su gestor, agrege al menos 3 categorias principales para clasificar sus gastos:\n")
    categoria1 = input("Escriba el nombre de la categoría #1: ")
    categoria2 = input("Escriba el nombre de la categoría #2: ")
    categoria3 = input("Escriba el nombre de la categoría #3: ")
    categorias_de_gastos = [categoria1, categoria2, categoria3]
    diccionarios["categorias_de_gastos"] = categorias_de_gastos
    guardar_cambios()
    print("Excelente, ahora, para empezar a registrar gastos cierre el programa y vuelvalo a abrir.")
    print("PRESIONE CUALQUIER TECLA PARA SALIR")
    msvcrt.getch()
