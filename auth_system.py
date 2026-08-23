import argparse
import hashlib
import os
import sqlite3
from pathlib import Path

# Configuración de la base de datos de usuarios
db_path = Path.cwd() / "secure_auth.db"

def inicializar_db():
    """Crea la tabla de usuarios seguros si no existe."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generar_hash_seguro(password: str, salt: bytes = None) -> tuple[str, str]:
    """
    Deriva una clave segura utilizando PBKDF2-HMAC-SHA256 con 100,000 iteraciones.
    Retorna el salt y el hash en formato hexadecimal.
    """
    if salt is None:
        salt = os.urandom(16)  # Genera un Salt criptográfico aleatorio de 16 bytes
        
    # Aplicamos PBKDF2 con 100,000 iteraciones para máxima seguridad defensiva
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )
    
    return salt.hex(), key.hex()

def registrar_usuario(username: str, password: str):
    """Registra un nuevo usuario aplicando Salting y PBKDF2 en la base de datos."""
    inicializar_db()
    
    if len(password) < 8:
        print("[ERROR DE SEGURIDAD] La contraseña debe tener al menos 8 caracteres.")
        return

    salt_hex, hash_hex = generar_hash_seguro(password)
    timestamp = os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip() # O datetime si prefieres

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, salt, password_hash, timestamp) VALUES (?, ?, ?, ?)",
            (username, salt_hex, hash_hex, str(timestamp))
        )
        conn.commit()
        conn.close()
        print(f"[REGISTRO EXITOSO] Usuario '{username}' registrado de forma segura con PBKDF2 (100k iteraciones).")
    except sqlite3.IntegrityError:
        print(f"[ERROR] El usuario '{username}' ya existe en el sistema.")
    except Exception as e:
        print(f"[ERROR DB] No se pudo completar el registro: {e}")

def autenticar_usuario(username: str, password: str):
    """Verifica las credenciales recalculando el hash con el salt almacenado."""
    inicializar_db()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT salt, password_hash FROM usuarios WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            print(f"[AUTENTICACIÓN FALLIDA] El usuario '{username}' no está registrado.")
            return

        salt_hex_almacenado, hash_almacenado = resultado
        salt_bytes = bytes.fromhex(salt_hex_almacenado)

        # Recalculamos el hash de la contraseña ingresada usando exactamente el mismo salt
        _, hash_intento = generar_hash_seguro(password, salt_bytes)

        # Verificación segura de hashes (contra ataques de temporización / timing attacks)
        if hmac_securcompare(hash_intento, hash_almacenado):
            print(f"\n[ACCESO CONCEDIDO] ¡Bienvenido, {username}! Las credenciales son auténticas.")
        else:
            print(f"\n[ACCESO DENEGADO] Contraseña incorrecta para el usuario '{username}'.")

    except Exception as e:
        print(f"[ERROR SISTEMA] Fallo en el proceso de autenticación: {e}")

def hmac_securcompare(val1: str, val2: str) -> bool:
    """Comparación segura para prevenir ataques de temporización."""
    import hmac
    return hmac.compare_digest(val1, val2)

def main():
    parser = argparse.ArgumentParser(description="Sistema de Autenticación Segura (PBKDF2 + Salting).")
    parser.add_argument("--accion", type=str, choices=["registrar", "login"], required=True, help="Acción a realizar.")
    parser.add_argument("--user", type=str, required=True, help="Nombre de usuario.")
    parser.add_argument("--pwd", type=str, required=True, help="Contraseña del usuario.")

    args = parser.parse_args()

    print("=== NÚCLEO DE AUTENTICACIÓN INDUSTRIAL ===")

    if args.accion == "registrar":
        registrar_usuario(args.user, args.pwd)
    elif args.accion == "login":
        autenticar_usuario(args.user, args.pwd)

if __name__ == "__main__":
    main()

