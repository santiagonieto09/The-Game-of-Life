from flask import Blueprint, request, jsonify, send_file
from Modelo.patrones import get_lista_patrones, get_patron
import io
import json

api = Blueprint("api", __name__)

# Referencia al juego activo por sala; se inyecta desde app.py
salas = {}


def get_juego(room):
    from app import get_o_crear_sala
    return get_o_crear_sala(room)


@api.route("/api/estado")
def estado():
    room = request.args.get("room", "default")
    juego = get_juego(room)
    return jsonify(juego.get_estado())


@api.route("/api/avanzar", methods=["POST"])
def avanzar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_juego(room)
    tablero_vacio = juego.avanzar()
    return jsonify({"grid": juego.grid, "tablero_vacio": tablero_vacio, "paused": juego.paused})


@api.route("/api/toggle_celda", methods=["POST"])
def toggle_celda():
    data = request.json
    room = data.get("room", "default")
    juego = get_juego(room)
    juego.toggle_celda(data["x"], data["y"])
    return jsonify({"grid": juego.grid})


@api.route("/api/borrar", methods=["POST"])
def borrar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_juego(room)
    juego.borrar()
    return jsonify({"grid": juego.grid, "paused": juego.paused})


@api.route("/api/guardar", methods=["POST"])
def guardar():
    room = request.json.get("room", "default") if request.json else "default"
    juego = get_juego(room)
    data = juego.guardar()
    if data is None:
        return jsonify({"error": "No hay datos para guardar"}), 400
    buffer = io.BytesIO(data.encode("utf-8"))
    buffer.seek(0)
    return send_file(buffer, mimetype="application/json", as_attachment=True, download_name="juego_de_la_vida.json")


@api.route("/api/cargar", methods=["POST"])
def cargar():
    room = request.form.get("room", "default")
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400
    file = request.files["file"]
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        return jsonify({"error": "Archivo JSON inválido"}), 400
    juego = get_juego(room)
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
    juego = get_juego(room)
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
    juego = get_juego(room)
    juego.redimensionar(data["ancho"], data["largo"])
    return jsonify(juego.get_estado())
