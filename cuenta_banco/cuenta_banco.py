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

#HOY HICE: las funciones restantes, o sea todas, a excepcion de depositar().
#QUE HARÉ MAÑANA: Corregiré como se ve la hora al momento de describir un objeto de la clase Operacion

