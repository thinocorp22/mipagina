class GestorConfiguracionSistema:
    _instancia = None  # Variable de clase para guardar la única instancia permitida

    def __new__(cls, *args, **kwargs):
        # Sobrescribimos el método de creación (__new__) para controlar las instancias
        if cls._instancia is None:
            print("[Singleton] Creando la ÚNICA instancia del sistema de configuración...")
            cls._instancia = super(GestorConfiguracionSistema, cls).__new__(cls)
            # Inicializamos variables internas de la instancia única
            cls._instancia.configuraciones = {
                "entorno": "producción",
                "servidor": "Termux-Mobile",
                "puerto": 8080
            }
        else:
            print("[Singleton] La instancia ya existe. Reutilizando la existente.")
        return cls._instancia

    def obtener_config(self, clave):
        return self.configuraciones.get(clave, "No encontrado")

    def actualizar_config(self, clave, valor):
        self.configuraciones[clave] = valor
        print(f"[Actualización] Configuración '{clave}' modificada a '{valor}'.")

if __name__ == "__main__":
    print("=== PATRÓN DE DISEÑO SINGLETON (ÚNICA INSTANCIA) ===")
    
    # Intentamos crear la primera instancia
    config1 = GestorConfiguracionSistema()
    print(f"Puerto actual desde config1: {config1.obtener_config('puerto')}")
    
    print("\nModificando configuración usando config1...")
    config1.actualizar_config("puerto", 5000)
    
    print("\nIntentando crear una 'nueva' instancia (config2)...")
    config2 = GestorConfiguracionSistema()
    
    # Verificamos que config2 apunta exactamente al mismo objeto en memoria y comparte el estado
    print(f"Puerto leído desde config2: {config2.obtener_config('puerto')}")
    print(f"¿Son exactamente el mismo objeto en memoria? {config1 is config2}")

