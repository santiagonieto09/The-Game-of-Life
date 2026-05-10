import json


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
        return json.dumps({"grid": grid})

    def cargar(self, data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if "grid" in data and isinstance(data["grid"], list) and len(data["grid"]) == self.largo_grilla:
                for row in data["grid"]:
                    if not isinstance(row, list) or len(row) != self.ancho_grilla:
                        return None
                return data["grid"]
        except (json.JSONDecodeError, TypeError, KeyError):
            return None
        return None
