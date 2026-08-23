import argparse
import math
import string
import secrets
import hashlib

def calcular_entropia(password: str) -> float:
    """
    Calcula la entropía de una contraseña en bits.
    La entropía mide la imprevisibilidad basándose en el tamaño del conjunto de caracteres (pool).
    """
    if not password:
        return 0.0

    pool_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_symbol: pool_size += len(string.punctuation)

    # Fórmula de entropía: L * log2(R)
    if pool_size == 0:
        return 0.0
    
    entropia = len(password) * math.log2(pool_size)
    return round(entropia, 2)

def auditar_password(password: str):
    """Analiza la fortaleza de una contraseña y emite un veredicto de seguridad."""
    print(f"\n--- AUDITORÍA DE SEGURIDAD PARA: '{password}' ---")
    
    longitud = len(password)
    entropia = calcular_entropia(password)

    print(f"• Longitud de caracteres: {longitud}")
    print(f"• Entropía estimada: {entropia} bits")

    # Criterios de evaluación de entropía
    if entropia < 28:
        nivel = "MUY DÉBIL (Vulnerable a ataques instantáneos de fuerza bruta)"
    elif 28 <= entropia < 36:
        nivel = "DÉBIL (Fácil de adivinar con diccionarios básicos)"
    elif 36 <= entropia < 60:
        nivel = "MODERADA (Aceptable para uso general, pero mejorable)"
    elif 60 <= entropia < 128:
        nivel = "FUERTE (Segura contra ataques modernos)"
    else:
        nivel = "EXTREMADAMENTE FUERTE (Grado militar / Criptográfico)"

    print(f"• Veredicto de Fortaleza: {nivel}")

    # Simulación de hash seguro (SHA-256)
    hash_sha256 = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"• Hash SHA-256 (Representación segura en BD): {hash_sha256}")

def generar_password_segura(longitud: int = 16) -> str:
    """Genera una contraseña criptográficamente segura utilizando el módulo secrets."""
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    # Selecciona caracteres aleatorios seguros de forma criptográfica
    password_segura = ''.join(secrets.choice(alfabeto) for _ in range(longitud))
    return password_segura

def main():
    parser = argparse.ArgumentParser(description="Auditor de Ciberseguridad y Generador Criptográfico.")
    parser.add_argument("--accion", type=str, choices=["auditar", "generar"], required=True, help="Acción a realizar.")
    parser.add_argument("--pwd", type=str, default="", help="Contraseña a auditar.")
    parser.add_argument("--longitud", type=int, default=16, help="Longitud para generar nueva contraseña.")

    args = parser.parse_args()

    print("=== NÚCLEO DE CIBERSEGURIDAD ===")

    if args.accion == "auditar":
        if not args.pwd:
            print("[ERROR] Debes proporcionar una contraseña usando --pwd 'tu_contraseña'")
            return
        auditar_password(args.pwd)

    elif args.accion == "generar":
        nueva = generar_password_segura(args.longitud)
        print(f"\n[GENERADOR CRIPTOGRÁFICO] Contraseña segura sugerida:")
        print(f"-> {nueva}")
        auditar_password(nueva)

if __name__ == "__main__":
    main()

