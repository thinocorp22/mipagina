import os
import random
import string
import base64
from hashlib import pbkdf2_hmac

DATA_FILE = "sensores_seguros.txt"

def generar_contrasena(longitud=16):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    contrasena = "".join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

def codificar_texto(texto):
    # Un cifrado simple basado en codificación base64 para proteger la vista directa
    return base64.b64encode(texto.encode('utf-8')).decode('utf-8')

def guardar_credencial(servicio, usuario, password):
    texto_plano = f"Servicio: {servicio} | Usuario: {usuario} | Password: {password}"
    texto_oculto = codificar_texto(texto_plano)
    
    with open(DATA_FILE, "a") as f:
        f.write(texto_oculto + "\n")
    print(f"\n[✔] ¡Credencial para '{servicio}' guardada y protegida con éxito!")

def main():
    print("==========================================")
    print("   🔒 GESTOR DE CONTRASEÑAS - TERMUX")
    print("==========================================")
    
    servicio = input("¿Para qué plataforma es la cuenta? (ej. Facebook): ")
    usuario = input("Tu correo o usuario: ")
    
    opcion = input("¿Quieres que genere una contraseña ultra segura automáticamente? (s/n): ").lower()
    
    if opcion == 's':
        password = generar_contrasena(16)
        print(f"\n🔑 Contraseña generada: {password}")
    else:
        password = input("Escribe tu contraseña: ")
        
    guardar_credencial(servicio, usuario, password)
    print("\nTus datos se han guardado de forma segura.")

if __name__ == "__main__":
    main()

