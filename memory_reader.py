import argparse
import math
from cryptography.fernet import Fernet
from pathlib import Path

def calcular_entropia_bloque(datos: bytes) -> float:
    """
    Calcula la entropía de un bloque de memoria o archivo.
    Una entropía cercana a 8.0 indica datos altamente aleatorios, 
    lo cual es un fuerte indicador de cifrado o compresión.
    """
    if not datos:
        return 0.0
    
    entropia = 0.0
    longitud = len(datos)
    
    # Contar la frecuencia de cada byte (0-255)
    frecuencias = [0] * 256
    for b in datos:
        frecuencias[b] += 1
        
    for f in frecuencias:
        if f > 0:
            probabilidad = f / longitud
            entropia -= probabilidad * math.log2(probabilidad)
            
    return round(entropia, 4)

def analizar_volcado_memoria(ruta_archivo: str):
    """Analiza un archivo binario o volcado de memoria buscando regiones cifradas."""
    archivo = Path(ruta_archivo)
    if not archivo.exists():
        print(f"[ERROR] El archivo o volcado '{ruta_archivo}' no existe.")
        return

    print(f"\n[ANALIZADOR FORENSE] Analizando archivo: {archivo.name} ...")
    
    with open(archivo, "rb") as f:
        contenido = f.read()

    tamano_total = len(contenido)
    entropia_total = calcular_entropia_bloque(contenido)

    print(f"• Tamaño total analizado: {tamano_total} bytes")
    print(f"• Entropía global del bloque: {entropia_total} / 8.0 bits")

    if entropia_total > 7.2:
        print("[CONCLUSIÓN] El contenido muestra una entropía muy alta. Probablemente es un volcado completamente cifrado o comprimido.")
    elif 4.0 <= entropia_total <= 7.0:
        print("[CONCLUSIÓN] El contenido muestra una mezcla de texto plano, código o estructuras legibles y datos protegidos.")
    else:
        print("[CONCLUSIÓN] Baja entropía. Predominan datos estructurados o texto plano.")

def leer_datos_encriptados(ruta_archivo: str, clave_hex_o_fernet: str):
    """Intenta descifrar y leer el contenido protegido utilizando una clave simétrica."""
    archivo = Path(ruta_archivo)
    if not archivo.exists():
        print(f"[ERROR] El archivo cifrado no existe.")
        return

    try:
        with open(archivo, "rb") as f:
            datos_cifrados = f.read()

        # Inicializamos el cifrador simétrico Fernet (AES-128 en modo CBC con HMAC)
        cipher = Fernet(clave_hex_o_fernet.encode('utf-8'))
        datos_descifrados = cipher.decrypt(datos_cifrados)

        print(f"\n[ÉXITO] Memoria / Archivo descifrado correctamente.")
        print(f"--- CONTENIDO RECUPERADO (Primeros 300 caracteres) ---")
        print(datos_descifrados[:300].decode('utf-8', errors='ignore'))

    except Exception as e:
        print(f"[ERROR DE DESCIFRADO] No se pudo leer la memoria encriptada (Clave incorrecta o formato dañado): {e}")

def main():
    parser = argparse.ArgumentParser(description="Lector y Analizador Forense de Memoria y Archivos Cifrados.")
    parser.add_argument("--accion", type=str, choices=["analizar", "leer"], required=True, help="Acción a realizar.")
    parser.add_argument("--archivo", type=str, required=True, help="Ruta del archivo binario o volcado de memoria.")
    parser.add_argument("--clave", type=str, default="", help="Clave de descifrado (para la acción 'leer').")

    args = parser.parse_args()

    print("=== NÚCLEO DE ANÁLISIS DE MEMORIA Y CRIPTOGRAFÍA ===")

    if args.accion == "analizar":
        analizar_volcado_memoria(args.archivo)
    elif args.accion == "leer":
        if not args.clave:
            print("[ERROR] Debes proporcionar la clave de descifrado usando --clave 'tu_clave'")
            return
        leer_datos_encriptados(args.archivo, args.clave)

if __name__ == "__main__":
    main()

