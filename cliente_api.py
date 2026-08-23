import requests

def consumir_api_local():
    # URL del endpoint que creamos con Flask
    url = "http://localhost:5000/api/proyectos"
    
    print("Conectando con tu servidor Flask local...")
    
    try:
        respuesta = requests.get(url)
        
        # Verificamos si la petición fue exitosa (Código HTTP 200)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            print(f"\n[Éxito] Conexión establecida con la API.")
            print(f"Estado del servidor: {datos.get('status')}")
            print(f"Total de proyectos registrados: {datos.get('total_proyectos')}\n")
            
            print("--- LISTADO EXTRAÍDO DE LA API ---")
            for proyecto in datos.get('proyectos', []):
                print(f"ID: {proyecto['id']} | Nombre: {proyecto['nombre']} | Tipo: {proyecto['tipo']} | Estado: {proyecto['estado']}")
            print("-----------------------------------")
        else:
            print(f"Error en la respuesta del servidor. Código: {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[Error de Conexión] No se pudo conectar al servidor. ¿Aseguraste de dejar corriendo 'mi_api.py' en otra terminal?")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    consumir_api_local()

