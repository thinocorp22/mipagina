from abc import ABC, abstractmethod

# 1. Interfaz base (Clase abstracta)
class TareaSistema(ABC):
    @abstractmethod
    def ejecutar(self):
        pass

# 2. Clases concretas que heredan de la interfaz
class TareaWeb(TareaSistema):
    def ejecutar(self):
        return "[Fábrica] Ejecutando despliegue de componentes web y frontend."

class TareaBackend(TareaSistema):
    def ejecutar(self):
        return "[Fábrica] Configurando endpoints de API y microservicios."

class TareaBaseDatos(TareaSistema):
    def ejecutar(self):
        return "[Fábrica] Verificando respaldos y tablas en la base de datos SQLite."

# 3. La Clase Fábrica (Factory)
class CreadorDeTareas:
    @staticmethod
    def crear_tarea(tipo):
        """
        Método estático que decide qué clase instanciar en base al parámetro recibido,
        centralizando la lógica de creación.
        """
        tipo_normalizado = tipo.lower()
        
        if tipo_normalizado == "web":
            return TareaWeb()
        elif tipo_normalizado == "backend":
            return TareaBackend()
        elif tipo_normalizado == "db":
            return TareaBaseDatos()
        else:
            raise ValueError(f"Tipo de tarea desconocido: '{tipo}'")

if __name__ == "__main__":
    print("=== PATRÓN DE DISEÑO FACTORY (FÁBRICA DE OBJETOS) ===")
    
    # Simulamos la creación dinámica de tareas solicitadas por el sistema o por el usuario
    tipos_solicitados = ["web", "backend", "db"]
    
    for tipo in tipos_solicitados:
        # Usamos la fábrica para obtener el objeto correcto sin preocuparnos por sus detalles internos
        tarea = CreadorDeTareas.crear_tarea(tipo)
        print(tarea.ejecutar())

