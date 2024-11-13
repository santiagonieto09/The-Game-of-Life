import tkinter as tk

# La clase `Boton` es una clase de botón personalizada en Python que hereda de `tk.Button` y permite
# la creación sencilla de botones con texto, comando, ancho y alto específicos.
class Boton(tk.Button):
    def __init__(self, parent, text, command, width, height):
        super().__init__(parent, text=text, command=command, width=width, height=height, cursor="hand2")
        self.pack(side=tk.LEFT, padx=5, pady=5)