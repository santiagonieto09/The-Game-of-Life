import json

MAX_DIMENSION = 150


class Archivo:
    _instance = None

    def __init__(self, ancho_grilla, largo_grilla):
        self.ancho_grilla = ancho_grilla
        self.largo_grilla = largo_grilla

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def guardar(self, grid):
        if all(not any(row) for row in grid):
            return None
        largo = len(grid)
        ancho = len(grid[0]) if largo > 0 else 0
        return json.dumps({"ancho": ancho, "largo": largo, "grid": grid})

    def cargar(self, data):
        try:
            if isinstance(data, str):
                data = json.loads(data)

            if not isinstance(data, dict) or "grid" not in data:
                return None

            grid = data["grid"]
            if not isinstance(grid, list) or len(grid) == 0:
                return None

            largo = len(grid)
            ancho = len(grid[0]) if isinstance(grid[0], list) else 0

            if ancho == 0 or largo == 0:
                return None
            if ancho > MAX_DIMENSION or largo > MAX_DIMENSION:
                return None

            sanitized = []
            for row in grid:
                if not isinstance(row, list) or len(row) != ancho:
                    return None
                sanitized_row = []
                for cell in row:
                    if not isinstance(cell, bool):
                        return None
                    sanitized_row.append(cell)
                sanitized.append(sanitized_row)

            return {"ancho": ancho, "largo": largo, "grid": sanitized}
        except (json.JSONDecodeError, TypeError, KeyError):
            return None
