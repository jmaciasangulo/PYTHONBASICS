import datetime
import sys
import uuid
import sqlite3
from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario : str
    nombre : str
    contrasena : str

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

    def _validar_dias_retraso(self, dias_retraso):
        if not isinstance(dias_retraso, int):
            raise ValueError("Los días de retraso deben de ser un número entero")

class Libro(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, paginas, genero):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.paginas = paginas
        self.genero = genero

    def calcular_multa(self, dias_retraso):
        self._validar_dias_retraso(dias_retraso)
        multa = dias_retraso * 5
        return multa

class Pelicula(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, duracion, clasificacion):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.duracion = duracion
        self.clasificacion = clasificacion

    def calcular_multa(self, dias_retraso):
        self._validar_dias_retraso(dias_retraso)
        multa = dias_retraso * 10
        return multa

class Revista(MaterialBibliografico):

    def __init__(self, titulo, autor, fecha_adquisicion, numero_edicion, periodicidad):
        super().__init__(titulo, autor, fecha_adquisicion)
        self.numero_edicion = numero_edicion
        self.periodicidad = periodicidad

    def calcular_multa(self, dias_retraso):
        self._validar_dias_retraso(dias_retraso)
        multa = dias_retraso * 3
        return multa

conexion = sqlite3.connect("sistema_bibliotecario.db")
basedatos = conexion.cursor()

basedatos.execute("PRAGMA foreign_keys = ON")

basedatos.execute("CREATE TABLE IF NOT EXISTS materiales_bibliograficos(id TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, disponibilidad INTEGER)")

basedatos.execute("CREATE TABLE IF NOT EXISTS peliculas( id_pelicula TEXT PRIMARY KEY, autor TEXT, fecha_adquisicion TEXT, duracion TEXT, clasificacion TEXT, FOREIGN KEY (id_pelicula) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS libros( id_libro TEXT PRIMARY KEY, autor TEXT, fecha_adquisicion TEXT, paginas INTEGER, genero TEXT, FOREIGN KEY (id_libro) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

basedatos.execute("CREATE TABLE IF NOT EXISTS revistas( id_revista TEXT PRIMARY KEY, autor TEXT, fecha_adquisicion TEXT, numero_edicion INTEGER, periodicidad TEXT, FOREIGN KEY (id_revista) REFERENCES materiales_bibliograficos(id) ON DELETE CASCADE)")

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
            usuario = menu_iniciar_sesion()
            cuenta_usuario = instanciar_usuario(usuario)
            menu_principal(cuenta_usuario)

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

    return id_usuario_input

def menu_principal(cuenta):
    while True:
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

        match opcion:
            case "1":
                menu_donar_material()

            case "2":
                pass

            case "3":
                pass

            case "4":
                pass

            case "5":
                pass

        repetir_bucle = input("Desea volver a hacer otra operación? [S/N]: ").upper()

        while repetir_bucle not in ["S", "N"]:
            print("Opción invalida, vuelva a intentar...")
            repetir_bucle = input("Desea volver a hacer otra operación? [S/N]: ").upper()

        if repetir_bucle == "N":
            break

def instanciar_usuario(usuario):

    basedatos.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (usuario,))
    datos_usuario = basedatos.fetchone()

    cuenta_usuario = Usuario(datos_usuario[0], datos_usuario[1], datos_usuario[2])

    return cuenta_usuario

