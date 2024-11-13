
from Modelo.juegoDeLaVida import JuegoDeLaVida

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = JuegoDeLaVida(self.vista.ancho_grilla, self.vista.largo_grilla)

    def guardar(self):
        """
        Maneja el evento de hacer clic en el botón de guardar.
        """
        self.modelo.guardar(self.vista)
        
    def cargar(self):
        """
        Maneja el evento de hacer clic en el botón de cargar.
        """
        self.modelo.cargar(self.vista)
        self.vista.dibujar_grilla()

    def contar_vecinos_vivos(self, x, y):
        """
        Maneja el metodo de contar vecinos.
        """
        return self.modelo.contar_vecinos_vivos(self.vista, x, y)

