import tkinter as tk
import copy
from .boton import Boton
from Controlador.controlador import Controlador


class Ventana:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Juego de la Vida")
        self.tamanio_celda = 20
        self.ancho_grilla = 68
        self.largo_grilla = 30
        self.ancho_boton = 13  
        self.alto_boton = 2  
        self.canvas = tk.Canvas(self.raiz, width=self.tamanio_celda * self.ancho_grilla, height=self.tamanio_celda * self.largo_grilla)
        self.canvas.pack()
        self.controlador = Controlador(self)

        self.grid = [[False] * self.ancho_grilla for _ in range(self.largo_grilla)]
        self.paused = True

        boton_frame = tk.Frame(self.raiz)  # Frame para contener los botones
        boton_frame.pack(side=tk.BOTTOM, padx=20, pady=20)  # Ajustar el margen del contenedor de los botones

        

        self.boton_iniciar_parar = Boton(boton_frame, text="Iniciar", command=self.toggle_iniciar_parar,
                                         width=self.ancho_boton, height=self.alto_boton)
        self.boton_avanzar = Boton(boton_frame, text="Avanzar", command=self.avanzar,
                                   width=self.ancho_boton, height=self.alto_boton)
        self.boton_borrar = Boton(boton_frame, text="Borrar Tablero", command=self.borrar,
                                  width=self.ancho_boton, height=self.alto_boton)
        self.boton_guardar = Boton(boton_frame, text="Guardar Modelo", command=self.controlador.guardar,
                                   width=self.ancho_boton, height=self.alto_boton)
        self.boton_cargar = Boton(boton_frame, text="Cargar Modelo", command=self.controlador.cargar,
                                  width=self.ancho_boton, height=self.alto_boton)
        self.boton_salir = Boton(boton_frame, text="Salir", command=self.salir_juego,
                                 width=self.ancho_boton, height=self.alto_boton)

        self.canvas.bind("<Button-1>", self.hacer_click)

        self.dibujar_grilla()
    
    def salir_juego(self):
        """
        La función "salir_juego" comprueba si todas las filas del grid están vacías y sale del juego si
        lo están, de lo contrario pide confirmación antes de salir.
        """
        if all(not any(row) for row in self.grid):
            self.raiz.quit()
        else:
            confirm = tk.messagebox.askokcancel("Confirmación", "¿Desea salir el juego? Se perderan los datos.")
            if confirm:
                self.raiz.quit()
            
    def toggle_iniciar_parar(self):
        """
        La función alterna entre iniciar y detener un proceso y actualiza el texto de un botón en
        consecuencia.
        """
        self.paused = not self.paused
        self.boton_iniciar_parar.configure(text="Iniciar" if self.paused else "Detener")
        if not self.paused:
            self.avanzar()

    def hacer_click(self, event):
        """
        Esta función actualiza una cuadrícula en función de un evento de clic del mouse
        alternando el valor en la celda de la cuadrícula correspondiente y luego volviendo a dibujar la
        cuadrícula.
        
        :param event: El parámetro `event` suele ser un objeto que representa
        un evento que ha ocurrido, como un clic del mouse o una pulsación de tecla. En este contexto,
        el parámetro "evento" captura las coordenadas del evento de clic del mouse,
        específicamente la x y
        """
        x = event.x // self.tamanio_celda
        y = event.y // self.tamanio_celda
        self.grid[y][x] = not self.grid[y][x]
        self.dibujar_grilla()

    def dibujar_grilla(self):
        """
        La función dibuja una cuadrícula con rectángulos que representan
        celdas, delineándolas en gris y llenando las celdas vivas en rojo.
        """
        self.canvas.delete("all")
        for y in range(self.largo_grilla):
            for x in range(self.ancho_grilla):
                # Dibujar la cuadricula
                self.canvas.create_rectangle(
                    x * self.tamanio_celda,
                    y * self.tamanio_celda,
                    (x + 1) * self.tamanio_celda,
                    (y + 1) * self.tamanio_celda,
                    outline="gray",
                    width=1
                )
                if self.grid[y][x]:
                    # Dibujar las celulas vivas
                    self.canvas.create_rectangle(
                        x * self.tamanio_celda + 1,
                        y * self.tamanio_celda + 1,
                        (x + 1) * self.tamanio_celda - 1,
                        (y + 1) * self.tamanio_celda - 1,
                        fill="red"
                    )
     
    def avanzar(self):
        """
        La función avanza el estado de una cuadrícula según
        las reglas del Juego de la Vida de Conway, actualizando los estados de las celdas y volviendo a
        dibujar la cuadrícula.
        """
        new_grid = copy.deepcopy(self.grid)
        for y in range(self.largo_grilla):
            for x in range(self.ancho_grilla):
                live_neighbors = self.controlador.contar_vecinos_vivos(x, y)
                if self.grid[y][x]:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[y][x] = False
                else:
                    if live_neighbors == 3:
                        new_grid[y][x] = True
        self.grid = new_grid
        self.dibujar_grilla()

        # Verificar si el tablero está vacío y pausar el juego si es necesario
        if all(not any(row) for row in self.grid):
            self.paused = True
            self.boton_iniciar_parar.configure(text="Iniciar")
            tk.messagebox.showinfo("Juego Terminado", "El tablero está vacío.")

        if not self.paused:
            self.raiz.after(100, self.avanzar)
                    
    def borrar(self):
        """
        La función verifica si todas las filas de la cuadrícula están vacías y solicita
        confirmación al usuario antes de borrar la cuadrícula si es necesario.
        :return: Si se cumple la condición "todos (no cualquiera (fila) para la fila en self.grid)",
        entonces se devuelve "Ninguno". De lo contrario, si el usuario confirma la eliminación del
        tablero, el tablero se borrará y se volverá a dibujar, pero en ese caso no se devolverá ningún
        valor específico.
        """
        if all(not any(row) for row in self.grid):
            return
        else:
            confirm = tk.messagebox.askokcancel("Confirmación", "¿Desea borrar el tablero?")
            if confirm:
                self.grid = [[False] * self.ancho_grilla for _ in range(self.largo_grilla)]
                self.dibujar_grilla()
        
