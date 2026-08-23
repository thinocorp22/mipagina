import threading
import time
import queue
import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Configuración de Rutas y Base de Datos Global
db_path = Path.cwd() / "enterprise_telemetry.db"
event_queue = queue.Queue()

def inicializar_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            lat REAL,
            lon REAL,
            alt REAL,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

@dataclass
class TelemetryEvent:
    device_id: str
    lat: float
    lon: float
    alt: float
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =====================================================================
# 1. EVENT BROKER & WORKERS (Arquitectura Orientada a Eventos)
# =====================================================================
def database_worker(q: queue.Queue):
    """Worker independiente que consume eventos de la cola y realiza escritura batch/asíncrona en SQLite."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    while True:
        event: TelemetryEvent = q.get()
        if event is None: # Señal de cierre
            break
        try:
            status = "CRITICAL_ALTITUDE" if event.alt > 2500 else "NORMAL"
            cursor.execute(
                "INSERT INTO telemetry_stream (device_id, lat, lon, alt, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (event.device_id, event.lat, event.lon, event.alt, status, event.timestamp)
            )
            conn.commit()
            print(f"[DB-WORKER] Evento procesado y persistido para: {event.device_id} [Estado: {status}]")
        except Exception as e:
            print(f"[ERROR DB-WORKER]: {e}")
        finally:
            q.task_done()
    
    conn.close()

# =====================================================================
# 2. SIMULADOR DE DISPOSITIVOS CONCURRENTES (Hilos / Threads)
# =====================================================================
def simular_dispositivo(device_id: str, q: queue.Queue, iteraciones: int = 3):
    """Simula un dispositivo IoT enviando paquetes de telemetría de forma concurrente."""
    print(f"[INIT THREAD] Dispositivo {device_id} conectado y transmitiendo...")
    for _ in range(iteraciones):
        lat = 31.0 + random.uniform(-0.5, 0.5)
        lon = -106.0 + random.uniform(-0.5, 0.5)
        alt = random.uniform(1100.0, 2700.0) # Algunos superarán el límite crítico
        
        evento = TelemetryEvent(device_id=device_id, lat=lat, lon=lon, alt=alt)
        q.put(evento) # Inyecta el evento al bus asíncrono
        
        time.sleep(1.0) # Simula latencia de red entre paquetes
    print(f"[EXIT THREAD] Dispositivo {device_id} finalizó su transmisión.")

# =====================================================================
# 3. NÚCLEO DE ORQUESTACIÓN DISTRIBUIDA
# =====================================================================
def main():
    inicializar_db()
    print("=== INICIANDO MOTOR DE TELEMETRÍA CONCURRENTE (EDA) ===")

    # Lanzamos el Worker de Base de Datos en un hilo secundario dedicado
    db_thread = threading.Thread(target=database_worker, args=(event_queue,))
    db_thread.daemon = True
    db_thread.start()

    # Simulamos una flotilla de múltiples dispositivos enviando datos AL MISMO TIEMPO (Hilos paralelos)
    dispositivos_ids = ["FLOTILLA-ALPHA-01", "FLOTILLA-BETA-02", "UNIDAD-LOGISTICA-03"]
    hilos = []

    inicio = time.time()
    for dev_id in dispositivos_ids:
        t = threading.Thread(target=simular_dispositivo, args=(dev_id, event_queue, 3))
        hilos.append(t)
        t.start()

    # Esperamos a que todos los dispositivos terminen de transmitir
    for t in hilos:
        t.join()

    # Esperamos a que la cola vacíe todos los eventos pendientes hacia la base de datos
    event_queue.join()
    
    # Señalizamos el cierre del worker de BD
    event_queue.put(None)
    db_thread.join()

    fin = time.time()
    print(f"\n[ÉXITO TOTAL] Procesamiento concurrente completado en {fin - inicio:.4f} segundos.")
    print("Los datos masivos han sido desacoplados, encolados y persistidos de manera segura.")

if __name__ == "__main__":
    main()

