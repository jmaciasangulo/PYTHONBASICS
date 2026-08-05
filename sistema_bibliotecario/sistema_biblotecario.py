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
        if dias_retraso < 0:
            raise ValueError("Los dias de retraso deben de ser un número positivo")

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
                menu_pedir_prestado_material(cuenta)

            case "3":
                menu_devolver_material(cuenta)

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
            basedatos.execute("INSERT INTO revistas VALUES (?, ?, ?, ?, ?)",
                              (nuevo_material.id_material, nuevo_material.autor, nuevo_material.fecha_adquisicion, nuevo_material.numero_edicion, nuevo_material.periodicidad))
            conexion.commit()
        case "PELICULA":
            duracion = input("Ingrese la duracion de la película (en minutos): ")
            clasificacion = input("Ingrese la clasificación de la película: ")

            nuevo_material = Pelicula(titulo, autor, fecha_adquisicion, duracion, clasificacion)

            basedatos.execute("INSERT INTO materiales_bibliograficos VALUES (?, ?, ?, ?)",
                              (nuevo_material.id_material, tipo_material, nuevo_material.titulo, nuevo_material.disponiblidad ))
            basedatos.execute("INSERT INTO peliculas VALUES (?, ?, ?, ?, ?)",
                              (nuevo_material.id_material, nuevo_material.autor, nuevo_material.fecha_adquisicion, nuevo_material.duracion, nuevo_material.clasificacion))
            conexion.commit()

    print(f"El registro de {titulo} ha sido llevado a cabo con exito.")
    print("Te agradecemos de corazon por donar a nuestra biblioteca!!!")

def menu_pedir_prestado_material(cuenta):
    print("Prestar Material.")
    print()
    basedatos.execute("SELECT COUNT(*) FROM historial_prestamos WHERE id_usuario = ? AND fecha_devolucion IS NULL", (cuenta.id_usuario,))
    total_prestamos = basedatos.fetchone()[0]

    if total_prestamos == 5:
        print("Usted tiene ya ha alcanzado el límite de prestamos.")
        print("Regrese al menos un material para pode obtener otro.")
    else:
        seleccionar_material = input("Ingrese el ID del material que desea pedir prestado: ")
        print()

        basedatos.execute("SELECT * FROM materiales_bibliograficos WHERE id = ?", (seleccionar_material,))
        resultado = basedatos.fetchone()

        if resultado is None:
            print("EL ID ingresado no existe.")
        elif resultado[3] == 0:
            print("El material seleccionado se encuentra ocupado, intentelo después.")
        else:
            material_seleccionado = imprimir_material_tipo(seleccionar_material, resultado[1], "SELECCIONADO")

            continuar = input("Desea proceder con el préstamo? [S/N] ").upper()

            while continuar not in ["S", "N"]:
                print("Respuesta invalida, vuelva a intentar...")
                continuar = input("Desea proceder con el préstamo? [S/N] ").upper()

            if continuar == "S":

                material_seleccionado.prestar()

                basedatos.execute("""UPDATE materiales_bibliograficos SET disponibilidad = ? WHERE id = ?""", (material_seleccionado.disponiblidad, material_seleccionado.id_material))

                id_prestamo = str(uuid.uuid7())
                id_material = material_seleccionado.id_material
                id_usuario = cuenta.id_usuario
                momento_actual = datetime.datetime.now()
                fecha_prestamo = momento_actual.strftime("%Y-%m-%d")
                fecha_limite = momento_actual + datetime.timedelta(days=20)
                fecha_limite = fecha_limite.strftime("%Y-%m-%d")
                fecha_devolucion = None

                basedatos.execute("""INSERT INTO historial_prestamos VALUES (?, ?, ?, ?, ?, ?)""",
                                  (id_prestamo, id_material, id_usuario, fecha_prestamo, fecha_limite, fecha_devolucion))

                conexion.commit()

                print("El material ha sido entregado a ti.")
                print("Recuerda cuidar el material :)")

            else:
                print("El prestamo ha sido cancelado.")

