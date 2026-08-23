import re

def analizar_texto():
    # Texto de prueba que simula un registro (log) o contenido de tu sitio
    texto_muestra = """
    Hola desde El Rincón de las Esquinas. 
    Puedes contactarnos en soporte@elrincondelasesquinas.com o visitar nuestra web segura https://thinocorp22.github.io/mipagina.
    Fecha de la actualización: 2026-08-22. Código de servidor interno: SRV-8080.
    """

    print("=== ANÁLISIS CON EXPRESIONES REGULARES (REGEX) ===")

    # 1. Buscar y extraer correos electrónicos usando un patrón Regex
    # Patrón: busca caracteres de texto antes de una '@', seguido de un dominio y extensión
    patron_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails_encontrados = re.findall(patron_email, texto_muestra)
    print(f"\n[Correos detectados]: {emails_encontrados}")

    # 2. Buscar y extraer fechas con formato YYYY-MM-DD
    # Patrón: 4 dígitos, un guion, 2 dígitos, un guion, 2 dígitos
    patron_fecha = r'\d{4}-\d{2}-\d{2}'
    fechas_encontradas = re.findall(patron_fecha, texto_muestra)
    print(f"[Fechas detectadas]: {fechas_encontradas}")

    # 3. Validar si existe una URL web segura (https://)
    patron_url = r'https://[^\s]+'
    urls_encontradas = re.findall(patron_url, texto_muestra)
    print(f"[URLs seguras detectadas]: {urls_encontradas}")

    # 4. Reemplazar texto dinámicamente (por ejemplo, censurar códigos internos)
    texto_censurado = re.sub(r'SRV-\d+', 'SRV-XXXX', texto_muestra)
    print(f"\n[Texto modificado con Regex]:\n{texto_censurado}")

if __name__ == "__main__":
    analizar_texto()

