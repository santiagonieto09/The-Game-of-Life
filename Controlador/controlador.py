from flask import Blueprint, request, jsonify, send_file
from Modelo.juegoDeLaVida import JuegoDeLaVida
from Modelo.patrones import get_lista_patrones, get_patron
import io
import json
import time

api = Blueprint("api", __name__)

salas = {}
salas_usuarios = {}
salas_actividad = {}
DEFAULT_ANCHO = 60
DEFAULT_LARGO = 35
TIMEOUT_INACTIVIDAD = 5 * 60  # 5 minutos


def get_o_crear_sala(room):
    if room not in salas:
        salas[room] = JuegoDeLaVida(DEFAULT_ANCHO, DEFAULT_LARGO)
        salas_usuarios[room] = 0
    registrar_actividad(room)
    return salas[room]


def registrar_actividad(room):
    salas_actividad[room] = time.time()


def sala_inactiva(room):
    ultima = salas_actividad.get(room, 0)
    return (time.time() - ultima) > TIMEOUT_INACTIVIDAD


def sala_vacia(room):
    return salas_usuarios.get(room, 0) <= 0


def limpiar_sala(room):
    salas.pop(room, None)
    salas_usuarios.pop(room, None)
    salas_actividad.pop(room, None)


@api.route("/api/estado")
def estado():
    room = request.args.get("room", "default")
    juego = get_o_crear_sala(room)
    return jsonify(juego.get_estado())


@api.route("/api/avanzar", methods=["POST"])
def avanzar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_o_crear_sala(room)
    tablero_vacio = juego.avanzar()
    return jsonify({"grid": juego.grid, "tablero_vacio": tablero_vacio, "paused": juego.paused})


@api.route("/api/toggle_celda", methods=["POST"])
def toggle_celda():
    data = request.json
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.toggle_celda(data["x"], data["y"])
    return jsonify({"grid": juego.grid})


@api.route("/api/borrar", methods=["POST"])
def borrar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_o_crear_sala(room)
    juego.borrar()
    return jsonify({"grid": juego.grid, "paused": juego.paused})


@api.route("/api/guardar", methods=["POST"])
def guardar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_o_crear_sala(room)
    data = juego.guardar()
    if data is None:
        return jsonify({"error": "No hay datos para guardar"}), 400
    buffer = io.BytesIO(data.encode("utf-8"))
    buffer.seek(0)
    return send_file(buffer, mimetype="application/json", as_attachment=True, download_name="juego_de_la_vida.json")


ALLOWED_EXTENSIONS = {".json"}
MAX_FILE_SIZE = 512 * 1024  # 512 KB


@api.route("/api/cargar", methods=["POST"])
def cargar():
    room = request.form.get("room", "default")

    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    import os
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Solo se permiten archivos .json"}), 400

    raw = file.read(MAX_FILE_SIZE + 1)
    if len(raw) > MAX_FILE_SIZE:
        return jsonify({"error": "El archivo excede el tamaño máximo (512 KB)"}), 400

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return jsonify({"error": "Archivo JSON inválido"}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "Formato de archivo no reconocido"}), 400

    allowed_keys = {"grid", "ancho", "largo"}
    if not set(data.keys()).issubset(allowed_keys):
        return jsonify({"error": "El archivo contiene campos no permitidos"}), 400

    juego = get_o_crear_sala(room)
    if juego.cargar(data):
        return jsonify(juego.get_estado())
    return jsonify({"error": "Formato de grilla inválido"}), 400


@api.route("/api/patrones")
def patrones():
    return jsonify(get_lista_patrones())


@api.route("/api/patron", methods=["POST"])
def colocar_patron():
    data = request.json
    room = data.get("room", "default")
    patron_id = data.get("patron_id")
    juego = get_o_crear_sala(room)
    celdas = get_patron(patron_id)
    if celdas is None:
        return jsonify({"error": "Patrón no encontrado"}), 404
    offset_x = data.get("offset_x", juego.ancho_grilla // 2 - 5)
    offset_y = data.get("offset_y", juego.largo_grilla // 2 - 5)
    juego.colocar_patron(celdas, offset_x, offset_y)
    return jsonify({"grid": juego.grid, "paused": juego.paused})


@api.route("/api/redimensionar", methods=["POST"])
def redimensionar():
    data = request.json
    room = data.get("room", "default")
    juego = get_o_crear_sala(room)
    juego.redimensionar(data["ancho"], data["largo"])
    return jsonify(juego.get_estado())
