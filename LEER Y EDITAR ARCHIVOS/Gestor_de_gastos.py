#Proyecto iniciado el 28 de marzo del 2026.
#-------------------------------IMPORTS--------------------------------------
import msvcrt
import os
import json
#----------------------------PREPARATIVOS------------------------------------
ruta_script= os.path.dirname(os.path.abspath(__file__))
ruta_tareas = os.path.join(ruta_script, "gastos.json")

try:
    with open(ruta_tareas, "r") as json_file:
        lista_gastos = json.load(json_file)
except FileNotFoundError:
    lista_gastos = {}
#----------------------------DICCIONARIOS------------------------------------
operaciones = {
    "agregar categoria de gastos": lambda: "funcion no definida",
    "eliminar categoria de gastos": lambda: "funcion no definida",
    "registrar gasto": lambda: "función no definida",
    "listar gasto": lambda: "función no definida",
    "eliminar gasto": lambda: "función no definida",
    "ver resumen de gastos": lambda: "función no definida"
}
#----------------------------FUNCIONES---------------------------------------
#----------------------------UNIDAD LOGICA-----------------------------------
if categorias:
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
    categoria1 = input("Escriba el nombre de la categoría #1: ").lower()
    categoria2 = input("Escriba el nombre de la categoría #2: ").lower()
    categoria3 = input("Escriba el nombre de la categoría #3: ").lower()
    print("Excelente, ahora, para empezar a registrar gastos cierre el programa y vuelvalo a abrir.")
    print("PRESIONE CUALQUIER TECLA PARA SALIR")
    msvcrt.getch()
