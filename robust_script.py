import sys
from pathlib import Path

def analizar_archivo_proyecto(nombre_archivo):
    ruta_archivo = Path.cwd() / nombre_archivo
    
    print(f"\nIntentando analizar el archivo: {nombre_archivo}")
    
    try:
        # Intentamos abrir el archivo en modo lectura
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            lineas = contenido.splitlines()
            print(f"[Éxito] Archivo leído correctamente. Total de líneas: {len(lineas)}")
            
    except FileNotFoundError:
        # Error específico si el archivo no existe
        print(f"[Error controlado] El archivo '{nombre_archivo}' no existe en este directorio.")
        print("Sugerencia: Crea el archivo o verifica el nombre antes de ejecutar.")
        
    except PermissionError:
        # Error si no tenemos permisos de lectura
        print(f"[Error de Permisos] No tienes autorización para leer el archivo '{nombre_archivo}'.")
        
    else:
        # Se ejecuta SOLAMENTE si todo salió bien (sin excepciones)
        print("[Info] El bloque 'else' confirma que la operación principal fue impecable.")
        
    finally:
        # Se ejecuta SIEMPRE, haya error o no (ideal para cerrar conexiones o limpiar recursos)
        print("[Sistema] Finalizó el intento de lectura del archivo.\n")

if __name__ == "__main__":
    # Probaremos con un archivo que existe (index.html) y uno que no (fantasma.txt)
    analizar_archivo_proyecto("index.html")
    analizar_archivo_proyecto("fantasma.txt")

