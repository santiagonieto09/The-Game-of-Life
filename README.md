# Juego de la Vida

Este proyecto es una implementación del famoso "Juego de la Vida" de Conway, utilizando Python y la biblioteca Tkinter para la interfaz gráfica. El juego simula la evolución de una cuadrícula de celdas que pueden estar vivas o muertas.
En cada generación, se aplican las siguientes reglas a todas las celdas de la
cuadrícula:
- Si una celda está viva y tiene menos de dos vecinos vivos, muere por
soledad.
- Si una celda está viva y tiene dos o tres vecinos vivos, sigue viva en la
siguiente generación.
- Si una celda está viva y tiene más de tres vecinos vivos, muere por
sobrepoblación.
- Si una celda está muerta y tiene exactamente tres vecinos vivos, se convierte
en una celda viva debido a la reproducción.

El objetivo del juego es observar cómo evoluciona el patrón de celdas a lo largo de
las generaciones.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)


## Características

- Interfaz gráfica intuitiva.
- Posibilidad de iniciar, detener y avanzar el juego.
- Funciones para guardar y cargar el estado del juego.
- Interacción con la cuadrícula mediante clics del mouse.

## Requisitos

- Python 3.x
- Tkinter (generalmente incluido con Python)
- Bibliotecas estándar de Python (json)

## Instalación

1. Clona el repositorio:
   ```bash
   https://github.com/santiagonieto09/The-Game-of-Life.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd juego-de-la-vida
   ```
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```

## Uso

- Al iniciar la aplicación, verás una cuadrícula donde puedes hacer clic para alternar el estado de las celdas (viva/muerta).
- Utiliza los botones en la parte inferior para iniciar, detener, avanzar, guardar o cargar el estado del juego.
- Puedes borrar el tablero y confirmar la acción si es necesario.


## Pantallas del Juego

![image](https://github.com/user-attachments/assets/9e5ec818-85c8-44ad-a6fb-91f96ddf21e8)
