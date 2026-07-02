import copy
import datetime
import json
import os
import sys
import uuid


ruta_script = os.path.dirname(os.path.abspath(__file__))

ruta_json = os.path.join(ruta_script, "cuentas.json")


class Operacion:

    def __init__(self, fecha, hora, operacion, monto):
        self.fecha = fecha
        self.hora = hora
        self.operacion = operacion
        self.monto = monto

    def __str__(self):
        if self.operacion == "Consulta de balance" or self.operacion == "Consulta de historial de operaciones de cuenta":
            return f"{self.fecha}-{self.hora}-{self.operacion}"
        else:
            return f"{self.fecha}-{self.hora}-{self.operacion}-{self.monto}"

class CuentaBancaria:
    def __init__(self, titular, balance, nip):
        self.id_cuenta = f"{uuid.uuid4()}"
        self.titular = titular
        self.balance = balance
        self.nip = nip
        self.historial = []

    def depositar(self, monto):
        self.balance += monto
        operacion = self._crear_operacion( "Deposito", monto)
        self._anexar_operacion(operacion)

    def retirar(self, monto):
        if monto > self.balance:
            operacion = self._crear_operacion("Retiro - FALLIDO", monto)
            self._anexar_operacion(operacion)
            return False
        else:
            self.balance -= monto
            operacion = self._crear_operacion("Retiro", monto)
            self._anexar_operacion(operacion)
            return True

    def ver_balance(self):
        print(f"Estimado {self.titular},")
        print(f"Su balance actual es de: ${self.balance} MXN")

        operacion = self._crear_operacion("Consulta de balance", None)
        self._anexar_operacion(operacion)

    def ver_historial(self):
        operacion = self._crear_operacion("Consulta de historial de operaciones de cuenta", None)
        self._anexar_operacion(operacion)

        for operacion in self.historial:
            if operacion.monto is None:
                print()
                print(f"OPERACIÓN REALIZADA:        {operacion.operacion}")
                print(f"FECHA EN LA QUE SE REALIZÓ: {operacion.fecha}")
                print(f"HORA EN LA QUE SE REALIZÓ:  {operacion.hora}")
            else:
                print()
                print(f"OPERACIÓN REALIZADA:        {operacion.operacion}")
                print(f"MONTO DE LA OPERACIÓN:      ${operacion.monto}")
                print(f"FECHA EN LA QUE SE REALIZÓ: {operacion.fecha}")
                print(f"HORA EN LA QUE SE REALIZÓ:  {operacion.hora}")

    def _crear_operacion(self, operacion, monto):
        momento_actual = datetime.datetime.now()
        hora_actual = momento_actual.strftime("%I:%M %p")
        fecha_actual = momento_actual.strftime("%d/%m/%Y")

        historial = Operacion(fecha_actual, hora_actual, operacion, monto)
        return historial

    def _anexar_operacion(self, operacion):
        self.historial.append(operacion)

def serializar_cuenta(cuenta_bancaria):
    dicionario_cuenta = copy.copy(cuenta_bancaria.__dict__)
    hist_indep = [operacion.__dict__ for operacion in cuenta_bancaria.historial]
    dicionario_cuenta["historial"] = hist_indep
    return dicionario_cuenta

def deserializar_cuenta(dict_cuenta):
    historial = []
    id_cuenta = dict_cuenta["id_cuenta"]
    for operacion in dict_cuenta["historial"]:
        historial.append(Operacion(operacion["fecha"], operacion["hora"], operacion["operacion"], operacion["monto"]))
    cuenta_obj = CuentaBancaria(dict_cuenta["titular"], dict_cuenta["balance"], dict_cuenta["nip"])
    cuenta_obj.historial = historial
    cuenta_obj.id_cuenta = id_cuenta
    return cuenta_obj

def guardar_cambios():
    with open(ruta_json, "w", encoding="utf-8") as archivo_cuentas_esc:
        json.dump(usuarios, archivo_cuentas_esc, indent=4, ensure_ascii=False)

def obtener_usuario(input_usuario):
    for usuario in usuarios:
        if usuarios[usuario]["titular"] == input_usuario:
            dicionario_cuenta = usuarios[usuario]
            return dicionario_cuenta
    dicionario_cuenta = None
    return dicionario_cuenta

