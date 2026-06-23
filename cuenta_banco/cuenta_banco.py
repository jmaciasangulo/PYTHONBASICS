import datetime
import json
import sys
import uuid


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
        self.balance -= monto
        operacion = self._crear_operacion("Retiro", monto)
        self._anexar_operacion(operacion)

    def ver_balance(self):
        operacion = self._crear_operacion("Consulta de balance", None)
        self._anexar_operacion(operacion)
        return self.balance

    def ver_historial(self):
        operacion = self._crear_operacion("Consulta de historial de operaciones de cuenta", None)
        self._anexar_operacion(operacion)
        return self.historial

    def _crear_operacion(self, operacion, monto):
        hora_actual = datetime.datetime.now().strftime("%I:%M %p")
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

        historial = Operacion(fecha_actual, hora_actual, operacion, monto)
        return historial

    def _anexar_operacion(self, operacion):
        self.historial.append(operacion)

def serializar_cuenta(cuenta_bancaria):
    dicionario_cuenta = cuenta_bancaria.__dict__
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
    with open("cuentas.json", "w", encoding="utf-8") as archivo_cuentas_esc:
        json.dump(usuarios, archivo_cuentas_esc, indent=4, ensure_ascii=False)

def obtener_usuario(input_usuario):
    for usuario in usuarios:
        if usuarios[usuario]["titular"] == input_usuario:
            dicionario_cuenta = usuarios[usuario]
            return dicionario_cuenta
    dicionario_cuenta = None
    return dicionario_cuenta

def validar_nip(nip):
    global cuenta_actual
    if cuenta_actual.nip == nip:
        acceso = True
        return acceso
    else:
        return False

def menu_principal(cuenta):
    print("-----------------MENÚ DE CUENTA-----------------")
    print()
    print("Usted puede realizar las siguientes operaciones:")
    print("-Realizar  un Depósito-----------------------[1]")
    print("-Realizar un Retiro--------------------------[2]")
    print("-Consultar su Balance Actual-----------------[3]")
    print("-Consultar el Historal de Operaciones--------[4]")
    print()
    respuesta = input("¿Qué desea hacer? Ingrese su opción: ")

    while respuesta not in ["1", "2", "3", "4"]:
        print("Respuesta invalida, vuelva a intentar.")
        respuesta = input("¿Qué desea hacer? Ingrese su opción: ")

    match respuesta:
        case "1":
            print("*****************DEPÓSITO*****************")
            cantidad_dinero = input("Ingrese el monto del dinero a depositar: $")


try:
    with open("cuentas.json", "r", encoding= "utf-8") as archivo_cuentas_lec:
        usuarios = json.load(archivo_cuentas_lec)
except FileNotFoundError:
    usuarios = {}

cuenta_actual = None

print("¡Bienvenido a PyBank!")
print()
print("-Acceder a su cuenta bancaria.-[1]")
print("-Crear nueva cuenta bancaria.--[2]")
print()
opcion = input("¿Qué desea hacer?: ")
print()

while opcion not in ["1", "2"]:
    print("Respuesta invalida, vuelva a intentar.")
    opcion = input("¿Qué desea hacer?: ")
    print()

match opcion:
    case "1":
        nombre = input("Ingrese el nombre del titular: ")

        dic_cuenta = obtener_usuario(nombre)

        if dic_cuenta:

            cuenta_actual = deserializar_cuenta(dic_cuenta)
            nip_ingresado = input("Ingrese su NIP: ")
            intentos = 0

            while not validar_nip(nip_ingresado):

                if intentos == 2:
                    print("Has agotado los intentos de acceso, intentelo más tarde.")
                    sys.exit()

                intentos += 1
                print("NIP incorrecto, vuelva a intenar.")
                nip_ingresado = input("Ingrese su NIP: ")

            print()
            print("Has accedido correctamete.")

        else:
            print("El usuario no existe")

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

        nombre = input("Ingrese el nombre del titular de la cuenta: ")
        todos_caracter = all( caracter.isalpha() or caracter.isspace() for caracter in nombre)
        while not todos_caracter:
            print("Escriba su nombre en letras.")
            nombre = input("Ingrese el nombre del titular de la cuenta: ")
            todos_caracter = all(caracter.isalpha() or caracter.isspace() for caracter in nombre)

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
