#PROYECTO INICIADO EL 20 DE ABRIL DEL 2026
from decimal import Decimal, InvalidOperation, ROUND_DOWN

class CuentaDeBanco:

    def __init__(self, nombre, balance, nip):
        self.nombre = nombre
        self.balance = balance
        self.nip = nip
# IMPRIME ATRIBUTOS EN PANTALLA
    def atributos(self):
        print(f"Nombre: {self.nombre}")
        print(f"Balance: $ {self.balance} USD")
        print(f"NIP: {self.nip}")
# PIDE AL USUARIO UN MONTO POR MEDIO DE LA TERMINAL. VALIDA QUE EL EL MONTO SE ESCRIBA USANDO NÚMEROS.
# VALIDA QUE SEA POSITIVO. REVISA SI TIENE DECIMALES. INDICA AL USUARIO QUE SE GUARDARÁN LOS DOS PRIMEROS DECIMALES.
# TRUNCA LOS 2 PRIMEROS DECIMALES. MODIFICA EL BALANCE SEGÚN EL MONTO. MUESTRA EN PANTALLA EL MONTO INGRESADO Y EL BALANCE MODIFICADO
#    def depositar(self):
#        while True:
#            try:
#                monto = Decimal(input("\nEscriba la cantidad a depositar: "))
#                if monto <= 0:
#                    print("Deposito invalido, escriba solo números positivos")
#                    continue
#                str_monto = str(monto)
#                if "." in str_monto:
#                    decimales = str_monto.split(".")[1]
#                    if len(decimales) > 2:
#                        print("El programa solo guardará los primeros 2 decimales")
#                        monto = monto.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
#                break
#            except InvalidOperation:
#                print("Digite en números la cantidad a depositar.")
#
#        self.balance += monto
#        print(f"Deposito por la cantidad de: {monto} USD")
#        print(f"Balance actual: {self.balance} USD")
    def

    def retirar(self):
        while True:
            try:
                monto = Decimal(input("\nEscriba la cantidad a retirar: "))
                if monto <= 0:
                    print("Deposito invalido, escriba solo números positivos")
                    continue
                str_monto = str(monto)
                if "." in str_monto:
                    decimales = str_monto.split(".")[1]
                    if len(decimales) > 2:
                        print("El programa solo guardará los primeros 2 decimales")
                        monto = monto.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
                break
            except InvalidOperation:
                print("Digite en números la cantidad a depositar.")

        self.balance -= monto
        print(f"Retiro por la cantidad de: {monto} USD")
        print(f"Balance actual: {self.balance} USD")

class Operacion:

    def __init__(self, tipo, fecha, hora,):
        self.tipo = tipo
        self.fecha = fecha
        self.hora = hora




mi_cuenta = CuentaDeBanco("Jesús Alejandro Macías Angulo", 130000, 2821)
mi_cuenta.atributos()
#mi_cuenta.depositar()
mi_cuenta.retirar()
mi_cuenta.atributos()