import math
from dataclasses import dataclass

@dataclass
class PuntoRuta:
    nombre: str
    lat: float
    lon: float

def calcular_distancia(p1: PuntoRuta, p2: PuntoRuta) -> float:
    """Calcula la distancia euclidiana o aproximada entre dos puntos geográficos."""
    return math.sqrt((p2.lat - p1.lat)**2 + (p2.lon - p1.lon)**2)

def optimizar_ruta_vecino_cercano(puntos: list[PuntoRuta], inicio: PuntoRuta) -> list[PuntoRuta]:
    """
    Algoritmo goloso (Greedy) del vecino más cercano para ordenar una ruta de entrega.
    """
    no_visitados = list(puntos)
    if inicio in no_visitados:
        no_visitados.remove(inicio)
        
    ruta_optimizada = [inicio]
    actual = inicio

    while no_visitados:
        # Encuentra el punto no visitado más cercano al punto actual
        siguiente = min(no_visitados, key=lambda p: calcular_distancia(actual, p))
        ruta_optimizada.append(siguiente)
        no_visitados.remove(siguiente)
        actual = siguiente

    return ruta_optimizada

def main():
    print("=== ALGORITMO DE OPTIMIZACIÓN DE RUTAS (LOGÍSTICA GPS) ===")
    
    # Definimos un conjunto de puntos de entrega simulados
    puntos_entrega = [
        PuntoRuta("Almacén Central", 31.6904, -106.4245),
        PuntoRuta("Sucursal Norte", 31.7400, -106.4500),
        PuntoRuta("Cliente Industrial", 31.6100, -106.3500),
        PuntoRuta("Punto Zona Este", 31.6800, -106.3100)
    ]

    punto_partida = puntos_entrega[0]  # El Almacén Central

    print(f"\nPuntos iniciales desordenados:")
    for p in puntos_entrega:
        print(f" - {p.nombre} ({p.lat}, {p.lon})")

    # Ejecutamos el algoritmo
    ruta_final = optimizar_ruta_vecino_cercano(puntos_entrega, punto_partida)

    print(f"\n--- RUTA ÓRDENADA DE REPARTO SUGERIDA ---")
    for i, p in enumerate(ruta_final, 1):
        print(f"{i}. {p.nombre} -> Coordenadas: [{p.lat}, {p.lon}]")

if __name__ == "__main__":
    main()

