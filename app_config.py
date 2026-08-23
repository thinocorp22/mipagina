import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

def iniciar_sistema():
    print("=== LECTURA SEGURA DE CONFIGURACIÓN (.ENV) ===")
    
    # Obtenemos las variables de entorno de forma segura
    modo = os.getenv("MODO_SERVIDOR", "producción")
    puerto = os.getenv("PUERTO_WEB", "80")
    proyecto = os.getenv("NOMBRE_PROYECTO", "Sin nombre")
    admin = os.getenv("ADMINISTRADOR", "admin")
    
    print(f"-> Proyecto configurado: {proyecto}")
    print(f"-> Administrador del sistema: {admin}")
    print(f"-> Entorno activo: {modo}")
    print(f"-> Puerto asignado: {puerto}")
    
    if modo == "desarrollo":
        print("\n[Aviso] El servidor está corriendo en modo local/desarrollo seguro.")

if __name__ == "__main__":
    iniciar_sistema()

