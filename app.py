from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API del simulador funcionando."

@app.route("/simular", methods=["POST"])
def simular():
    data = request.get_json()

    # Obtener magnitud
    try:
        magnitud = float(data.get("magnitude", 0))
    except:
        return jsonify({"error": "La magnitud debe ser un número."}), 400

    # Validación de magnitud REALISTA
    if magnitud < 0 or magnitud > 10:
        return jsonify({
            "error": "La magnitud ingresada no es realista. Usa valores entre 0 y 10."
        }), 400

    # Obtener piso
    piso = data.get("floor")
    # Obtener movimiento
    mov = data.get("movement")

    # Validar piso
    if piso not in ["baja", "media", "alta"]:
        return jsonify({"error": "Piso inválido."}), 400

    # Validar movimiento
    if mov not in ["oscilatorio", "trepidatorio", "mixto"]:
        return jsonify({"error": "Movimiento inválido."}), 400

    # Clasificación simple
    if magnitud < 3.5:
        mensajes = [
            "El sismo es leve. No suele causar daños, pero ubica tus zonas de seguridad.",
            "Movimiento ligero. Mantén la calma y revisa rutas de evacuación.",
            "Sismo leve. Revisa si hubo caída de objetos y continúa con precaución."
        ]
    elif magnitud < 6.5:
        mensajes = [
            "Sismo moderado. Aléjate de ventanas y objetos que puedan caer.",
            "Mantén la calma. Protégete bajo una mesa resistente.",
            "Evita usar elevadores. Refúgiate hasta que deje de temblar."
        ]
    else:
        mensajes = [
            "Riesgo de daños importantes. Refúgiate hasta que termine.",
            "En pisos altos, evacuar durante el sismo es peligroso. Refúgiate.",
            "El movimiento trepidatorio puede ser brusco y causar agrietamientos."
        ]

    # Elegir recomendación aleatoria
    recomendacion = random.choice(mensajes)

    return jsonify({
        "recomendacion": recomendacion,
        "magnitud": magnitud,
        "piso": piso,
        "movimiento": mov
    })

if __name__ == "__main__":
    app.run(debug=True)
