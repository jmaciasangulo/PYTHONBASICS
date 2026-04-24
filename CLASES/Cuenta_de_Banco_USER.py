class Usuario:
    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena

    def get_usuario(self):
        return self.usuario

    def set_usuario(self, nuevousuario):
        self.usuario = nuevousuario

    def get_contrasena(self):
        return self.contrasena

    def set_contrasena(self, contrasena):
        self.contrasena = contrasena
