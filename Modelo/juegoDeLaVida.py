from .archivo import Archivo


class JuegoDeLaVida:
    def __init__(self, ANCHO_GRILLA, LARGO_GRILLA):
        self.ancho_grilla = ANCHO_GRILLA
        self.largo_grilla = LARGO_GRILLA
        
    def contar_vecinos_vivos(self,ventana, x, y):
        """
        Esta función cuenta la cantidad de vecinos vivos que rodean una celda en una
        cuadrícula, teniendo en cuenta los límites de la cuadrícula mediante operaciones de módulo.
        
        :param x: El parámetro "x" representa la coordenada x
        de una celda en una cuadrícula. La función está diseñada para contar el
        número de vecinos vivos que rodean una celda en la posición `(x, y)` en la grilla
        
        :param y: El parámetro 'y' representa la posición vertical o el índice de fila
        en una cuadrícula. Se utiliza para determinar la fila actual en la cuadrícula para la cual
        queremos contar el número de vecinos activos
        
        :return: el recuento de vecinos vivos que rodean la celda en la posición (x, y) de la
        cuadrícula.
        """
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.ancho_grilla   # Aplicar operacion modulo para obtener una posición valida en el eje x
                ny = (y + dy) % self.largo_grilla  # Aplicar operacion modulo para obtener una posición valida en el eje y
                if ventana.grid[ny][nx]:
                    count += 1
        return count
    
    def guardar(self,ventana):
        """
        La función guarda los datos de la grilla usando una función auxiliar
        `Archivo.guardar`.
        """
        archivoSingleton = Archivo(self.ancho_grilla, self.largo_grilla)
        archivoSingleton.guardar(ventana.grid)

    def cargar(self,ventana):
        """
        La función carga un grid desde un archivo usando el método `Archivo.cargar` y actualiza
        el atributo grid del objeto.
        """
        archivoSingleton = Archivo(self.ancho_grilla, self.largo_grilla)
        loaded_grid = archivoSingleton.cargar()
        if loaded_grid:
            ventana.grid = loaded_grid
            ventana.dibujar_grilla()
            
        