def validar_nip(nip, cuenta):
    return cuenta.nip == nip

#FUNCIÓN PRINCIPAL. ES EL MENÚ PRINCIPAL
def menu_principal(cuenta):
    while True:
        print("-----------------MENÚ DE CUENTA-----------------")
        print()
        print("Usted puede realizar las siguientes operaciones:")
        print()
        print("-Realizar  un Depósito-----------------------[1]")
        print("-Realizar un Retiro--------------------------[2]")
        print("-Consultar su Balance Actual-----------------[3]")
        print("-Consultar el Historal de Operaciones--------[4]")
        print()
        respuesta = input("¿Qué desea hacer? Ingrese su opción: ")
        print()
        print("------------------------------------------------")
        print()

        while respuesta not in ["1", "2", "3", "4"]:
            print("Respuesta invalida, vuelva a intentar.")
            print()
            respuesta = input("¿Qué desea hacer? Ingrese su opción: ")
            print()

        match respuesta:
            case "1":
                print("*****************DEPÓSITO*****************")

                while True:
                    try:
                        cantidad_dinero = float(input("Ingrese el monto del dinero a depositar: $"))
                        while cantidad_dinero <= 0:
                            print("CANTIDAD INVALIDA, VUELVA A INTENTAR")
                            cantidad_dinero = float(input("Ingrese el monto del dinero a depositar: $"))
                        break
                    except ValueError:
                        print("Ingrese el monto de la operación utilizando números.")

                cuenta.depositar(cantidad_dinero)
                print()
                print(f"Se han depositado: ${cantidad_dinero} MXN")
                print(f"Balance actual:    ${cuenta.balance} MXN")
                print()
                print("******************************************")
                print()

                guardar_cambios_final_operacion(cuenta)

            case "2":
                print("******************RETIRO******************")

                while True:
                    try:
                        cantidad_dinero = float(input("Ingrese el monto del dinero a retirar: $"))
                        while cantidad_dinero <= 0:
                            print("CANTIDAD INVALIDA, VUELVA A INTENTAR")
                            cantidad_dinero = float(input("Ingrese el monto del dinero a retirar: $"))
                        break
                    except ValueError:
                        print("Ingrese el monto de la operación utilizando números.")


                if not cuenta.retirar(cantidad_dinero):
                    print()
                    print("EL RETIRO NO ES POSIBLE:")
                    print("LA CANTIDAD ES MAYOR A LA QUE SE TIENE.")
                    print()
                    print(f"Se han intentado retirar: ${cantidad_dinero} MXN")
                    print(f"EL BALANCE ACTUAL NO HA SIDO MODIFICADO.")
                    print()
                    print("******************************************")
                    print()
                else:
                    print()
                    print(f"Se han retirado:  -${cantidad_dinero} MXN")
                    print(f"Balance actual:    ${cuenta.balance} MXN")
                    print()
                    print("******************************************")
                    print()

                guardar_cambios_final_operacion(cuenta)

            case "3":
                print("***********CONSULTA DE BALANCE************")
                print()
                cuenta.ver_balance()
                print()
                print("******************************************")
                print()

                guardar_cambios_final_operacion(cuenta)

            case "4":
                print("***********CONSULTA DE HISTORAL***********")
                print()
                cuenta.ver_historial()
                print()
                print("******************************************")
                print()

                guardar_cambios_final_operacion(cuenta)

        continuar = input("¿Desea realizar otra operación? [S/N] ").upper()

        while continuar not in ["S", "N"]:
            print("Respuesta invalida, vuelva a intentar.")
            continuar = input("¿Desea realizar otra operación? [S/N] ").upper()

        print()

        if continuar == "N":
            print(f"¡Gracias por usar PyBank, {cuenta.titular}!")
            break

def validar_respuesta(respuesta):

    while respuesta not in ["S", "N"]:
        print("Respuesta invalida, vuelva a intentar.")
        respuesta = input("¿Desea volver a intentarlo? [S/N] ").upper()

    return respuesta

def preguntar_cerrar_programa():
    print()
    print("El titular no existe.")
    continuar = input("¿Desea volver a intentarlo? [S/N] ").upper()
    print()

    return validar_respuesta(continuar)

