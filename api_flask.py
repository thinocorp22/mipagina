from flask import Flask, jsonify, request
import string
import secrets
import math
import hashlib

app = Flask(__name__)

@app.route("/", methods=["GET"])
def leer_raiz():
    return jsonify({
        "estado": "activo",
        "mensaje": "Bienvenido al servidor backend con Flask en Termux",
        "endpoints": ["/api/auditar-password", "/api/generar-password"]
    })

@app.route("/api/auditar-password", methods=["POST"])
def auditar_password():
    data = request.get_json() or {}
    pwd = data.get("password", "")
    
    if not pwd:
        return jsonify({"error": "La contraseña no puede estar vacía."}), 400

    # Lógica de entropía
    pool_size = 0
    if any(c.islower() for c in pwd): pool_size += 26
    if any(c.isupper() for c in pwd): pool_size += 26
    if any(c.isdigit() for c in pwd): pool_size += 10
    if any(c in string.punctuation for c in pwd): pool_size += len(string.punctuation)

    entropia = round(len(pwd) * math.log2(pool_size), 2) if pool_size > 0 else 0.0

    if entropia < 28:
        nivel = "MUY DÉBIL"
    elif 28 <= entropia < 36:
        nivel = "DÉBIL"
    elif 36 <= entropia < 60:
        nivel = "MODERADA"
    elif 60 <= entropia < 128:
        nivel = "FUERTE"
    else:
        nivel = "EXTREMADAMENTE FUERTE"

    hash_sha256 = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    return jsonify({
        "longitud": len(pwd),
        "entropia_bits": entropia,
        "veredicto": nivel,
        "hash_sha256": hash_sha256
    })

@app.route("/api/generar-password", methods=["POST"])
def generar_password():
    data = request.get_json() or {}
    longitud = data.get("longitud", 16)
    
    if longitud < 8:
        return jsonify({"error": "La longitud mínima recomendada es de 8 caracteres."}), 400
    
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    password_segura = ''.join(secrets.choice(alfabeto) for _ in range(longitud))
    
    return jsonify({
        "longitud": longitud,
        "password_generada": password_segura
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

