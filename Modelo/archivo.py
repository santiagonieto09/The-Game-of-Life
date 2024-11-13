from tkinter import filedialog
import tkinter as tk
import json

# Clase Singleton para manejar operaciones de archivo
class Archivo:
    _instance = None
    def __init__(self, ANCHO_GRILLA, LARGO_GRILLA):
        self.ancho_grilla = ANCHO_GRILLA
        self.largo_grilla = LARGO_GRILLA

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def guardar(self, grid):
        """
        Guarda una grilla en un archivo JSON después de verificar si hay datos para guardar.
        :param grid: La grilla que se va a guardar.
        """
        if all(not any(row) for row in grid):
            tk.messagebox.showwarning("Advertencia", "No hay datos para guardar!")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".json")
            if file_path:
                data = {"grid": grid}
                with open(file_path, "w") as file:
                    json.dump(data, file)
                tk.messagebox.showinfo("Atención", "Archivo guardado exitosamente.")
            

    def cargar(self):
        """
        Carga datos de un archivo JSON y devuelve los datos del grid si cumple ciertas condiciones.
        :return: Los datos de la cuadrícula de un archivo JSON si el archivo se carga correctamente,
                 None si no se cumplen las condiciones.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)
                if "grid" in data and isinstance(data["grid"], list) and len(data["grid"]) == self.largo_grilla:
                    for row in data["grid"]:
                        if not isinstance(row, list) or len(row) != self.ancho_grilla:
                            break
                    else:
                        return data["grid"]
        return None
