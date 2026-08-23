from flask import Flask, jsonify

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Ruta principal (Home)
@app.route('/')
def home():
    return "¡Bienvenido a la API oficial de El Rincón de las Esquinas! Servidor móvil activo."

# Endpoint de API que devuelve datos en formato JSON
@app.route('/api/proyectos', methods=['GET'])
def obtener_proyectos():
    proyectos_data = [
        {"id": 1, "nombre": "El Rincón de las Esquinas", "estado": "Activo", "tipo": "Web y Comunidad"},
        {"id": 2, "nombre": "Servidor Móvil Termux", "estado": "Configurado", "tipo": "Infraestructura Linux"},
        {"id": 3, "nombre": "Automatización con Python", "estado": "Completado", "tipo": "Backend"}
    ]
    
    # jsonify convierte automáticamente diccionarios de Python en respuestas JSON válidas
    return jsonify({
        "status": "success",
        "total_proyectos": len(proyectos_data),
        "proyectos": proyectos_data
    })

if __name__ == '__main__':
    # Ejecutamos el servidor localmente en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

