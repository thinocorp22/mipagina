import asyncio
import time

async def simular_consulta_servidor(id_tarea, retraso):
    print(f"[Inicio] Consultando servidor externo {id_tarea}...")
    # Simulamos una espera de red de forma asíncrona (sin bloquear el sistema)
    await asyncio.sleep(retraso)
    print(f"[Completado] Respuesta recibida del servidor {id_tarea} tras {retraso} segundos.")
    return f"Datos_Servidor_{id_tarea}"

async def main():
    print("=== INICIANDO OPERACIONES ASÍNCRONAS (ASYNC/AWAIT) ===")
    inicio_tiempo = time.time()
    
    # Lanzamos múltiples tareas concurrentes para que se ejecuten en paralelo lógico
    tarea1 = asyncio.create_task(simular_consulta_servidor(1, 2))
    tarea2 = asyncio.create_task(simular_consulta_servidor(2, 3))
    tarea3 = asyncio.create_task(simular_consulta_servidor(3, 1))
    
    # Esperamos a que todas terminen
    resultados = await asyncio.gather(tarea1, tarea2, tarea3)
    
    fin_tiempo = time.time()
    print(f"\n[Éxito] Todas las tareas asíncronas finalizaron.")
    print(f"Resultados obtenidos: {resultados}")
    print(f"Tiempo total de ejecución concurrente: {fin_tiempo - inicio_tiempo:.2f} segundos.")

if __name__ == "__main__":
    # Ejecutamos el bucle de eventos asíncrono
    asyncio.run(main())

