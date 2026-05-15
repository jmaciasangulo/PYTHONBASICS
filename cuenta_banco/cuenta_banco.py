import datetime
hora_actual = datetime.datetime.now().strftime("%I:%M %p")
fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

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
        historial = Operacion(fecha_actual, hora_actual, operacion, monto)
        return historial

    def _anexar_operacion(self, operacion):
        self.historial.append(operacion)

def serializar_cuenta(cuenta_bancaria):
    dic_cuenta = cuenta_bancaria.__dict__
    hist_indep = [operacion.__dict__ for operacion in cuenta_bancaria.historial]
    dic_cuenta["historial"] = hist_indep
    return dic_cuenta

LOGICA DE CARGA DE ARCHIVOS:
try:
    bloque de código que busca el archivo y carga la informacion
    en variables para que el programa trabaje con ellas
except FileNotFoundError:
    bloque de código que crea la estructura del diccionario vacía
    para que el programa trabaje con el
    
def guardar_cambios():
    Abre el archivo o lo crea de manera automatica si no existe,
    y descarga la informacion de los diccionarios al archivo .JSON
#Esta funcion se llama cada que el usuario haga una operacion, para si se llega a cerrar la sesion de 
#manera inesperada, los datos no se pierdan.
"""

#HOY HICE: Definí la estructura del archivo .json y la lógica de la carga y guardado de informacion en el .json
#QUE ME ATASCÓ: No sé como serializar los objetos para que se puedan guardar en archivos .JSON, No sé cual es la sintaxis
#para escribir la lógica de la descarga y carga de archivos
#QUE HARÉ MAÑANA: Mañana investigaré como serializar objetos y cual es la sintaxis para guardar y descargar la información en .JSONs
