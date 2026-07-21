import uuid
import sqlite3


class MaterialBibliografico:

    def __init__(self, titulo, autor, fecha_adquisicion):

        self.id_material = str(uuid.uuid7())
        self.titulo = titulo
        self.autor = autor
        self.fecha_adquisicion = fecha_adquisicion
        self.disponiblidad = True

    def prestar(self):
        self.disponiblidad = False

    def devolver(self):
        self.disponiblidad = True

    def calcular_multa(self, dias_retraso):
        raise NotImplementedError("Este método solo funciona en las clases hijas de esta misma clase.")


class Libro(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, paginas, genero):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.paginas = paginas
        self.genero = genero

    def calcular_multa(self, dias_retraso):
        if dias_retraso is not int:
            raise ValueError("Los días de retraso deben der ser un número entero")
        multa = dias_retraso * 5
        return multa

class Pelicula(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, duracion, clasificacion):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.duracion = duracion
        self.clasificacion = clasificacion

    def calcular_multa(self, dias_retraso):

        if dias_retraso is not int:
            raise ValueError("Los días de retraso deben de ser un número entero")
        multa = dias_retraso * 10
        return multa

class Revista(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, numero_edicion, periodicidad):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.numero_edicion = numero_edicion
        self.periodicidad = periodicidad

    def calcular_multa(self, dias_retraso):
        if dias_retraso is not int:
            raise ValueError("Los días de retraso deben de ser un número entero")
        multa = dias_retraso * 3
        return multa

conexion = sqlite3.connect("sistema_bibliotecario.db")
basedatos = conexion.cursor()

basedatos.execute("PRAGMA foreign_keys = ON")

basedatos.execute("CREATE TABLE IF NOT EXISTS materiales_bibliograficos(id TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, disponibilidad INTEGRER)")

basedatos.execute("CREATE TABLE IF NOT EXISTS peliculas( id_pelicula TEXT PRIMARY KEY, titulo TEXT, director TEXT, fecha_adquisicion TEXT, duracion TEXT, clasificacion TEXT, FOREIGN KEY (id_pelicula) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS libros( id_libro TEXT PRIMARY KEY, titulo TEXT, autor TEXT, fecha_adquisicion TEXT, paginas INTEGER, genero TEXT, FOREIGN KEY (id_libro) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")