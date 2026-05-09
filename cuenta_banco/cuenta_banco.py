import datetime
hora_actual = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
fecha_actual = str(datetime.datetime.now().date())

class Operacion:
    def __init__(self, fecha, hora, operacion, monto):
        self.fecha = fecha
        self.hora = hora
        self.operacion = operacion
        self.monto = monto

class CuentaBancaria:
    def __init__(self, titular, balance, nip):
        self.titular = titular
        self.balance = balance
        self.nip = nip
        self.historial = []

    def depositar(self, monto):
        self.balance += monto
        operacion = self._crear_operacion("PENDIENTE", "PENDIENTE", "Deposito", monto)
        self._anexar_operacion(operacion)

    def retirar(self, monto):
        self.balance -= monto
        operacion = self._crear_operacion("PENDIENTE", "PENDIENTE", "Retiro", monto)
        self._anexar_operacion(operacion)

    def ver_balance(self):
        operacion = self._crear_operacion("PENDIENTE", "PENDIENTE", "Consulta de balance", None)
        self._anexar_operacion(operacion)
        return self.balance

    def ver_historial(self):
        operacion = self._crear_operacion("PENDIENTE", "PENDIENTE", "Consulta de historial de operaciones de cuenta", None)
        self._anexar_operacion(operacion)
        return self.historial


    def _crear_operacion(self, fecha, hora, operacion, monto):
        historial = Operacion(fecha, hora, operacion, monto)
        return historial
    def _anexar_operacion(self, operacion):
        self.historial.append(operacion)

