import logging
from pathlib import Path

# Configuramos el sistema de logs para que guarde en un archivo llamado 'sistema.log'
# y también muestre los mensajes importantes en la consola.
log_path = Path.cwd() / "sistema.log"

logging.basicConfig(
    level=logging.INFO, # Nivel mínimo a registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'), # Guarda en archivo
        logging.StreamHandler()                          # Muestra en pantalla
    ]
)

logger = logging.getLogger("ServidorMovil")

def realizar_operaciones_criticas():
    logger.info("Iniciando secuencia de operaciones del sistema...")
    
    # Simulamos una advertencia
    logger.warning("El espacio de almacenamiento local en el servidor móvil está al 80%.")
    
    try:
        # Simulamos una operación que podría fallar
        logger.info("Intentando conectar con la base de datos local...")
        resultado = 10 / 2 # Operación exitosa
        logger.info(f"Conexión y cálculo exitoso. Resultado: {resultado}")
        
    except ZeroDivisionError as e:
        logger.error(f"Fallo crítico en la operación matemática: {e}")

if __name__ == "__main__":
    print("=== REGISTRO DE EVENTOS (LOGGING) ===")
    realizar_operaciones_criticas()
    print(f"\n[Info] Los registros se han guardado automáticamente en: {log_path}")

