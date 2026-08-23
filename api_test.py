import requests

def consultar_api():
    # Usaremos una API pública de datos aleatorios o clima/hechos
    url = "https://api.chucknorris.io/jokes/random"
    
    print("Consultando API externa desde tu servidor móvil...")
    
    try:
        response = requests.get(url)
        
        # Verificamos si la petición fue exitosa (código 200)
        if response.status_code == 200:
            data = response.json()
            print("\n ¡Petición exitosa!")
            print(f"Categoría: {data.get('category', ['General'])[0]}")
            print(f"Dato/Mensaje obtenido: {data['value']}")
        else:
            print(f"Error en la petición. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"Ocurrió un error de red: {e}")

if __name__ == "__main__":
    consultar_api()

