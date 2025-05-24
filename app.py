
from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

orden_actual = ""

@app.route("/", methods=["POST"])
def chatgpt():
    global orden_actual
    data = request.json
    mensaje = data.get("mensaje", "")
    orden_actual = mensaje
    print(f"[POST] Orden recibida: {orden_actual}")
    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensaje}]
        )
        contenido = respuesta.choices[0].message.content
        print(f"[POST] Respuesta generada: {contenido[:60]}...")
        return jsonify({"respuesta": contenido})
    except Exception as e:
        print(f"[ERROR] OpenAI: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Servidor ChatGPT activo en Render"

@app.route("/orden", methods=["GET"])
def obtener_orden():
    global orden_actual
    if not orden_actual:
        orden_actual = "verifica_estado"
    print(f"[GET] Entregando orden actual: {orden_actual}")
    return jsonify({"orden": orden_actual})
