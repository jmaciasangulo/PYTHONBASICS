#Este es un conversor de unidades, elaborado el 11 de marzo del 2026 y terminado el 15 de marzo del 2026.

#En este diccionario denominado "areas" están todas las unidades de área representadas en metros cuadrados.
areas = {
      "millas cuadradas": 2589988.110336,
      "kilometros cuadrados": 1000000,
      "hectareas": 10000,
      "acres": 4046.8564224,
      "decareas": 1000,
      "stremmas": 1000,
      "areas": 100,
      "metros cuadrados": 1,
      "pies cuadrados": 0.09290304,
      "yardas cuadradas": 0.83612736,
      "pulgadas cuadradas": 0.00064516,
      "centimetros cuadrados": 0.0001,
      "milimetros cuadrados": 0.000001
}
#al igual que el diccionario de areas, todas las divisas están representadas en dólares estadounidenses.
divisas = {
      "dolares canadienses": 0.73,
      "dolares estadounidenses": 1,
      "pesos mexicanos": 0.06,
      "yenes": 0.01,
      "yuanes": 0.15,
      "euros": 1.14,
      "libras esterlinas": 1.32,
      "dolares australianos": 0.70,
      "francos suizos": 1.23,
      "dolares hongkoneses": 0.13,
      "dolares neozelandeses": 0.53
}
#Unidad de peso base representada en kilogramos
peso = {
      "dracmas": 0.001771845195312,
      "gramos": 0.001,
      "kilogramos": 1,
      "libras": 0.45359237,
      "miligramos": 0.000001,
      "microgramos": 0.000000001,
      "onzas": 0.028349523125,
      "slugs": 14.593902937206,
      "stones": 6.35029318,
      "toneladas cortas": 907.18474,
      "toneladas métricas": 1000
}
#Datos representados en bytes
datos = {
      "bits": 0.125,
      "bytes": 1,
      "kilobytes": 1024,
      "megabytes": 1048576,
      "gigabytes": 1073741824,
      "terabytes": 1099511627776,
      "petabytes": 1125899906842624,
}
#datos representados en metros
longitud = {
      "años luz": 9460730472580800,
      "centimetros": 0.01,
      "decimetros": 0.1,
      "kilometros": 1000,
      "metros": 1,
      "milímetros": 0.001,
      "millas": 1609.344,
      "millas nauticas": 1852,
      "parsecs": 30856775814913673,
      "pies": 0.3048,
      "pulgadas": 0.0254,
      "unidades astronomicas": 149597870700,
      "yardas": 0.9144,
      "micrometro": 0.000001,
      "nanometros": 0.000000001
}
#datos representados en kilopascales
presion = {
      "kilopascales": 1,
      "atmosferas": 101.325,
      "bares": 100,
      "libras por pulgada cuadrada": 6.8947572931684,
      "pascales": 0.001,
      "pulgadas de mercurio": 3.386388157895,
      "torr": 0.13332236842105
}
#datos representados en metros por segundo
velocidad = {
      "kilometros por hora": 0.27777777777777777,
      "millas por hora": 0.44704,
      "nudo": 0.51444444444444,
      "pie por segundo": 0.3048,
      "metro por segundo": 1
}
tiempo = {
      "nanosegundo":  0.000000001,
      "microsegundo": 0.000001,
      "milisegundo": 0.001,
      "segundos": 1,
      "minutos": 60,
      "horas": 3600,
      "días": 86400,
      "semana": 604800,
      "años": 31536000,
      "decadas": 315360000,
      "siglos": 3153600000
}
#datos representados en metros cúbicos
volumen = {
      "centilitros": 0.00001,
      "centimetros cubicos": 0.000001,
      "metros cubicos": 1,
      "galones estadounidenses": 0.00378541,
      "cuartos estadounidenses": 0.000946353,
      "pintas estadounidenses": 0.000473176,
      "tazas americanas oficiales": 0.00024,
      "onzas liquidas estadounidenses": 0.00002957704,
      "cucharadas estadounidenses": 0.00001478633,
      "cucharaditas estadounidenses": 0.00000492853,
      "litros": 0.001,
      "mililitros": 0.00001,
      "galones imperial": 0.00454609,
      "cuarto imperial": 0.00113652,
      "pinta imperial": 0.000568261,
      "taza imperial": 0.000284131,
      "onza líquida imperial": 0.00002840909,
      "cucharada imperial": 0.00001775883,
      "cucharadita imperial": 0.00000592066,
      "pie cubico": 0.0283168,
      "pulgada cubica": 0.00001638806

}

