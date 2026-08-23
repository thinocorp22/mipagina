import time
from functools import wraps

def memoize_con_cache(func):
    """
    Un decorador proxy que actúa como caché. Almacena en un diccionario los resultados
    de operaciones pesadas para devolverlos instantáneamente si los parámetros se repiten.
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        # Si los argumentos ya fueron calculados, los devolvemos de la caché
        if args in cache:
            print(f"[Proxy Caché] ¡Acierto! Recuperando resultado guardado para: {args}")
            return cache[args]
        
        # Si no están en caché, ejecutamos la función real y guardamos el resultado
        print(f"[Proxy Caché] Calculando resultado por primera vez para: {args}...")
        resultado = func(*args)
        cache[args] = resultado
        return resultado
        
    return wrapper

@memoize_con_cache
def operacion_pesada_simulada(id_recurso):
    # Simulamos una consulta pesada a base de datos o API externa que tarda 2 segundos
    time.sleep(2)
    return f"Datos del recurso {id_recurso} procesados correctamente."

if __name__ == "__main__":
    print("=== PATRÓN PROXY Y MEMORIZACIÓN (CACHING) ===")
    
    # Primera llamada (deberá calcular y tardar 2 segundos)
    inicio = time.time()
    print(operacion_pesada_simulada(101))
    print(f"Tiempo transcurrido: {time.time() - inicio:.2f} segundos.\n")
    
    # Segunda llamada con el mismo parámetro (deberá ser instantánea gracias al proxy caché)
    inicio = time.time()
    print(operacion_pesada_simulada(101))
    print(f"Tiempo transcurrido: {time.time() - inicio:.2f} segundos.\n")
    
    # Tercera llamada con un parámetro diferente (calcula de nuevo)
    inicio = time.time()
    print(operacion_pesada_simulada(202))
    print(f"Tiempo transcurrido: {time.time() - inicio:.2f} segundos.")

