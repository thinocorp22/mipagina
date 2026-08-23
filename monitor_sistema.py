import time
from datetime import datetime
from pathlib import Path

def iniciar_monitoreo():
    print("=== INICIANDO SERVICIO DE MONITOREO AUTOMÁTICO ===")
    print("Presiona Ctrl + C en cualquier momento para detener el servicio.\n")
    
    contador_ciclos = 1
    
    try:
        while True:
            # Obtenemos la marca de tiempo actual
            tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Verificamos si existe nuestra base de datos o carpeta de proyectos
            db_path = Path.home() / "mis_proyectos.db"
            estado_db = "Disponible" if db_path.exists() else "No encontrada"
            
            print(f"[Ciclo {contador_ciclos}] - {tiempo_actual}")
            print(f" -> Estado de la base de datos local: {estado_db}")
            print(f" -> Directorio actual analizado: {Path.cwd()}")
            print("-" * 50)
            
            # Incrementamos el contador
            contador_ciclos += 1
            
            # Esperamos 5 segundos antes del siguiente ciclo (en producción puedes poner horas o minutos)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[Sistema] Servicio de monitoreo detenido de forma segura por el usuario.")

if __name__ == "__main__":
    iniciar_monitoreo()

