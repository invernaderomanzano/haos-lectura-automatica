from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return "Servidor ChatGPT activo"

@app.route("/orden", methods=["GET"])
def recibir_orden():
    return {"orden": "chatgpt_revisar_config"}

@app.route("/subida", methods=["POST"])
def recibir_archivos():
    archivos = request.files
    for nombre, archivo in archivos.items():
        contenido = archivo.read().decode("utf-8", errors="ignore")
        print(f"[{nombre}]")
        print(contenido[:200])  # Mostrar solo los primeros 200 caracteres por archivo
    return "Archivos recibidos correctamente", 200
