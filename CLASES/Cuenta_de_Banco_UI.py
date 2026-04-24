from colorama import init, Fore
init(autoreset=True)


operaciones = {
    "CONSULTAR ESTADO DE CUENTA",
    "RETIRO DE EFECTIVO",
    "DEPÓSITO DE EFECTIVO",
    "TRANSFERENCIA BANCARIA",
    "VER HISTORIAL DE OPERACIONES"
}

# def validar_respuesta(respuesta, diccionario):
#     if respuesta not in diccionario:
#         return False
#     else:
#         return True
#
#

print( "\n", Fore.CYAN + "Bienvenido a PyBank", end='\n\n' )
print("Para acceder a su cuenta bancaria, ingrese su usuario y contraseña.", end='\n')
usuario = input("Escriba su usuario: ")
contrasena = input("Escriba su contraseña: ")

# print( "\n", Fore.CYAN + "Bienvenido a su Cuenta de Banco", end='\n\n' )
#
# print("Usted puede hacer las siguientes operaciones:", end='\n')
# for operacion in operaciones:
#     print("-", operacion, end='.\n')
#
# operacion_Bancaria = input("\n" "Escriba la operación que realizará: ").upper()
#
# if not validar_respuesta(operacion_Bancaria, operaciones):
#     print("Opcción invalida, vuélvalo a intentar...")
#     operacion_Bancaria = input("\n" "Escriba la operación que realizará: ").upper()
#
# else:





