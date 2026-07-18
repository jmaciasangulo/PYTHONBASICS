class MaterialBibliografico:

    def __init__(self, titulo, autor, fecha_adquisicion):

        self.id_material = None
        self.titulo = titulo
        self.autor = autor
        self.fecha_adquisicion = fecha_adquisicion
        self.disponiblidad = True

    def prestar(self):
        self.disponiblidad = False

    def devolver(self):
        self.disponiblidad = True