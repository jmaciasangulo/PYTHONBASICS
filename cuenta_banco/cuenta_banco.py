import datetime
import json
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
    global acceso
    if cuenta_actual.nip == nip:
        acceso = True
        return acceso
    else:
        return False

try:
    with open("cuentas.json", "r", encoding= "utf-8") as archivo_cuentas_lec:
        usuarios = json.load(archivo_cuentas_lec)
except FileNotFoundError:
    usuarios = {}

cuenta_actual = None
acceso = False

print("¡Bienvenido a PyBank!")
print()
print("-Acceder a su cuenta bancaria.-[1]")
print("-Crear nueva cuenta bancaria.--[2]")
opcion = int(input("¿Qué desea hacer?: "))

while opcion not in [1, 2]:
    print("Respuesta invalida, vuelva a intentar.")
    opcion = int(input("¿Qué desea hacer?: "))

match opcion:
    case 1:
        nombre = input("Ingrese el nombre del titular: ")

        dicionario_cuenta = obtener_usuario(nombre)

        if dicionario_cuenta:

            cuenta_actual = deserializar_cuenta(dicionario_cuenta)
            nip_ingresado = input("Ingrese su NIP: ")
            intentos = 0
            while not validar_nip(nip_ingresado):

                if intentos == 2:
                    print("Has agotado los intentos de acceso, intentelo más tarde.")
                    break

                intentos += 1
                print("NIP incorrecto, vuelva a intenar.")
                nip_ingresado = input("Ingrese su NIP: ")
                validar_nip(nip_ingresado)

        else:
            print("El usuario no existe")