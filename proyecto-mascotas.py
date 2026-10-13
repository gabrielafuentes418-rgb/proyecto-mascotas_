
from abc import ABC, abstractmethod
import json
import threading


# Excepcion personalizada
class MascotaNoEncontradaError(Exception):
    pass


# Interfaz para describir objetos
class Describible(ABC):

    @abstractmethod
    def describir(self):
        pass


# Clase abstracta de los animales
class Animal(ABC):

    @abstractmethod
    def hacer_sonido(self):
        pass


# Clase principal de las mascotas
class Mascota(Animal, Describible):

    def __init__(self, nombre, especie, edad=0, peso=0.0):
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


# Perro sobrescribe el metodo heredado
class Perro(Mascota):

    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Guau!")


# Gato sobrescribe el metodo heredado
class Gato(Mascota):

    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Miau!")


# Composicion: clase que administra una lista de mascotas
class RegistroMascotas:

    def __init__(self):
        self.mascotas = []

    def agregar(self, mascota):
        self.mascotas.append(mascota)

    def listar(self):
        return self.mascotas


# Clase encargada de guardar y leer archivos JSON
class ArchivoMascotas:

    def guardar(self, mascotas, archivo):
        datos = []

        for mascota in mascotas:
            datos.append({
                "nombre": mascota.nombre,
                "especie": mascota._especie,
                "edad": mascota.obtener_edad(),
                "peso": mascota.peso
            })

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

        except OSError as error:
            raise OSError(
                "No se pudieron guardar las mascotas."
            ) from error

    def leer(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

        except json.JSONDecodeError as error:
            raise ValueError(
                "El archivo JSON contiene datos dañados."
            ) from error

        mascotas = []

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

            mascotas.append(mascota)

        return mascotas


# Veterinaria utiliza un registro en lugar de heredar de Mascota
class Veterinaria:

    def __init__(self, nombre):
        self.nombre = nombre
        self.registro = RegistroMascotas()
        self.archivos = ArchivoMascotas()

    def agregar_mascota(self, mascota):
        self.registro.agregar(mascota)

    def buscar_mascota(self, nombre):
        for mascota in self.registro.listar():
            if mascota.nombre.lower() == nombre.lower():
                return mascota

        raise MascotaNoEncontradaError(
            f"No se encontro una mascota llamada {nombre}"
        )

    def mostrar_mascotas(self):
        print(f"\nMascotas de {self.nombre}:")
        for mascota in self.registro.listar():
            print(mascota.describir())

    # Guardar los datos en JSON
    
    # Guardar mascotas utilizando la clase ArchivoMascotas
    def guardar_json(self, archivo):
        try:
            self.archivos.guardar(
                self.registro.listar(), archivo
            )
            print("Mascotas guardadas correctamente.")

        except OSError as error:
            print("Error al guardar:", error)

    # Recuperar mascotas desde un archivo JSON
    def leer_json(self, archivo):
        mascotas = self.archivos.leer(archivo)

        self.registro = RegistroMascotas()

        for mascota in mascotas:
            self.registro.agregar(mascota)

        return mascotas


# Funcion que se ejecutara en un hilo
def procesar_mascota(mascota):
    print(f"Procesando a {mascota.nombre}...")
    mascota.hacer_sonido()


# Programa principal
def main():

    # Crear las mascotas
    mascota1 = Perro("Luna", "Perro", 3, 12.5)
    mascota2 = Gato("Michi", "Gato", 2, 4.2)
    mascota3 = Perro("Rocky", "Perro", 5, 18.0)

    # Crear la veterinaria y registrar las mascotas
    veterinaria = Veterinaria("Amigos Peludos")
    veterinaria.agregar_mascota(mascota1)
    veterinaria.agregar_mascota(mascota2)
    veterinaria.agregar_mascota(mascota3)

    # Mostrar informacion
    veterinaria.mostrar_mascotas()

    # Demostrar polimorfismo
    print("\nSonidos de las mascotas:")
    for mascota in veterinaria.registro.listar():
        mascota.hacer_sonido()

    # Demostrar el uso de metodos
    mascota1.comer()
    mascota2.dormir()
    mascota3.jugar()

    # Demostrar comparacion
    mascota4 = Perro("Luna", "Perro", 3, 12.5)
    print("\n¿Son el mismo objeto?", mascota1 is mascota4)
    print("¿Son iguales por nombre?", mascota1 == mascota4)

    # Crear una mascota desde texto
    mascota5 = Mascota.desde_texto("Max,Perro,4,15.5")
    mascota5.mostrar()
    print("¿Max es adulta?", Mascota.es_adulta(
        mascota5.obtener_edad()
    ))

    # Demostrar excepcion personalizada
    try:
        mascota = veterinaria.buscar_mascota("Luna")
        print("\nMascota encontrada:", mascota.describir())

        veterinaria.buscar_mascota("Toby")

    except MascotaNoEncontradaError as error:
        print("Error:", error)

    # Guardar las mascotas en JSON
    veterinaria.guardar_json("mascotas.json")

    # Leer y reconstruir las mascotas
    try:
        recuperadas = veterinaria.leer_json("mascotas.json")

        print("\nMascotas recuperadas del archivo:")
        for mascota in recuperadas:
            print(mascota.describir())

    except (FileNotFoundError, ValueError) as error:
        print("Error al leer las mascotas:", error)

    # Demostrar concurrencia con dos hilos
    print("\nProcesamiento con hilos:")

    hilo1 = threading.Thread(
        target=procesar_mascota,
        args=(mascota1,)
    )

    hilo2 = threading.Thread(
        target=procesar_mascota,
        args=(mascota2,)
    )

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("Todas las tareas terminaron.")


if __name__ == "__main__":
    main()
