from dataclasses import dataclass
from datetime import datetime

# Definimos una clase de datos para tipar y estructurar la información de un proyecto
@dataclass
class ProyectoModel:
    id: int
    nombre: str
    tipo: str
    estado: str
    fecha_creacion: str = datetime.now().strftime("%Y-%m-%d")

    def resumen(self):
        return f"[{self.id}] {self.nombre} ({self.tipo}) - Estado: {self.estado} [Creado: {self.fecha_creacion}]"


if __name__ == "__main__":
    print("=== GESTIÓN DE DATOS CON DATACLASSES ===")
    
    # Creamos instancias limpias y estructuradas sin necesidad de escribir constructores largos (__init__)
    p1 = ProyectoModel(id=1, nombre="El Rincón de las Esquinas", tipo="Web y Comunidad", estado="Activo")
    p2 = ProyectoModel(id=2, nombre="Servidor Móvil Termux", tipo="Infraestructura", estado="Configurado")
    
    # Imprimimos los resúmenes usando los métodos de la clase de datos
    print(p1.resumen())
    print(p2.resumen())

