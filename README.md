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
- [Diseno de la implementacion](#diseño-de-la-implementación)
- [Patrones de Diseño](#patrones-de-diseño)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Pantallas del Juego](#pantallas-del-juego)


## Características

- Interfaz gráfica intuitiva.
- Posibilidad de iniciar, detener y avanzar el juego.
- Funciones para guardar y cargar el estado del juego.
- Interacción con la cuadrícula mediante clics del mouse.
## Diseño de la implementación.
  
  ![image](https://github.com/user-attachments/assets/02710e38-d727-46cb-9aa9-511d049402f8)
  
## Patrones de Diseño.
- Modelo-Vista-Controlador (MVC):
  
  ![image](https://github.com/user-attachments/assets/86d63f1f-15db-40d0-a71c-0b3dfe464021)

El patrón Modelo-Vista-Controlador (MVC) es un patrón de diseño de
software que separa la lógica de una aplicación en tres componentes
principales: el Modelo, la Vista y el Controlador. Esta separación permite un
desarrollo modular y facilita el mantenimiento y la reutilización del código.

   1. Modelo: Representa los datos y la lógica de negocio de la aplicación.
      En este proyecto, la clase JuegoDeLaVida es el Modelo, que
      contiene la lógica principal del Juego de la Vida y la clase Archivo
      que es la encargada de guardar y cargar los modelos del juego de la
      vida en formatos JSON.
   2. Vista: Es responsable de la presentación y la representación visual de
los datos. En este proyecto, las clases Ventana y Boton forman la
vista, encargándose de la interfaz gráfica de usuario (GUI) y la
visualización de la cuadrícula.
   3. Controlador: Actúa como intermediario entre el Modelo y la Vista. Es
responsable de manejar las entradas del usuario. En este proyecto, la
clase Controlador actúa como el Controlador, manejando las
interacciones entre la Vista (Ventana) y el Modelo (JuegoDeLaVida).




- Singleton:
  
El patrón Singleton es un patrón de diseño de creación que garantiza que una clase
tenga una única instancia y proporciona un punto de acceso global a ella. Este
patrón se utiliza cuando se necesita un control estricto sobre la creación de objetos
y se desea asegurar que solo exista una instancia de una clase.

![image](https://github.com/user-attachments/assets/280d7817-76f4-4f84-9e53-479d128d2ee2)


En este proyecto, la clase Archivo implementa el patrón Singleton. Esta clase se
encarga de las operaciones de guardar y cargar el estado del juego en archivos
JSON. Al utilizar el patrón Singleton, se asegura que solo exista una instancia de la
clase Archivo, lo que permite un manejo centralizado de las operaciones de
archivo.
La implementación del patrón Singleton en la clase Archivo se realiza mediante el
método __new__ y una variable de clase _instance. Cuando se intenta crear una
nueva instancia de archivo, el método __new__ verifica si ya existe una instancia
previa. Si no existe, crea una nueva instancia y la almacena en _instance. Si ya
existe una instancia, devuelve la instancia existente.

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
