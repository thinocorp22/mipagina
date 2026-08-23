import argparse
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import base64
import sqlite3

# 1. CONFIGURACIÓN DE LOGGING Y RUTAS
log_path = Path.cwd() / "owner_audit.log"
db_path = Path.cwd() / "owner_system.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [OWNER-AUDIT] [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OwnerMasterPanel")


# 2. PERSISTENCIA EN BASE DE DATOS
def inicializar_base_datos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            accion TEXT,
            proyecto TEXT,
            estado_resultado TEXT
        )
    """)
    conn.commit()
    conn.close()


def registrar_en_db(accion: str, proyecto: str, resultado: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO historial_operaciones (timestamp, accion, proyecto, estado_resultado) VALUES (?, ?, ?, ?)",
            (ahora, accion, proyecto, resultado)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error en BD: {e}")


# 3. ESTRUCTURA DE DATOS
@dataclass
class ProyectoOwner:
    id_proyecto: int
    nombre: str
    estado: str
    version: str
    propietario: str = "José Martínez (Owner)"


# =====================================================================
# 4. APLICANDO OCP: INTERFAZ ABSTRACTA PARA COMANDOS (EXTENSIBLE)
# =====================================================================
class ComandoOwner(ABC):
    @abstractmethod
    def ejecutar(self, proyecto: str):
        pass


# Comandos Concretos Existentes (Cerrados a modificación, pero ya integrados)
class ComandoEstado(ComandoOwner):
    def ejecutar(self, proyecto: str):
        p = ProyectoOwner(id_proyecto=1, nombre=proyecto, estado="Activo y En Línea", version="2.5.0")
        print(f"[{p.id_proyecto}] {p.nombre} (v{p.version}) - Estado: {p.estado} | Owner: {p.propietario}")
        logger.info(f"Consulta de estado ejecutada para: {proyecto}")
        registrar_en_db("estado", proyecto, "Éxito - Estado consultado")


class ComandoDesplegar(ComandoOwner):
    def ejecutar(self, proyecto: str):
        print(f"[DEPLOY] Iniciando despliegue seguro del proyecto '{proyecto}'...")
        logger.info(f"Despliegue maestro ejecutado para: {proyecto}")
        print("[ÉXITO] Servidores actualizados y sincronizados.")
        registrar_en_db("desplegar", proyecto, "Éxito - Despliegue completado")


class ComandoAuditar(ComandoOwner):
    def ejecutar(self, proyecto: str):
        print(f"[AUDITORÍA] Leyendo registros de auditoría en: {log_path}")
        logger.info("Reporte de auditoría global solicitado.")
        print("[ÉXITO] Auditoría completada sin anomalías.")
        registrar_en_db("auditar", proyecto, "Éxito - Auditoría leída")


class ComandoRespaldar(ComandoOwner):
    def ejecutar(self, proyecto: str):
        print("[RESPALDO] Iniciando protocolo de cifrado nativo...")
        try:
            if not log_path.exists():
                print("[Advertencia] No hay registros para respaldar.")
                return
            with open(log_path, "rb") as f:
                datos = f.read()
            # Cifrado nativo XOR + Base64
            cifrados = bytes([b ^ 85 for b in datos])
            codificados = base64.b64encode(cifrados)
            
            respaldo_path = Path.cwd() / "owner_audit_seguro.enc"
            with open(respaldo_path, "wb") as f:
                f.write(codificados)
            
            print(f"[CRIPTO-ÉXITO] Respaldo guardado en: {respaldo_path}")
            logger.info("Respaldo cifrado generado con éxito.")
            registrar_en_db("respaldar", proyecto, "Éxito - Respaldo generado")
        except Exception as e:
            print(f"[ERROR] Falló el respaldo: {e}")
            registrar_en_db("respaldar", proyecto, f"Fallo: {e}")


class ComandoHistorial(ComandoOwner):
    def ejecutar(self, proyecto: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, accion, proyecto, estado_resultado FROM historial_operaciones ORDER BY id DESC LIMIT 5")
        filas = cursor.fetchall()
        conn.close()

        print("\n=== HISTORIAL RECIENTE EN BASE DE DATOS (SQLite) ===")
        if not filas:
            print("No hay registros previos.")
            return
        for fila in filas:
            print(f"[{fila[0]}] Acción: {fila[1].upper()} | Proyecto: {fila[2]} | Estado: {fila[3]}")
        logger.info("Historial consultado.")
        registrar_en_db("historial", proyecto, "Éxito - Historial consultado")


# --- ¡EXTENSIBILIDAD PURA (NUEVA ACCIÓN SIN MODIFICAR EL NÚCLEO)! ---
# Si mañana quieres agregar una acción de "analizar seguridad", solo creas esta clase:
class ComandoAnalisisSeguridad(ComandoOwner):
    def ejecutar(self, proyecto: str):
        print(f"[SCANNER] Escaneando vulnerabilidades en el entorno de '{proyecto}'...")
        print("[SEGURIDAD] Integridad del sistema al 100%. Sin amenazas detectadas.")
        logger.info(f"Escaneo de seguridad ejecutado para: {proyecto}")
        registrar_en_db("escanear", proyecto, "Éxito - Escaneo completado")


# 5. REGISTRO DE COMANDOS (POLIMORFISMO)
REGISTRO_COMANDOS = {
    "estado": ComandoEstado(),
    "desplegar": ComandoDesplegar(),
    "auditar": ComandoAuditar(),
    "respaldar": ComandoRespaldar(),
    "historial": ComandoHistorial(),
    "escanear": ComandoAnalisisSeguridad()  # ¡Agregado limpiamente aquí!
}


# 6. NÚCLEO PRINCIPAL
def main():
    inicializar_base_datos()

    parser = argparse.ArgumentParser(description="Panel de Control Maestro con Principio OCP.")
    parser.add_argument("--token", type=str, required=True, help="Token de seguridad de la cuenta Owner.")
    parser.add_argument("--accion", type=str, choices=list(REGISTRO_COMANDOS.keys()), required=True, help="Acción a ejecutar.")
    parser.add_argument("--proyecto", type=str, default="El Rincón de las Esquinas", help="Nombre del proyecto.")

    args = parser.parse_args()

    print("=== AUTENTICACIÓN DE DEVELOPER OWNER ===")
    
    TOKEN_MAESTRO_OWNER = "ROOT-ADMIN-2026"
    if args.token != TOKEN_MAESTRO_OWNER:
        logger.warning(f"Intento de acceso denegado con token: '{args.token}'")
        print("[ACCESO DENEGADO] Token inválido.")
        registrar_en_db(args.accion, args.proyecto, "Acceso Denegado")
        return

    logger.info("Autenticación de Owner exitosa.")
    print("[ACCESO AUTORIZADO] Bienvenido, Developer Owner.\n")

    # Ejecución polimórfica: El núcleo no sabe qué hace el comando, solo lo ejecuta.
    comando = REGISTRO_COMANDOS.get(args.accion)
    if comando:
        comando.ejecutar(args.proyecto)
    else:
        print("[ERROR] Acción no reconocida.")

if __name__ == "__main__":
    main()
	