def obtener_objeto_titular():
    while True:
        nombre = input("Ingrese el nombre del titular: ")

        try:
            cuenta_scope_funcion = deserializar_cuenta(obtener_usuario(nombre))
            break
        except TypeError:
            if preguntar_cerrar_programa() == "N":
                print("Gracias por usar PyBank!")
                cuenta_scope_funcion = None
                break

    return cuenta_scope_funcion

def guardar_cambios_final_operacion(cuenta):
    dic_cuenta = serializar_cuenta(cuenta)
    usuarios[cuenta.id_cuenta] = dic_cuenta
    guardar_cambios()



try:
    with open(ruta_json, "r", encoding= "utf-8") as archivo_cuentas_lec:
        usuarios = json.load(archivo_cuentas_lec)
except FileNotFoundError:
    usuarios = {}


print("¡Bienvenido a PyBank!")
print()
print("-Acceder a su cuenta bancaria.-[1]")
print("-Crear nueva cuenta bancaria.--[2]")
print()
opcion = input("¿Qué desea hacer?: ")
print()

while opcion not in ["1", "2"]:
    print("Respuesta invalida, vuelva a intentar.")
    print()
    opcion = input("¿Qué desea hacer?: ")
    print()

match opcion:
    case "1":
        cuenta_actual = obtener_objeto_titular()

        if  cuenta_actual is None:
            sys.exit()

        nip_ingresado = input("Ingrese su NIP: ")
        intentos = 0

        while not validar_nip(nip_ingresado, cuenta_actual):

            if intentos == 2:
                print("Has agotado los intentos de acceso, intentelo más tarde.")
                sys.exit()

            intentos += 1
            print("NIP incorrecto, vuelva a intenar.")
            nip_ingresado = input("Ingrese su NIP: ")

        print()
        print("Has accedido correctamete.")
        print()

        menu_principal(cuenta_actual)

    case  "2":
        print("Bienvenido a PyBank!")
        print()
        print("Le damos la bienvenida a nuestro banco a base de código de python.")
        print("Acontinuación le mostramos todo lo que nuestra cuenta de banco ofrece: ")
        print("-Depósitos y retiros 100% seguros y digitales.")
        print("-Consultas de dinero e historial.")
        print("-Un riguroso historial que lleva registro de todo lo que haga, en el momento que sea.")
        print("(Únicamente el dueño de la cuenta puede ver el historial de su cuenta, asi que es 100%")
        print("confidencial)")
        print()
        print("CREASE UNA CUENTA")
        print()

        nuevo_nombre = input("Ingrese el nombre del titular de la cuenta: ")
        todos_caracter = all( caracter.isalpha() or caracter.isspace() for caracter in nuevo_nombre)

        nombres = [dato["titular"] for dato in usuarios.values()]

        while not todos_caracter or nuevo_nombre in nombres:
            print("Nombre de titular invalido o ya existente, intende de nuevo.")
            nuevo_nombre = input("Ingrese el nombre del titular de la cuenta: ")
            todos_caracter = all(caracter.isalpha() or caracter.isspace() for caracter in nuevo_nombre)

        while True:
            try:
                balance_inicial = float(input("Ingrese con cuanto dinero creará su cuenta: $"))
                break
            except ValueError:
                print("Escriba la cantidad con números.")

        nip_nuevo = input("Escriba su NIP (contraseña de 4 dígitos para acceder a su cuenta): ")
        while len(nip_nuevo) != 4 or not(nip_nuevo.isdigit()):
            print("SOLO ESCRIBA 4 NÚMEROS PARA SU NIP")
            nip_nuevo = input("Escriba su NIP (contraseña de 4 dígitos para acceder a su cuenta): ")

        nueva_cuenta = CuentaBancaria(nuevo_nombre, balance_inicial, nip_nuevo)
        dic_nueva_cuenta = serializar_cuenta(nueva_cuenta)
        usuarios[nueva_cuenta.id_cuenta] = dic_nueva_cuenta
        guardar_cambios()

        print()
        print(f"Estimado {nueva_cuenta.titular},")
        print("has creado una cuenta en PyBank de manera exitosa!!!")
        print("Le aseguramos que será la mejor experiencia.")
        print("Para comenzar a usar su cuenta bancaria, vuelva a ejecutar")
        print("este script y acceda con los datos proporcionados.")
        print()
        print("¡Que tenga un excelente día!")
