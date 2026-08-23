def generar_logs_simulados(cantidad):
    """
    Una función generadora utiliza 'yield' en lugar de 'return'.
    Esto produce un valor a la vez y pausa la ejecución, ahorrando memoria RAM.
    """
    for i in range(1, cantidad + 1):
        # Simulamos la creación de un registro de evento bajo demanda
        yield f"Registro ID-{i}: Evento procesado correctamente en el servidor móvil."

if __name__ == "__main__":
    print("=== PROCESAMIENTO EFICIENTE CON GENERADORES (YIELD) ===")
    
    # Supongamos que necesitamos procesar 1 millón de registros (aquí usaremos 5 para el ejemplo)
    total_registros = 5
    
    print(f"Iniciando flujo de {total_registros} registros usando un generador:\n")
    
    # Consumimos el generador bucle por bucle sin saturar la memoria
    for log in generar_logs_simulados(total_registros):
        print(f"[Procesando] -> {log}")
        
    print("\n[Éxito] Todos los registros fueron procesados eficientemente sin cargar listas pesadas en RAM.")

