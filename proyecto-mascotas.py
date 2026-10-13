
from abc import ABC, abstractmethod
import threading
import json
import os

# Excepcion personalizada
class MascotaNoEncontradaError(Exception):
    pass


# Interfaz para describir objetos
class Describible(ABC):
    @abstractmethod
    def describir(self):
        pass


# Clase abstracta que representa un animal
class Animal(ABC):
    @abstractmethod
    def hacer_sonido(self):
        pass


# Clase principal de las mascotas
class Mascota(Animal, Describible):

    def __init__(self, nombre, especie, edad, peso):
        self.nombre = nombre
        self._especie = especie
        self.__edad = edad
        self.peso = peso

    def comer(self):
        print(f"{self.nombre} esta comiendo.")

    def dormir(self):
        print(f"{self.nombre} esta durmiendo.")

    def jugar(self):
        print(f"{self.nombre} esta jugando.")

    # Describir los datos de la mascota
    def describir(self):
        return (
            f"Nombre: {self.nombre}, "
            f"Especie: {self._especie}, "
            f"Edad: {self.__edad} años, "
            f"Peso: {self.peso} kg"
        )

    # Consultar la edad privada
    def obtener_edad(self):
        return self.__edad

    # Argumento por defecto: simula sobrecarga
    def mostrar(self, mensaje="Informacion de la mascota"):
        print(f"{mensaje}: {self.describir()}")

    # Comparar mascotas por nombre
    def __eq__(self, otra_mascota):
        if not isinstance(otra_mascota, Mascota):
            return False
        return self.nombre == otra_mascota.nombre

    # Crear una mascota desde un texto
    @classmethod
    def desde_texto(cls, texto):
        nombre, especie, edad, peso = texto.split(",")
        return cls(nombre, especie, int(edad), float(peso))

    # Comprobar si una mascota es adulta
    @staticmethod
    def es_adulta(edad):
        return edad >= 2

    def hacer_sonido(self):
        print(f"{self.nombre} hace un sonido.")


# Clase Perro: sobrescribe hacer_sonido
class Perro(Mascota):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Guau!")


# Clase Gato: sobrescribe hacer_sonido
class Gato(Mascota):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Miau!")


# Clase que administra las mascotas
class Veterinaria:

    def __init__(self, nombre):
        self.nombre = nombre
        self.mascotas = []

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)

    # Buscar una mascota por su nombre
    def buscar_mascota(self, nombre):
        for mascota in self.mascotas:
            if mascota.nombre.lower() == nombre.lower():
                return mascota

        raise MascotaNoEncontradaError(
            f"No se encontro una mascota llamada {nombre}"
        )

    def mostrar_mascotas(self):
        print(f"\nMascotas de {self.nombre}:")
        for mascota in self.mascotas:
            print(mascota.describir())
            
    # Guardar las mascotas en un archivo JSON
    def guardar_json(self, archivo):
        datos = []

        for mascota in self.mascotas:
            datos.append({
                "nombre": mascota.nombre,
                "especie": mascota._especie,
                "edad": mascota.obtener_edad(),
                "peso": mascota.peso
            })

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            print("Mascotas guardadas correctamente.")

        except OSError as error:
            print("Error al guardar el archivo:", error)

    # Leer mascotas desde un archivo JSON
    def leer_json(self, archivo):
        if not os.path.exists(archivo):
            raise FileNotFoundError("El archivo no existe.")

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            mascotas_leidas = []

            for dato in datos:
                if dato["especie"].lower() == "perro":
                    mascota = Perro(
                        dato["nombre"], dato["especie"],
                        dato["edad"], dato["peso"]
                    )
                elif dato["especie"].lower() == "gato":
                    mascota = Gato(
                        dato["nombre"], dato["especie"],
                        dato["edad"], dato["peso"]
                    )
                else:
                    mascota = Mascota(
                        dato["nombre"], dato["especie"],
                        dato["edad"], dato["peso"]
                    )

                mascotas_leidas.append(mascota)

            return mascotas_leidas

        except json.JSONDecodeError as error:
            raise ValueError("El archivo JSON tiene datos dañados.") from error



# Crear las mascotas
mascota1 = Perro("Luna", "Perro", 3, 12.5)
mascota2 = Gato("Michi", "Gato", 2, 4.2)
mascota3 = Perro("Rocky", "Perro", 5, 18.0)


# Mostrar informacion y acciones
mascota1.mostrar()
mascota2.mostrar("Datos")
mascota1.comer()
mascota2.dormir()
mascota3.jugar()


# Demostrar polimorfismo
print("\nSonidos de las mascotas:")
for mascota in [mascota1, mascota2, mascota3]:
    mascota.hacer_sonido()


# Comparar objetos
mascota4 = Perro("Luna", "Perro", 3, 12.5)
print("\n¿Son el mismo objeto?", mascota1 is mascota4)
print("¿Son iguales por nombre?", mascota1 == mascota4)


# Usar classmethod y staticmethod
mascota5 = Mascota.desde_texto("Max,Perro,4,15.5")
mascota5.mostrar()
print("¿Max es adulta?", Mascota.es_adulta(
    mascota5.obtener_edad()
))


# Registrar mascotas en la veterinaria
veterinaria = Veterinaria("Amigos Peludos")
veterinaria.agregar_mascota(mascota1)
veterinaria.agregar_mascota(mascota2)
veterinaria.agregar_mascota(mascota3)
veterinaria.mostrar_mascotas()


# Probar la excepcion personalizada
try:
    mascota = veterinaria.buscar_mascota("Luna")
    print("\nMascota encontrada:", mascota.describir())

    veterinaria.buscar_mascota("Toby")

except MascotaNoEncontradaError as error:
    print("\nError:", error)

# Funcion que procesa una mascota
def procesar_mascota(mascota):
    print(f"Procesando a {mascota.nombre}...")
    mascota.hacer_sonido()


# Crear dos hilos
hilo1 = threading.Thread(
    target=procesar_mascota,
    args=(mascota1,)
)

hilo2 = threading.Thread(
    target=procesar_mascota,
    args=(mascota2,)
)

# Iniciar los hilos
print("\nIniciando tareas en paralelo:")
hilo1.start()
hilo2.start()

# Esperar a que ambos terminen
hilo1.join()
hilo2.join()

print("Todas las tareas terminaron.")


# Ejercicio 6: guardar y recuperar mascotas
veterinaria.guardar_json("mascotas.json")

try:
    mascotas_recuperadas = veterinaria.leer_json("mascotas.json")

    print("\nMascotas recuperadas del archivo:")
    for mascota in mascotas_recuperadas:
        print(mascota.describir())

except (FileNotFoundError, ValueError) as error:
    print("No se pudieron recuperar las mascotas:", error)
