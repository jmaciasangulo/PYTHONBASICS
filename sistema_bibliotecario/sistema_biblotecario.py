import sys
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
        if not isinstance(dias_retraso, int):
            raise ValueError("Los días de retraso deben de ser un número entero")
        raise NotImplementedError("Este método solo funciona en las clases hijas de esta misma clase.")


class Libro(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, paginas, genero):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.paginas = paginas
        self.genero = genero

    def calcular_multa(self, dias_retraso):
        multa = dias_retraso * 5
        return multa

class Pelicula(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, duracion, clasificacion):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.duracion = duracion
        self.clasificacion = clasificacion

    def calcular_multa(self, dias_retraso):
        multa = dias_retraso * 10
        return multa

class Revista(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, numero_edicion, periodicidad):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.numero_edicion = numero_edicion
        self.periodicidad = periodicidad

    def calcular_multa(self, dias_retraso):
        multa = dias_retraso * 3
        return multa

conexion = sqlite3.connect("sistema_bibliotecario.db")
basedatos = conexion.cursor()

basedatos.execute("PRAGMA foreign_keys = ON")

basedatos.execute("CREATE TABLE IF NOT EXISTS materiales_bibliograficos(id TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, disponibilidad INTEGER)")

basedatos.execute("CREATE TABLE IF NOT EXISTS peliculas( id_pelicula TEXT PRIMARY KEY, titulo TEXT, autor TEXT, fecha_adquisicion TEXT, duracion TEXT, clasificacion TEXT, FOREIGN KEY (id_pelicula) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS libros( id_libro TEXT PRIMARY KEY, titulo TEXT, autor TEXT, fecha_adquisicion TEXT, paginas INTEGER, genero TEXT, FOREIGN KEY (id_libro) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS revistas( id_revista TEXT PRIMARY KEY, titulo TEXT, autor TEXT, fecha_adquisicion TEXT, numero_edicion INTEGER, periodicidad TEXT, FOREIGN KEY (id_revista) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS usuarios( id_usuario TEXT PRIMARY KEY, nombre_usuario TEXT, contrasena TEXT)")

basedatos.execute("CREATE TABLE IF NOT EXISTS historial_prestamos ( id_prestamo TEXT PRIMARY KEY, id_material TEXT, id_usuario TEXT, fecha_prestamo TEXT, fecha_limite TEXT, fecha_devolucion TEXT, FOREIGN KEY (id_material) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE, FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL)")

def menu_crear_cuenta():
    print("Bienvenido a PyLibrary, una libreria escrita con codigo Python.")
    print()
    print("En nuestra libreria puedes acceder a un catalogo de:")
    print("-Libros")
    print("-Revistas")
    print("-Peliculas")
    print()
    print("Crea una cuenta y accede a nuestra libreria!!!")
    print()
    nuevo_id_usuario = validar_id_usuario()
    nombre_usuario = validar_nombre_usuario()
    print("Es momento de crear una contraseña, por favor use:")
    print("-Al menos 8 caracteres")
    print("-Letras mayusculas y minusculas")
    print("-Números")
    print("-Caracteres especiales")
    print()
    contrasena = validar_contrasena()

    basedatos.execute("INSERT INTO usuarios  VALUES (?, ?, ?)", (nuevo_id_usuario, nombre_usuario, contrasena))
    conexion.commit()

    print(f"Bienvenido {nombre_usuario}! Disfruta de los contenidos de nuestra libreria")
    print()
    print("Para acceder a la librería, vuelva a ejecutar este script e inicie sesión")
    sys.exit()

def validar_id_usuario():
    while True:

        nuevo_id_usuario = input("Escriba un ID de usuario, maximo 10 caracteres: ")

        if not  5 <= len(nuevo_id_usuario) <= 10 :
            print("Ingrese un id de 5 a 10 caracteres")
            continue

        basedatos.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = ?", (nuevo_id_usuario,))

        if basedatos.fetchone() is None:
            break

        print("El id de usuario ya existe, intenta con otro...")

    return nuevo_id_usuario

