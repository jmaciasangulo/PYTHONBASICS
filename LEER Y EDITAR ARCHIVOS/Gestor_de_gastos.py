#Proyecto iniciado el 28 de marzo del 2026.
#-------------------------------IMPORTS--------------------------------------
#----------------------------PREPARATIVOS------------------------------------
#----------------------------DICCIONARIOS------------------------------------
operaciones = {
    "registrar gasto"
    "listar gasto"
    "eliminar gasto"
    "ver resumen de gastos"
}
#----------------------------FUNCIONES---------------------------------------
#----------------------------UNIDAD LOGICA-----------------------------------

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

