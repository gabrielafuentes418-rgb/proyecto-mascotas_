
from abc import ABC, abstractmethod


from abc import ABC, abstractmethod

# Clase abstracta que define el comportamiento de un animal
class Animal(ABC):

    @abstractmethod
    def hacer_sonido(self):
        pass

# Clase principal
class Mascota(Animal):
    def __init__(self, nombre, especie, edad, peso):
        self.nombre = nombre
        self._especie = especie
        self.__edad = edad
        self.peso = peso

    def comer(self):
        print(f"{self.nombre} está comiendo.")

    def dormir(self):
        print(f"{self.nombre} está durmiendo.")

    def jugar(self):
        print(f"{self.nombre} está jugando.")

    # Encapsulamiento: consultar la edad privada
    def obtener_edad(self):
        return self.__edad

    # Argumento por defecto: simula sobrecarga
    def mostrar(self, mensaje="Información de la mascota"):
        print(f"{mensaje}: {self.nombre}, {self._especie}, "
              f"{self.__edad} años, {self.peso} kg.")

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

    # Método estático
    @staticmethod
    def es_adulta(edad):
        return edad >= 2

    def hacer_sonido(self):
        print(f"{self.nombre} hace un sonido.")


# Herencia y polimorfismo
class Perro(Mascota):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Guau!")


class Gato(Mascota):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Miau!")


# Esta clase agrupa varias mascotas en una lista
class Veterinaria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mascotas = []

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)

    def mostrar_mascotas(self):
        print(f"\nMascotas de {self.nombre}:")
        for mascota in self.mascotas:
            mascota.mostrar()


# Crear objetos
mascota1 = Perro("Luna", "Perro", 3, 12.5)
mascota2 = Gato("Michi", "Gato", 2, 4.2)
mascota3 = Perro("Rocky", "Perro", 5, 18.0)

# Mostrar información
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
print("¿Max es adulta?",
      Mascota.es_adulta(mascota5.obtener_edad()))

# Agrupar mascotas en una veterinaria
veterinaria = Veterinaria("Amigos Peludos")
veterinaria.agregar_mascota(mascota1)
veterinaria.agregar_mascota(mascota2)
veterinaria.agregar_mascota(mascota3)
veterinaria.mostrar_mascotas()