#Esta es una lista donde están todas las opcciones de conversiones
options = {
      "area": areas,
      "divisa": divisas,
      "datos": datos,
      "longitud": longitud,
      "presion": presion,
      "velocidad": velocidad,
      "tiempo": tiempo,
      "volumen": volumen,
      "peso": peso
}
#La función "capture_information" tiene como propósito capturar la información que el usuario ingresa, la función se diseñó de
#tal manera que puda ser compatible con todos los tipos de conversion, ya que se usa la regla de 3 para hacer las conversiones.
"""
1m-----100cm | x= (10m * 100cm)/1m
10m-----x    | 
"""
#Esta funcion usa los parametros "diccionaryfunction", que es la que se usa en el proceso lógico.
def capture_information(diccionaryfunction):
      print(f"\nLas unidades para convertir son:\n")
      #Se imprimen todas las opcciones del diccionario de la conversion que se haga
      for clavesfunction in diccionaryfunction:
            print(clavesfunction)
      #Aquí el programa le pregunta al usuario que unidad se va a convertir.
      #El .lower() en este caso, sirve para simplificar la informacion para compararla después
      unitbasefunction = input("\nIngrese la unidad base: ").lower()
      #Se depura la variable, si la variable no está en el diccionario de las converiones del caso correspondiente,
      #se pide que vuelva a escribir la unidad de medida
      while unitbasefunction not in diccionaryfunction:
            print("Opcion incorrecta, vuelvalo a intentar")
            unitbasefunction = input(" Ingrese la unidad base: ").lower()
      #Se pide la magnitud que se va a convertir, el dato se castea a float por que el dato puede ser decimal
      magnitudebasefunction = float(input("Ingrese la magnitud: "))
      #Este input ingresa a qué unidad de medida se convertirán la magnitud y la unidad de medida que se solicitaron antes
      unitconvertedfunction = input(f"Ingrese la unidad a convertir: ").lower()
      #se depura la información de la misma forma que en la línea 76
      while unitconvertedfunction not in diccionaryfunction:
            print("Opcion incorrecta, vuelvalo a intentar")
            unitconvertedfunction = input(f"Ingrese la unidad a convertir: ").lower()
      #La función hizo el proceso de capturar la información, esa información se guardó en 3 distintas variables que son
      #las que regresa return, el valor de las variables ya está definido con base en la información que introduce el usuario.
      #Para entender mejor cada variable, vea el comentario que describe cada variable.
      #Los datos se usarán en la función "convertionunit" que es la que hace la regla de 3.
      return magnitudebasefunction, unitbasefunction, unitconvertedfunction
#Esta funcion (convertionunit) hace: la regla de 3 con base en los parametros que introdujo el usuario.
#E imprime en pantalla la convercion ya hecha. Para ser más preciso, muestra en pantalla la magnitud convertida y la
#unidad de medida a la que se solicitó convertir.
def convertionunit(magnitudebasefunction, unitbasefunction, unitconvertedfunction, unitconvertedstr):
      baseunit = magnitudebasefunction * unitbasefunction
      convertedmagnitude = baseunit / unitconvertedfunction
      return convertedmagnitude, unitconvertedstr
#------------------------------------------------------------------------------------------------------------------------

print("CONVERSOR DE UNIDADES\n")
print("En este conversor de unidades, podrás hacer converiones de:")
#se muestran todas las categorias de unidad de medida que se pueden convertir.
for claves in options:
      print(claves)
#Aquí definimos la variable "convertion" que nos indicará de que se hará conversión, usamos .lower() para que la variable
#se guarde en todas minusculas y sea más sencillo comparar resultados.
while True:
      convertion = input("¿Que conversion desea realizar?: ").lower()
      #aquí depuramos, si la variable no tiene algún valor que esté en el diccionario de "options" te dirá que es incorrecto y hace que
      #vuelvas a escribir tu respuesta.
      while convertion not in options:
            print("Opccion incorrecta, vuelvalo a intentar")
            convertion = input("¿Que conversion desea realizar?: ").lower()
      #Con este match, se le asignan a las variables de cadenas de texto lo que mostrarán en pantalla. Y a la variable
      #"diccionary", el diccionario con el cual trabajaran las funciones. También se hacen nuevas variables para usar el valor
      #asignado a cada unidad de medida, expresada en metros cuadrados; que se encuentra en el diccionario.
      diccionary = options[convertion]
      magnitudebase, unitbase, unitconverted = capture_information(diccionary)
      areabase_int = diccionary[unitbase]
      areaconverted_int = diccionary[unitconverted]
      print(f"\nEl resultado de convertir {magnitudebase} {unitbase} a {unitconverted} es:")
      resultmagnitude, factor = convertionunit(magnitudebase, areabase_int, areaconverted_int, unitconverted)
      print(f"{resultmagnitude} {factor}")
      seguirprograma = input("\n¿Desea hacer conversiones de nuevo? [SI/NO] ").lower()
      while seguirprograma not in ("si", "no"):
            print(f"{seguirprograma} no es una respuesta valida, escribe SI o NO")
            seguirprograma = input("¿Desea hacer converiones de nuevo? [SI/NO] ").lower()
      if seguirprograma == "no":
            break