def validar_nombre_usuario():
    nombre_usuario = input("Ingrese el nombre de usuario de su preferencia: ")

    todos_caracter = all(caracter.isalpha() or caracter.isspace() for caracter in nombre_usuario)

    while not todos_caracter:
        print("Ingrese su nombre de usuario solo usando letras")
        nombre_usuario = input("Ingrese el nombre de usuario de su preferencia: ")
        todos_caracter = all(caracter.isalpha() or caracter.isspace() for caracter in nombre_usuario)

    return nombre_usuario

def validar_contrasena():
    while True:

        contrasena = input("Ingrese su contraseña: ")

        if not any(caracter.isupper() for caracter in contrasena):
            print("Ingrese al menos una letra mayuscula.")
            continue

        if not any(caracter.islower() for caracter in contrasena):
            print("Ingrese al menos una letra minuscula.")
            continue

        if not any(caracter.isdigit() for caracter in contrasena):
            print("Ingrese al menos un número.")
            continue

        especiales = "!@#$%^&*()-_=+[]{}|;:',.<>/?"

        if not any(caracter in especiales for caracter in contrasena):
            print("Ingrese al menos un caracter especial.")
            continue

        if not 8 <=len(contrasena) <= 20:
            print("Ingrese entre 8 a 20 caracteres")
            continue

        print("La contraseña es válida.")
        break
    return contrasena

def menu_acceder():
    print("Bienvenido a PyLibrary.")
    print()
    print("Para continuar inicie sesión-------[1]")
    print("O crea una cuenta si no tienes una-[2]")
    print()
    opcion = input("Ingrese su opcion: ")
    print()

    while opcion not in ["1", "2"]:
        print("Opción no válida, vuelva a intentar...")
        opcion = input("Ingrese su opcion: ")
        print()

    match opcion:

        case "1":
            menu_iniciar_sesion()

        case "2":
            menu_crear_cuenta()

def menu_iniciar_sesion():
    while True:
        id_usuario_input = input("Ingrese su id de usuario: ")

        basedatos.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = ?", (id_usuario_input,))

        if basedatos.fetchone() is None:
            print("El id de usuario ingresado no existe.")
            print()
            volver_intentar = input("¿Desea volver a intentar? [S/N]: ").upper()
            print()

            while volver_intentar not in ["S", "N"]:
                print("Opción invalida, vuelva a intentar...")
                volver_intentar = input("¿Desea volver a intentar? [S/N]: ").upper()
                print()

            if volver_intentar == "S":
                continue

            if volver_intentar == "N":
                sys.exit()

        else:
            break

    cont = 0

    while True:

        if cont == 3:
            print("Has agotado todos los intentos para acceder, intentalo más tarde.")
            sys.exit()

        contrasena_input = input("Ingrese su contraseña: ")

        cont += 1

        basedatos.execute("SELECT contrasena FROM usuarios WHERE id_usuario = ?", (id_usuario_input,))

        if basedatos.fetchone()[0] == contrasena_input:
            print("Contraseña correcta.")
            break

        else:
            print("Contraseña incorrecta.")

def menu_principal(cuenta):
    print("Bienvenido a PyLibrary.")
    print()
    print("Usted puede hacer lo siguiente en nuestra librería:")
    print("Donar material--------------------[1]")
    print("Pedir prestado un material--------[2]")
    print("Devolver un material--------------[3]")
    print("Consultar materiales disponibles--[4]")
    print("Consultar materiales prestados----[5]")
    print()
    opcion = input("Ingrese su opcion: ")

    while opcion not in ["1", "2", "3", "4", "5"]:
        print("Opción invalida, vuelva a intentar...")
        opcion = input("Ingrese su opcion: ")

menu_acceder()