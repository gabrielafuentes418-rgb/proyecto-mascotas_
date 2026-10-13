
from abc import ABC, abstractmethod
import threading

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
