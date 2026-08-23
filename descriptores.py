class TareaProyecto:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.prioridad = prioridad  # Utiliza el setter definido abajo

    # Getter: Permite leer el atributo protegido de forma controlada
    @property
    def prioridad(self):
        return self._prioridad

    # Setter: Valida automáticamente los datos antes de asignarlos al objeto
    @prioridad.setter
    def prioridad(self, valor):
        if not isinstance(valor, int):
            raise TypeError("La prioridad debe ser un número entero.")
        if valor < 1 or valor > 5:
            raise ValueError("La prioridad debe estar en un rango del 1 al 5.")
        
        print(f"[Validación] Prioridad '{valor}' aceptada correctamente.")
        self._prioridad = valor

if __name__ == "__main__":
    print("=== CONTROL DE ATRIBUTOS CON PROPIEDADES (GETTER/SETTER) ===")
    
    try:
        # Creamos una tarea con prioridad válida
        tarea = TareaProyecto("Desplegar Servidor", 3)
        print(f"Tarea creada: {tarea.nombre} con prioridad {tarea.prioridad}")
        
        print("\nIntentando asignar una prioridad inválida (fuera de rango)...")
        # Esto disparará el error controlado del setter
        tarea.prioridad = 10 
        
    except ValueError as e:
        print(f"[Error Controlado Capturado]: {e}")

