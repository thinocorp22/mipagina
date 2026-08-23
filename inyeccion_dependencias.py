from abc import ABC, abstractmethod

# 1. Definimos la interfaz (Contrato) para el servicio de almacenamiento
class RepositorioDatos(ABC):
    @abstractmethod
    def guardar(self, dato: str):
        pass

# 2. Implementaciones concretas del servicio
class RepositorioSQLite(RepositorioDatos):
    def guardar(self, dato: str):
        return f"[Base de Datos SQLite] Guardando permanentemente: '{dato}'"

class RepositorioMemoria(RepositorioDatos):
    def guardar(self, dato: str):
        return f"[Memoria RAM Temporal] Almacenando de forma volátil: '{dato}'"

# 3. La clase principal que recibe su dependencia por parámetro (Inyección)
class GestorProyectos:
    def __init__(self, repositorio: RepositorioDatos):
        # Inyectamos la dependencia a través del constructor
        self.repositorio = repositorio

    def registrar_nuevo_proyecto(self, nombre_proyecto: str):
        print(f"[Gestor] Procesando alta del proyecto: {nombre_proyecto}")
        # Usamos el repositorio inyectado sin importar si es SQLite o Memoria
        resultado = self.repositorio.guardar(nombre_proyecto)
        print(resultado)

if __name__ == "__main__":
    print("=== INYECCIÓN DE DEPENDENCIAS ===")
    
    # Caso A: Inyectamos el repositorio de SQLite
    print("\n--- Estrategia 1: Usando Base de Datos SQLite ---")
    db_sqlite = RepositorioSQLite()
    gestor_con_db = GestorProyectos(repositorio=db_sqlite)
    gestor_con_db.registrar_nuevo_proyecto("El Rincón de las Esquinas v2")

    # Caso B: Inyectamos el repositorio en memoria (ideal para pruebas rápidas)
    print("\n--- Estrategia 2: Usando Almacenamiento en Memoria ---")
    db_memoria = RepositorioMemoria()
    gestor_en_memoria = GestorProyectos(repositorio=db_memoria)
    gestor_en_memoria.registrar_nuevo_proyecto("Módulo de Pruebas Temporales")

