from abc import ABC, abstractmethod

# 1. Interfaz del Observador
class Observador(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str):
        pass

# 2. Sujeto u Objeto Observable (el que emite los eventos)
class ServidorMonitoreo:
    def __init__(self):
        self._observadores = []
        self._estado_actual = "Normal"

    def agregar_observador(self, obs: Observador):
        self._observadores.append(obs)

    def quitar_observador(self, obs: Observador):
        self._observadores.remove(obs)

    def notificar_observadores(self):
        for obs in self._observadores:
            obs.actualizar(self._estado_actual)

    def cambiar_estado(self, nuevo_estado: str):
        print(f"\n[Sistema] El estado del servidor cambió a: '{nuevo_estado}'")
        self._estado_actual = nuevo_estado
        self.notificar_observadores()

# 3. Observadores Concretos (los que reaccionan al evento)
class AdministradorCorreo(Observador):
    def actualizar(self, mensaje: str):
        print(f" -> [Alerta Email] Enviando notificación al administrador. Estado: {mensaje}")

class SistemaRegistroLogs(Observador):
    def actualizar(self, mensaje: str):
        print(f" -> [Log Automático] Registrando evento crítico en disco. Estado: {mensaje}")

class PanelWebAlerta(Observador):
    def actualizar(self, mensaje: str):
        print(f" -> [Dashboard Frontend] Actualizando interfaz gráfica en tiempo real. Estado: {mensaje}")

if __name__ == "__main__":
    print("=== PATRÓN DE DISEÑO OBSERVER (EVENTOS) ===")
    
    # Creamos el sujeto observable
    servidor = ServidorMonitoreo()

    # Registramos a los observadores interesados en los cambios del servidor
    servidor.agregar_observador(AdministradorCorreo())
    servidor.agregar_observador(SistemaRegistroLogs())
    servidor.agregar_observador(PanelWebAlerta())

    # Simulamos un cambio de estado crítico en el sistema
    servidor.cambiar_estado("Alerta de Almacenamiento al 90%")