def menu_devolver_material(cuenta):

    basedatos.execute("""SELECT historial_prestamos.id_material, materiales_bibliograficos.tipo 
    FROM historial_prestamos
    JOIN materiales_bibliograficos ON historial_prestamos.id_material = materiales_bibliograficos.id
    WHERE historial_prestamos.id_usuario = ? AND historial_prestamos.fecha_devolucion IS NULL""", (cuenta.id_usuario,))
    resultados = basedatos.fetchall()

    if not resultados:
        print("Usted no tiene préstamos activos.")
    else:
        print("A continuación se presentan los materiales en su poseción.")
        for tupla in resultados:

            imprimir_material_tipo(tupla[0], tupla[1], "EN POSECIÓN")

        material_devolver = input("Ingrese el ID del material que desea devolver: ")

        ids_materiales_posecion = [tupla[0] for tupla in resultados]

        while material_devolver not in ids_materiales_posecion:
            print("El ID ingresado no corresponde a los materiales en su poseción.")
            material_devolver = input("Ingrese el ID del material que desea devolver: ")

        basedatos.execute("""SELECT tipo
        FROM materiales_bibliograficos
        WHERE id = ?""", (material_devolver,))
        tipo = basedatos.fetchone()[0]

        material_devolver = imprimir_material_tipo(material_devolver, tipo, "SELECCIONADO")

        continuar = input("¿Desea proceder con la devolución? [S/N] ").upper()

        while continuar not in ["S", "N"]:
            print("Respuesta invalida, vuelva a intentar.")
            continuar = input("¿Desea proceder con la devolución? [S/N] ").upper()

        if continuar == "S":
            material_devolver.devolver()
            basedatos.execute("""UPDATE  materiales_bibliograficos SET disponibilidad = ? WHERE id = ?""", (material_devolver.disponiblidad, material_devolver.id_material))

            basedatos.execute("""SELECT fecha_limite FROM historial_prestamos WHERE id_material = ? AND fecha_devolucion IS NULL""", (material_devolver.id_material,))
            fecha_limite = basedatos.fetchone()[0]

            momento_actual = datetime.datetime.now()
            fecha_devolucion = momento_actual.strftime("%Y-%m-%d")

            basedatos.execute("""UPDATE historial_prestamos SET fecha_devolucion = ? WHERE id_material = ?""", (fecha_devolucion, material_devolver.id_material))
            conexion.commit()

            fecha_limite = datetime.datetime.strptime(fecha_limite, "%Y-%m-%d")
            fecha_devolucion = datetime.datetime.strptime(fecha_devolucion, "%Y-%m-%d")

            dias_multa = (fecha_devolucion - fecha_limite).days

            if dias_multa < 1:
                dias_multa = 0

            multa = material_devolver.calcular_multa(dias_multa)

            if multa > 0:
                print(f"Usted tiene una multa de ${multa} pesos.")
                print("Asegurese de pagar su multa.")

            print("Muchas gracias por devolver el material :)")
        else:
            print("Devolución cancelada.")

