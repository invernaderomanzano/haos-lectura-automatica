
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor de gestión HAOS activo"

@app.route("/orden", methods=["POST"])
def recibir_orden():
    datos = request.json

    accion = datos.get("accion")
    archivo = datos.get("archivo")
    contenido = datos.get("contenido", "")
    destino = datos.get("destino", "")

    respuesta = {}

    try:
        if accion == "modificar_archivo" and archivo:
            with open(f"/config/{archivo}", "w") as f:
                f.write(contenido)
            respuesta["estado"] = f"Archivo {archivo} modificado correctamente."

        elif accion == "borrar_archivo" and archivo:
            ruta = f"/config/{archivo}"
            if os.path.exists(ruta):
                os.remove(ruta)
                respuesta["estado"] = f"Archivo {archivo} borrado."
            else:
                respuesta["error"] = f"Archivo {archivo} no encontrado."

        elif accion == "mover_archivo" and archivo and destino:
            origen = f"/config/{archivo}"
            destino_absoluto = f"/config/{destino}"
            if os.path.exists(origen):
                os.rename(origen, destino_absoluto)
                respuesta["estado"] = f"{archivo} movido a {destino}."
            else:
                respuesta["error"] = f"Archivo {archivo} no encontrado."

        else:
            respuesta["error"] = "Parámetros inválidos."

    except Exception as e:
        respuesta["error"] = str(e)

    return jsonify(respuesta)
