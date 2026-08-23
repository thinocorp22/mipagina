import unittest
from modelos import ProyectoModel

class TestProyectoModel(unittest.TestCase):
    
    def setUp(self):
        # Este método se ejecuta antes de cada prueba para preparar un entorno limpio
        self.proyecto = ProyectoModel(
            id=99, 
            nombre="Prueba Unitaria Test", 
            tipo="Testing", 
            estado="En pruebas"
        )

    def test_creacion_proyecto(self):
        # Verificamos que los atributos se asignen correctamente
        self.assertEqual(self.proyecto.id, 99)
        self.assertEqual(self.proyecto.nombre, "Prueba Unitaria Test")
        self.assertEqual(self.proyecto.estado, "En pruebas")

    def test_metodo_resumen(self):
        # Verificamos que el método devuelva la cadena esperada con el formato correcto
        resumen = self.proyecto.resumen()
        self.assertIn("Prueba Unitaria Test", resumen)
        self.assertIn("Testing", resumen)
        self.assertIn("En pruebas", resumen)

if __name__ == "__main__":
    # Ejecutamos las pruebas automáticamente
    unittest.main()

