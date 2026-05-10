# Juego de la Vida

Implementación web del famoso "Juego de la Vida" de Conway, usando **Flask**, **Flask-SocketIO** y **HTML5 Canvas**.

## Reglas

En cada generación se aplican estas reglas a todas las celdas:

- Si una celda está viva y tiene menos de dos vecinos vivos, muere por soledad.
- Si una celda está viva y tiene dos o tres vecinos vivos, sigue viva.
- Si una celda está viva y tiene más de tres vecinos vivos, muere por sobrepoblación.
- Si una celda está muerta y tiene exactamente tres vecinos vivos, nace por reproducción.

## Características

- Interfaz web moderna y responsive con tema oscuro.
- Simulación en tiempo real via WebSocket.
- Patrones predefinidos (Glider, Pulsar, Gosper Glider Gun, etc.).
- Control de velocidad de simulación.
- Grilla redimensionable.
- Soporte multiusuario: múltiples usuarios pueden unirse a la misma sala y editar el tablero en tiempo real.
- Guardar y cargar estados del juego como archivos JSON.

## Arquitectura (MVC)

- **Modelo** (`Modelo/`): Lógica del juego, manejo de archivos y patrones predefinidos.
- **Vista** (`templates/`, `static/`): Interfaz web con HTML5 Canvas, CSS y JavaScript.
- **Controlador** (`Controlador/`): Endpoints REST y manejo de eventos WebSocket.

### Patrones de diseño

- **MVC**: Separación clara entre lógica, presentación y control.
- **Singleton**: La clase `Archivo` garantiza una única instancia para las operaciones de archivo.

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/santiagonieto09/The-Game-of-Life.git
   cd The-Game-of-Life
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

4. Abre tu navegador en `http://localhost:5000`

## Uso

- **Clic en la grilla**: Alterna el estado de una celda (viva/muerta).
- **Iniciar/Detener**: Inicia o pausa la simulación.
- **Avanzar**: Avanza un solo paso.
- **Borrar**: Limpia todo el tablero.
- **Patrones**: Selecciona y coloca patrones predefinidos.
- **Velocidad**: Ajusta la velocidad de la simulación con el slider.
- **Tamaño**: Cambia las dimensiones de la grilla.
- **Salas**: Únete a una sala para editar colaborativamente con otros usuarios.
- **Guardar/Cargar**: Descarga o sube el estado del tablero como archivo JSON.

## Despliegue

