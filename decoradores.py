import time
from functools import wraps

def medir_tiempo(func):
    """
    Un decorador que envuelve una función para medir cuánto tiempo tarda en ejecutarse.
    """
    @wraps(func)
    def envuelta(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        duracion = fin - inicio
        print(f"[Monitoreo] La función '{func.__name__}' tardó {duracion:.4f} segundos en ejecutarse.")
        return resultado
    return envuelta

# Aplicamos el decorador usando la sintaxis de arroba (@)
@medir_tiempo
def simular_proceso_pesado(segundos):
    print(f"Ejecutando proceso complejo por {segundos} segundos...")
    time.sleep(segundos)
    print("¡Proceso finalizado!")
    return "Éxito"

if __name__ == "__main__":
    print("=== USO DE DECORADORES AVANZADOS ===")
    
    # Llamamos a la función decorada de manera normal
    respuesta = simular_proceso_pesado(2)
    print(f"Resultado devuelto: {respuesta}")

