class ProyectoWeb:
    # Constructor: inicializa los atributos del objeto
    def __init__(self, nombre, categoria, estado="En desarrollo"):
        self.nombre = nombre
        self.categoria = categoria
        self.estado = estado

    # Método para mostrar la información del proyecto
    def mostrar_detalles(self):
        print(f"Proyecto: {self.nombre} | Categoría: {self.categoria} | Estado: {self.estado}")

    # Método para actualizar el estado del proyecto
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f"[Actualización] El proyecto '{self.nombre}' ahora está: {self.estado}")


# Clase Administrador que hereda o agrupa lógica (Gestión de una colección de proyectos)
class Portafolio:
    def __init__(self):
        self.proyectos = []

    def agregar_proyecto(self, proyecto):
        self.proyectos.append(proyecto)
        print(f"-> Añadido al portafolio: {proyecto.nombre}")

    def listar_proyectos(self):
        print("\n=== PORTAFOLIO DE PROYECTOS (POO) ===")
        for p in self.proyectos:
            p.mostrar_detalles()
        print("=====================================\n")


if __name__ == "__main__":
    # Instanciamos (creamos) objetos basados en nuestras clases
    mi_portafolio = Portafolio()

    # Creamos proyectos individuales
    p1 = ProyectoWeb("El Rincón de las Esquinas", "Comunidad Web", "Activo")
    p2 = ProyectoWeb("Servidor Móvil Termux", "Infraestructura", "Configurado")

    # Los agregamos a nuestro portafolio administrado por objetos
    mi_portafolio.agregar_proyecto(p1)
    mi_portafolio.agregar_proyecto(p2)

    # Listamos todos los proyectos usando métodos orientados a objetos
    mi_portafolio.listar_proyectos()

    # Modificamos el estado de un objeto de forma independiente
    p1.actualizar_estado("Actualización masiva completada")
    p1.mostrar_detalles()

