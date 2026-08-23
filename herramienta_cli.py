import argparse

def main():
    # Configuramos el analizador de argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Herramienta CLI profesional para gestión de tareas y proyectos.")
    
    # Añadimos argumentos obligatorios y opcionales
    parser.add_argument("--nombre", type=str, required=True, help="Nombre de la tarea o proyecto.")
    parser.add_argument("--estado", type=str, default="En desarrollo", help="Estado actual del proyecto.")
    parser.add_argument("--prioridad", type=int, default=1, help="Nivel de prioridad (ej. 1, 2, 3).")

    # Analizamos los argumentos recibidos
    args = parser.parse_args()

    print("=== EJECUCIÓN DE HERRAMIENTA CLI ===")
    print(f"-> Proyecto recibido: {args.nombre}")
    print(f"-> Estado configurado: {args.estado}")
    print(f"-> Nivel de prioridad: {args.prioridad}")
    print("[Éxito] Argumentos procesados correctamente desde la terminal.")

if __name__ == "__main__":
    main()

