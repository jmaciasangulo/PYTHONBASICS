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
        hora_actual = datetime.datetime.now().strftime("%I:%M %p")
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")

        historial = Operacion(fecha_actual, hora_actual, operacion, monto)
        return historial

    def _anexar_operacion(self, operacion):
        self.historial.append(operacion)

def serializar_cuenta(cuenta_bancaria):
    dic_cuenta = cuenta_bancaria.__dict__
    hist_indep = [operacion.__dict__ for operacion in cuenta_bancaria.historial]
    dic_cuenta["historial"] = hist_indep
    return dic_cuenta

def deserializar_cuenta(dict_cuenta):
    historial = []
    for operacion in dict_cuenta["historial"]:
        historial.append(Operacion(operacion["fecha"], operacion["hora"], operacion["operacion"], operacion["monto"]))
    cuenta_obj = CuentaBancaria(dict_cuenta["titular"], dict_cuenta["balance"], dict_cuenta["nip"])
    cuenta_obj.historial = historial
    return cuenta_obj