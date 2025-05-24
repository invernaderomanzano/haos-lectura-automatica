from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

orden_actual = ""

@app.route("/", methods=["POST"])
def chatgpt():
    global orden_actual
    data = request.json
    mensaje = data.get("mensaje", "")
    orden_actual = mensaje
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensaje}]
        )
        contenido = respuesta["choices"][0]["message"]["content"]
        return jsonify({"respuesta": contenido})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Servidor ChatGPT activo en Render"

@app.route("/orden", methods=["GET"])
def obtener_orden():
    global orden_actual
    return jsonify({"orden": orden_actual})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
