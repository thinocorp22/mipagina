from functools import reduce

def procesar_datos_funcionales():
    # Lista de proyectos con sus horas de desarrollo estimadas
    proyectos = [
        {"nombre": "El Rincón de las Esquinas", "horas": 45, "activo": True},
        {"nombre": "Servidor Móvil Termux", "horas": 20, "activo": True},
        {"nombre": "Script de Respaldos", "horas": 5, "activo": False},
        {"nombre": "API de Gestión", "horas": 30, "activo": True}
    ]

    print("=== PROGRAMACIÓN FUNCIONAL EN PYTHON ===")
    
    # 1. FILTER: Filtramos únicamente los proyectos activos
    proyectos_activos = list(filter(lambda p: p["activo"], proyectos))
    print(f"\n[Filter] Proyectos activos encontrados: {len(proyectos_activos)}")
    for p in proyectos_activos:
        print(f" -> {p['nombre']}")

    # 2. MAP: Transformamos los datos para extraer solo los nombres en mayúsculas
    nombres_mayus = list(map(lambda p: p["nombre"].upper(), proyectos_activos))
    print(f"\n[Map] Nombres transformados: {nombres_mayus}")

    # 3. REDUCE: Acumulamos el total de horas invertidas en los proyectos activos
    total_horas = reduce(lambda acumulador, p: acumulador + p["horas"], proyectos_activos, 0)
    print(f"\n[Reduce] Total de horas en proyectos activos: {total_horas} hrs")

if __name__ == "__main__":
    procesar_datos_funcionales()

