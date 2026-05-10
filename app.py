from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from Controlador.controlador import api, get_o_crear_sala

app = Flask(__name__)
app.config["SECRET_KEY"] = "game-of-life-secret"
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(api)


@app.errorhandler(413)
def archivo_muy_grande(e):
    return jsonify({"error": "El archivo es demasiado grande (máximo 1 MB)"}), 413


@app.route("/")
def index():
    return render_template("index.html")


# --- WebSocket events ---

@socketio.on("join")
def on_join(data):
    room = data.get("room", "default")
    join_room(room)
    juego = get_o_crear_sala(room)
    emit("estado", juego.get_estado())


@socketio.on("leave")
def on_leave(data):
    room = data.get("room", "default")
    leave_room(room)


@socketio.on("start")
def on_start(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.paused = False
    emit("estado", juego.get_estado(), to=room)
    _run_simulation(room)


@socketio.on("stop")
def on_stop(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.paused = True
    emit("estado", juego.get_estado(), to=room)


@socketio.on("speed")
def on_speed(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.velocidad = max(50, min(2000, int(data.get("velocidad", 100))))
    emit("estado", juego.get_estado(), to=room)


@socketio.on("toggle_celda")
def on_toggle(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.toggle_celda(data["x"], data["y"])
    emit("update_grid", {"grid": juego.grid}, to=room)


@socketio.on("borrar")
def on_borrar(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.borrar()
    emit("estado", juego.get_estado(), to=room)


@socketio.on("patron")
def on_patron(data):
    from Modelo.patrones import get_patron
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    celdas = get_patron(data.get("patron_id"))
    if celdas:
        offset_x = data.get("offset_x", juego.ancho_grilla // 2 - 5)
        offset_y = data.get("offset_y", juego.largo_grilla // 2 - 5)
        juego.colocar_patron(celdas, offset_x, offset_y)
        emit("estado", juego.get_estado(), to=room)


@socketio.on("redimensionar")
def on_redimensionar(data):
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.redimensionar(int(data["ancho"]), int(data["largo"]))
    emit("estado", juego.get_estado(), to=room)


def _run_simulation(room):
    juego = get_o_crear_sala(room)
    if juego.paused:
        return
    tablero_vacio = juego.avanzar()
    socketio.emit("update_grid", {"grid": juego.grid, "tablero_vacio": tablero_vacio, "paused": juego.paused}, to=room)
    if tablero_vacio:
        return
    socketio.sleep(juego.velocidad / 1000.0)
    if not juego.paused:
        socketio.start_background_task(_run_simulation, room)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
