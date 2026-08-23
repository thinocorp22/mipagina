import argparse
import math
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sqlite3

# 1. CONFIGURACIÓN DE LA BASE DE DATOS DE RASTREO Y ALERTAS
db_path = Path.cwd() / "gps_routes.db"

def inicializar_db():
    """Crea las tablas para coordenadas y alertas si no existen."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coordenadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo TEXT,
            latitud REAL,
            longitud REAL,
            altitud REAL,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo TEXT,
            tipo_alerta TEXT,
            mensaje TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# 2. ESTRUCTURA DE DATOS GPS
@dataclass
class CoordenadaGPS:
    dispositivo: str
    latitud: float
    longitud: float
    altitud: float
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def resumen(self):
        return f"[{self.timestamp}] Dispositivo: {self.dispositivo} -> Lat: {self.latitud}, Lon: {self.longitud}, Alt: {self.altitud}m"


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos puntos GPS."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


# 3. MOTOR DE ALERTAS AUTOMATIZADAS
def registrar_alerta(dispositivo: str, tipo: str, mensaje: str):
    """Inserta una alerta crítica en la base de datos y la muestra en pantalla."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alertas (dispositivo, tipo_alerta, mensaje, timestamp) VALUES (?, ?, ?, ?)",
            (dispositivo, tipo, mensaje, ahora)
        )
        conn.commit()
        conn.close()
        print(f"\n🚨 [ALERTA DEL SISTEMA - {tipo.upper()}] -> {mensaje} (Hora: {ahora})")
    except Exception as e:
        print(f"[ERROR ALERTA] No se pudo registrar la alerta: {e}")


def evaluar_alertas(coord: CoordenadaGPS):
    """Evalúa reglas de negocio para disparar alertas automáticas."""
    # Regla 1: Alerta por altitud excesiva (Ej: zona montañosa peligrosa > 2500 metros)
    if coord.altitud > 2500.0:
        registrar_alerta(
            coord.dispositivo,
            "ALTITUD CRÍTICA",
            f"El dispositivo superó el límite seguro de altitud ({coord.altitud}m)."
        )

    # Regla 2: Análisis de salto masivo respecto al último punto
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT latitud, longitud FROM coordenadas WHERE dispositivo = ? ORDER BY id DESC LIMIT 1", (coord.dispositivo,))
        ultimo = cursor.fetchone()
        conn.close()

        if ultimo:
            lat_ant, lon_ant = ultimo
            distancia = calcular_distancia_haversine(lat_ant, lon_ant, coord.latitud, coord.longitud)
            
            if distancia > 300.0:
                registrar_alerta(
                    coord.dispositivo,
                    "MOVIMIENTO ANÓMALO",
                    f"Salto de distancia imprevisto detectado: {distancia:.2f} km."
                )
    except Exception as e:
        print(f"[ERROR] Evaluación de telemetría fallida: {e}")


# 4. EXPORTACIÓN GEOJSON
def exportar_geojson(dispositivo: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT latitud, longitud, altitud, timestamp FROM coordenadas WHERE dispositivo = ?", (dispositivo,))
        filas = cursor.fetchall()
        conn.close()

        if not filas:
            print("[EXPORTAR] No hay datos para exportar.")
            return

        features = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [f[1], f[0], f[2]]}, "properties": {"timestamp": f[3]}} for f in filas]
        geojson_data = {"type": "FeatureCollection", "features": features}

        output_path = Path.cwd() / f"ruta_{dispositivo}.geojson"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, indent=4)

        print(f"[ÉXITO] Archivo GeoJSON generado en: {output_path}")
    except Exception as e:
        print(f"[ERROR] Falló exportación: {e}")


def guardar_coordenada(coord: CoordenadaGPS):
    """Guarda la posición y dispara el motor de evaluación de alertas."""
    try:
        # Primero evaluamos si rompe alguna regla antes o durante el registro
        evaluar_alertas(coord)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO coordenadas (dispositivo, latitud, longitud, altitud, timestamp) VALUES (?, ?, ?, ?, ?)",
            (coord.dispositivo, coord.latitud, coord.longitud, coord.altitud, coord.timestamp)
        )
        conn.commit()
        conn.close()
        print(f"[GPS-DB] Coordenada almacenada correctamente.")
    except Exception as e:
        print(f"[ERROR DB]: {e}")


# 5. INTERFAZ CLI
def main():
    inicializar_db()

    parser = argparse.ArgumentParser(description="Software GPS con Motor de Alertas Automatizadas.")
    parser.add_argument("--accion", type=str, choices=["registrar", "historial", "alertas", "exportar"], required=True)
    parser.add_argument("--dispositivo", type=str, default="Tracker-Mobil-01")
    parser.add_argument("--lat", type=float, default=31.6904)
    parser.add_argument("--lon", type=float, default=-106.4245)
    parser.add_argument("--alt", type=float, default=1120.0)

    args = parser.parse_args()

    print("=== NÚCLEO DE GPS CON MOTOR DE ALERTAS ===")

    if args.accion == "registrar":
        nueva_pos = CoordenadaGPS(
            dispositivo=args.dispositivo,
            latitud=args.lat,
            longitud=args.lon,
            altitud=args.alt
        )
        print(nueva_pos.resumen())
        guardar_coordenada(nueva_pos)

    elif args.accion == "historial":
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, dispositivo, latitud, longitud, altitud FROM coordenadas ORDER BY id DESC LIMIT 5")
        filas = cursor.fetchall()
        conn.close()
        print("\n=== HISTORIAL DE RASTREO ===")
        for f in (filas or []):
            print(f"[{f[0]}] {f[1]} -> Lat: {f[2]}, Lon: {f[3]}, Alt: {f[4]}m")

    elif args.accion == "alertas":
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, dispositivo, tipo_alerta, mensaje FROM alertas ORDER BY id DESC LIMIT 5")
        filas = cursor.fetchall()
        conn.close()
        print("\n=== HISTORIAL DE ALERTAS REGISTRADAS ===")
        if not filas:
            print("No hay alertas registradas en el sistema.")
            return
        for f in filas:
            print(f"[{f[0]}] [{f[2]}] Dispositivo: {f[1]} -> {f[3]}")

    elif args.accion == "exportar":
        exportar_geojson(args.dispositivo)

if __name__ == "__main__":
    main()