def imprimir_material_tipo(id_seleccionado, tipo, cadena_texto):

    material_seleccionado = None

    match tipo:

        case "LIBRO":
            basedatos.execute("""SELECT *
                                            FROM materiales_bibliograficos
                                            JOIN libros ON materiales_bibliograficos.id = libros.id_libro
                                            WHERE materiales_bibliograficos.id = ?""", (id_seleccionado,))
            resultado = basedatos.fetchone()

            material_seleccionado = Libro(resultado[2], resultado[5], resultado[6], resultado[7], resultado[8])
            material_seleccionado.id_material = resultado[0]

            print(f"MATERIAL {cadena_texto}:")
            print()
            print(f"ID:       {material_seleccionado.id_material}")
            print(f"TIPO:     {resultado[1]}")
            print(f"TITULO:   {material_seleccionado.titulo}")
            print(f"AUTOR:    {material_seleccionado.autor}")
            print(f"PAGINAS:  {material_seleccionado.paginas}")
            print(f"GENERO:   {material_seleccionado.genero}")
            print()

        case "REVISTA":
            basedatos.execute("""SELECT *
                                            FROM materiales_bibliograficos
                                            JOIN revistas ON materiales_bibliograficos.id = revistas.id_revista
                                            WHERE materiales_bibliograficos.id = ?""",
                              (id_seleccionado,))
            resultado = basedatos.fetchone()

            material_seleccionado = Revista(resultado[2], resultado[5], resultado[6], resultado[7],
                                            resultado[8])
            material_seleccionado.id_material = resultado[0]

            print(f"MATERIAL {cadena_texto}:")
            print()
            print(f"ID:                 {material_seleccionado.id_material}")
            print(f"TIPO:               {resultado[1]}")
            print(f"TITULO:             {material_seleccionado.titulo}")
            print(f"AUTOR:              {material_seleccionado.autor}")
            print(f"NÚMERO DE EDICION:  {material_seleccionado.numero_edicion}")
            print(f"PERIODICIDAD:       {material_seleccionado.periodicidad}")
            print()

        case "PELICULA":
            basedatos.execute("""SELECT *
                                            FROM materiales_bibliograficos
                                            JOIN peliculas ON materiales_bibliograficos.id = peliculas.id_pelicula
                                            WHERE materiales_bibliograficos.id = ?""",
                              (id_seleccionado,))
            resultado = basedatos.fetchone()

            material_seleccionado = Pelicula(resultado[2], resultado[5], resultado[6], resultado[7],
                                             resultado[8])
            material_seleccionado.id_material = resultado[0]

            print(f"MATERIAL {cadena_texto}:")
            print()
            print(f"ID:                 {material_seleccionado.id_material}")
            print(f"TIPO:               {resultado[1]}")
            print(f"TITULO:             {material_seleccionado.titulo}")
            print(f"AUTOR:              {material_seleccionado.autor}")
            print(f"DURACIÓN:           {material_seleccionado.duracion} minutos")
            print(f"CLASIFICACIÓN:      {material_seleccionado.clasificacion}")
            print()
        case _:
            raise ValueError(f"El tipo del material desconocido {tipo}")

    return material_seleccionado

def menu_consultar_disponibles():
    print("Consultar disponibles.")
    print()
    tipo_consultar = input("Ingrese el tipo de materiales que desea consultar: ").upper()

    while tipo_consultar not in ["LIBRO", "LIBROS", "PELÍCULA", "PELÍCULAS", "PELICULA", "PELICULAS", "REVISTA", "REVISTAS"]:
        print("Respuesta invalida, vuelva a intentar...")
        tipo_consultar = input("Ingrese el tipo de materiales que desea consultar: ").upper()

    match tipo_consultar:
        case "LIBRO"| "LIBROS":

            basedatos.execute("""SELECT id FROM materiales_bibliograficos WHERE tipo = ? AND disponibilidad = ?""", ("LIBRO", 1))
            ids = basedatos.fetchall()

            if not ids:
                print("No hay libros disponibles")

            for tupla in ids:
                imprimir_material_tipo(tupla[0], "LIBRO", "DISPONIBLE")
            print("Final")

        case "PELICULA" | "PELICULAS" | "PELÍCULA" | "PELÍCULAS":

            basedatos.execute("""SELECT id FROM materiales_bibliograficos WHERE tipo = ? AND disponibilidad = ?""",
                              ("PELICULA", 1))
            ids = basedatos.fetchall()

            if not ids:
                print("No hay peliculas disponibles")

            for tupla in ids:
                imprimir_material_tipo(tupla[0], "PELICULA", "DISPONIBLE")

        case "REVISTA" | "REVISTAS":

            basedatos.execute("""SELECT id FROM materiales_bibliograficos WHERE tipo = ? AND disponibilidad = ?""",
                              ("REVISTA", 1))
            ids = basedatos.fetchall()

            if not ids:
                print("No hay revistas disponibles")

            for tupla in ids:
                imprimir_material_tipo(tupla[0], "REVISTA", "DISPONIBLE")

menu_acceder()