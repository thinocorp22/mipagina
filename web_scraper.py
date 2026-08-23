import argparse
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

# Analizador HTML personalizado para extraer títulos y enlaces
class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.enlaces = []
        self.titulos = []
        self._en_titulo = False
        self._en_enlace = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title':
            self._en_titulo = True
        elif tag.lower() == 'a':
            for attr, value in attrs:
                if attr == 'href' and value:
                    self.enlaces.append(value)

    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self._en_titulo = False

    def handle_data(self, data):
        texto_limpio = data.strip()
        if texto_limpio:
            if self._en_titulo:
                self.titulos.append(texto_limpio)

def analizar_pagina_web(url_destino: str):
    """Realiza una petición HTTP segura y extrae metadatos y enlaces de la página."""
    print(f"\n[SCRAPER] Conectando a: {url_destino} ...")
    
    # Validamos que la URL sea correcta
    parsed_url = urlparse(url_destino)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("[ERROR] La URL proporcionada no es válida. Asegúrate de incluir http:// o https://")
        return

    # Configuramos una cabecera User-Agent para simular un navegador real
    headers = {'User-Agent': 'Mozilla/5.0 (Compatible; AutomatedScraperBot/1.0)'}
    
    try:
        req = urllib.request.Request(url_destino, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as respuesta:
            if respuesta.status != 200:
                print(f"[ERROR] El servidor respondió con código de estado: {respuesta.status}")
                return
            
            # Leemos y decodificamos el contenido HTML
            html_bytes = respuesta.read()
            html_texto = html_bytes.decode('utf-8', errors='ignore')

        print("[ÉXITO] Contenido HTML descargado. Analizando estructura...")
        
        # Parseamos el HTML con nuestro analizador personalizado
        parser = SimpleHTMLParser()
        parser.feed(html_texto)

        print(f"\n--- RESULTADOS DEL ANÁLISIS ---")
        if parser.titulos:
            print(f"• Título de la página: {parser.titulos[0]}")
        else:
            print("• Título de la página: (No encontrado)")

        print(f"• Total de enlaces (<a>) encontrados: {len(parser.enlaces)}")
        print("\nPrimeros 5 enlaces extraídos:")
        for i, link in enumerate(parser.enlaces[:5], 1):
            print(f"  {i}. {link}")

    except urllib.error.URLError as e:
        print(f"[ERROR DE RED] No se pudo conectar a la URL: {e.reason}")
    except Exception as e:
        print(f"[ERROR INESPERADO]: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bot de Web Scraping y Automatización de Extracción de Datos.")
    parser.add_argument("--url", type=str, required=True, help="URL completa de la página web a analizar.")

    args = parser.parse_args()

    print("=== NÚCLEO DE AUTOMATIZACIÓN Y SCRAPING ===")
    analizar_pagina_web(args.url)

if __name__ == "__main__":
    main()