def menu_donar_material():
    print("Muchas gracias por donar material a la biblioteca!!!")
    print()
    print("Para concluir, realiza el siguiente formulario:")
    tipo_material = input("Ingrese el tipo de material [LIBRO, REVISTA, PELICULA]: ").upper()

    while tipo_material not in ["LIBRO", "REVISTA", "PELICULA"]:
        print("Opccion invalida, vuelva a intentar...")
        tipo_material = input("Ingrese el tipo de material [LIBRO, REVISTA, PELICULA]: ").upper()

    titulo = input("Ingrese el titulo del material: ")
    autor = input("Ingrese el autor del material: ")
    fecha_adquisicion = datetime.datetime.now().strftime("%Y-%m-%d")

    match tipo_material:
        case "LIBRO":
            paginas = input("Ingrese el número de paginas del material: ")
            genero = input("Ingrese el genero del material: ")

            nuevo_material = Libro(titulo, autor, fecha_adquisicion, paginas, genero)

            basedatos.execute(" INSERT INTO materiales_bibliograficos VALUES (?, ?, ?, ?)",
                              (nuevo_material.id_material, tipo_material, nuevo_material.titulo, nuevo_material.disponiblidad ))
            basedatos.execute("INSERT INTO libros VALUES (?, ?, ?, ?, ?)",
                              (nuevo_material.id_material, nuevo_material.autor, nuevo_material.fecha_adquisicion, nuevo_material.paginas, nuevo_material.genero))
            conexion.commit()
        case "REVISTA":
            numero_edicion = input("Ingrese el numero de edicion de la revista: ")
            periodicidad = input("Ingrese la periodicidad de la revista: ")

            nuevo_material = Revista(titulo, autor, fecha_adquisicion, numero_edicion, periodicidad)

            basedatos.execute("INSERT INTO materiales_bibliograficos VALUES (?, ?, ?, ?)",
                              (nuevo_material.id_material, tipo_material, nuevo_material.titulo, nuevo_material.disponiblidad))
            basedatos.execute("INSERT INTO libros VALUES (?, ?, ?, ?, ?)",
                              (nuevo_material.id_material, nuevo_material.autor, nuevo_material.fecha_adquisicion, nuevo_material.numero_edicion, nuevo_material.periodicidad))
            conexion.commit()
        case "PELICULA":
            duracion = input("Ingrese la duracion de la película (en minutos): ")
            clasificacion = input("Ingrese la clasificación de la película: ")

            nuevo_material = Pelicula(titulo, autor, fecha_adquisicion, duracion, clasificacion)

            basedatos.execute("INSERT INTO materiales_bibliograficos VALUES (?, ?, ?, ?)",
                              (nuevo_material.id_material, tipo_material, nuevo_material.titulo, nuevo_material.disponiblidad ))
            basedatos.execute("INSERT INTO libros VALUES (?, ?, ?, ?, ?)",
                              (nuevo_material.id_material, nuevo_material.autor, nuevo_material.fecha_adquisicion, nuevo_material.duracion, nuevo_material.clasificacion))
            conexion.commit()

    print(f"El registro de {titulo} ha sido llevado a cabo con exito.")
    print("Te agradecemos de corazon por donar a nuestra biblioteca!!!")

def menu_pedir_prestado_material(cuenta):
    print("Prestar Material.")
    print()
    basedatos.execute(
        "SELECT COUNT(*) FROM historial_prestamos WHERE id_usuario = ? AND WHERE fecha_devolucion IS NULL", (cuenta,))
    total_prestamos = basedatos.fetchone()[0]

    if total_prestamos == 5:
        print("Usted tiene ya ha alcanzado el límite de prestamos.")
        print("Regrese al menos un material para pode obtener otro.")
    else:
        while True:
            material_buscar = input("Ingrese el nombre o el ID del material que desea buscar: ")
            basedatos.execute("SELECT * FROM materiales_bibliograficos WHERE id = ? OR WHERE titulo = ?", (material_buscar, material_buscar))
            resultados = basedatos.fetchall()

            print()
            print("RESULTADOS DE BUSQUEDA")
            for tupla in resultados:
                print()
                print("ID:     ", tupla[0])
                print("TIPO:   ", tupla[1])
                print("TITULO: ", tupla[2])
                if tupla[3] == 0:
                    print(" ESTE MATERIAL ESTÁ DISPONIBLE")
                else:
                    print("ESTE MATERIAL NO ESTÁ DISPONIBLE")

            print("Para mejores resultados, consulte los materiales disponibles y prestados.")

            repetir_busqueda = input("Desea volver a buscar material? [S/N]: ").upper()

            while repetir_busqueda not in ["S", "N"]:
                print("Opción invalida, vuelva a intentar...")
                repetir_busqueda = input("Desea volver a buscar material? [S/N]: ").upper()

            if repetir_busqueda == "N":
                break

            id_material = input("Ingrese el ID del material que desea pedir prestado: ")
            basedatos.execute("SELEC * FROM materiales_bibliograficos WHERE id_material = ?", (id_material,))
            material_seleccionado = basedatos.fetchone()

            print("MATERIAL SELECCIONADO: ")

            print("ID:     ", material_seleccionado[0])
            print("TITULO: ", material_seleccionado[2])
menu_acceder()