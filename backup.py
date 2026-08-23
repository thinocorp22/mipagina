import os
import shutil
from datetime import datetime
from pathlib import Path

def realizar_backup():
    # Directorio origen (tu carpeta actual)
    origen = Path.cwd()
    
    # Crear carpeta de respaldos si no existe
    backup_dir = Path.home() / "backups_proyectos"
    backup_dir.mkdir(exist_ok=True)
    
    # Generar un nombre único basado en la fecha y hora actual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"backup_mipagina_{timestamp}"
    
    ruta_destino = backup_dir / nombre_archivo
    
    print(f"Iniciando respaldo de los archivos desde: {origen}")
    
    try:
        # Creamos un archivo comprimido tipo zip con el contenido del proyecto
        archivo_final = shutil.make_archive(str(ruta_destino), 'zip', str(origen))
        print(f"\n[Éxito] Respaldo creado correctamente.")
        print(f"Ubicación: {archivo_final}")
    except Exception as e:
        print(f"[Error] No se pudo completar el respaldo: {e}")

if __name__ == "__main__":
    realizar_backup()

