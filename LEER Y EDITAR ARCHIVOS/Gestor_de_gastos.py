#Proyecto iniciado el 28 de marzo del 2026.
#-------------------------------IMPORTS--------------------------------------
import msvcrt
import os
import json
#----------------------------PREPARATIVOS------------------------------------
ruta_script= os.path.dirname(os.path.abspath(__file__))
ruta_tareas = os.path.join(ruta_script, "gastos.json")

try:
    with open(ruta_tareas, "r") as archivo:
        diccionarios = json.load(archivo)
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
categorias = {}
#----------------------------FUNCIONES---------------------------------------
def guardar_cambios():
    with open(ruta_tareas, "w") as archivo:
        json.dump(diccionarios, archivo, indent=4, ensure_ascii=False)
def agregar_categoria_de_gastos():
    nueva_categoria = input("\nEscriba como se llamará su nueva categoría de gastos: ")
    diccionarios["categorias_de_gastos"].append(nueva_categoria)
    guardar_cambios()
    print(f'Categoría denominada como "{nueva_categoria}" agregada con éxito.')
def registrar_gasto():
    nombre = input("\nEscriba el concepto del gasto: ")
    descripcion = input("Agrege una breve descripción: ")
    monto = validar_monto()
    fecha, fecha_en_dias = validar_fecha()
    categoria = validar_categoria()
    id_gasto = str(uuid.uuid4())

    nombre = {
        "descripcion": descripcion,
        "monto": monto,
        "fecha": [fecha,fecha_en_dias],
        "categoria": categoria,
        "ID de gasto": id_gasto
    }

    diccionarios["lista_de_gastos"].append(nombre)
    guardar_cambios()
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
        while repetir not in ["si", "no"]:
            print("Opcion invalida, vuelva a intentar...")
            repetir = input("Desea volver a trabajar con su gestor? [SI/NO]: ").lower()
        if repetir == "si":
            continue
        else:
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
