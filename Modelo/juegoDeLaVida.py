import copy
from .archivo import Archivo


class JuegoDeLaVida:
    def __init__(self, ancho_grilla, largo_grilla):
        self.ancho_grilla = ancho_grilla
        self.largo_grilla = largo_grilla
        self.grid = [[False] * ancho_grilla for _ in range(largo_grilla)]
        self.paused = True
        self.velocidad = 100

    def contar_vecinos_vivos(self, x, y):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.ancho_grilla
                ny = (y + dy) % self.largo_grilla
                if self.grid[ny][nx]:
                    count += 1
        return count

    def avanzar(self):
        new_grid = copy.deepcopy(self.grid)
        for y in range(self.largo_grilla):
            for x in range(self.ancho_grilla):
                live_neighbors = self.contar_vecinos_vivos(x, y)
                if self.grid[y][x]:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[y][x] = False
                else:
                    if live_neighbors == 3:
                        new_grid[y][x] = True
        self.grid = new_grid
        tablero_vacio = all(not any(row) for row in self.grid)
        if tablero_vacio:
            self.paused = True
        return tablero_vacio

    def toggle_celda(self, x, y):
        if 0 <= x < self.ancho_grilla and 0 <= y < self.largo_grilla:
            self.grid[y][x] = not self.grid[y][x]

    def borrar(self):
        self.grid = [[False] * self.ancho_grilla for _ in range(self.largo_grilla)]
        self.paused = True

    def redimensionar(self, nuevo_ancho, nuevo_largo):
        self.ancho_grilla = nuevo_ancho
        self.largo_grilla = nuevo_largo
        self.grid = [[False] * nuevo_ancho for _ in range(nuevo_largo)]
        self.paused = True

    def colocar_patron(self, patron, offset_x=0, offset_y=0):
        self.borrar()
        for (dx, dy) in patron:
            x = (offset_x + dx) % self.ancho_grilla
            y = (offset_y + dy) % self.largo_grilla
            self.grid[y][x] = True

    def guardar(self):
        archivo = Archivo(self.ancho_grilla, self.largo_grilla)
        return archivo.guardar(self.grid)

    def cargar(self, data):
        archivo = Archivo(self.ancho_grilla, self.largo_grilla)
        loaded_grid = archivo.cargar(data)
        if loaded_grid:
            self.grid = loaded_grid
            return True
        return False

    def get_estado(self):
        return {
            "grid": self.grid,
            "paused": self.paused,
            "ancho": self.ancho_grilla,
            "largo": self.largo_grilla,
            "velocidad": self.velocidad,
        }
