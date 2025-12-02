from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Simulador activo"})

@app.route("/simular", methods=["POST"])
def simular():
    data = request.get_json(silent=True) or {}

    # ===== VALIDACIÓN MAGNITUD =====
    try:
        magnitud = float(data.get("magnitude", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "La magnitud debe ser un número."}), 400

    if magnitud < 1.0 or magnitud > 10.0:
        return jsonify({
            "error": "La magnitud ingresada no es realista. Usa valores entre 1.0 y 10.0."
        }), 400

    # ===== VALIDACIÓN PISO Y MOVIMIENTO =====
    piso = data.get("floor")
    movimiento = data.get("movement")

    if piso not in ("baja", "media", "alta"):
        return jsonify({"error": "Piso inválido."}), 400

    if movimiento not in ("oscilatorio", "trepidatorio", "mixto"):
        return jsonify({"error": "Movimiento inválido."}), 400

    # ===== CLASIFICACIÓN DE RIESGO =====
    if 1.0 <= magnitud < 3.0:
        nivel = "muy bajo"
        mensajes = [
            "En Iztapalapa, un sismo tan leve rara vez causa daños. Permanece en un punto estable dentro del inmueble.",
            "Movimiento casi imperceptible. Mantén calma y revisa objetos altos por si se movieron ligeramente.",
            "Aunque el riesgo es muy bajo, en zonas de suelo blando puede sentirse un poco más. Permanece en zona segura.",
            "El movimiento es ligero pero perceptible. Mantente alejado de vidrios y objetos que puedan caer."
        ]

    elif 3.0 <= magnitud < 4.0:
        nivel = "bajo"
        mensajes = [
            "Puede mover muebles ligeros y generar fisuras pequeñas. Ubícate en zona de seguridad dentro del inmueble.",
            "Quédate lejos de ventanas y revisa estructuras ligeras al finalizar el sismo.",
            "Aunque es un nivel bajo, el movimiento puede sentirse fuerte en suelos blandos. Permanece firme.",
            "Puede causar caída de objetos mal fijados. Al terminar revisa repisas y techos ligeros."
        ]

    elif 4.0 <= magnitud < 6.0:
        nivel = "medio"
        mensajes = [
            "Este nivel puede generar daños visibles. Permanece en un punto seguro y revisa muros y techos después.",
            "La sacudida puede amplificarse. Evita ventanas y objetos pesados durante el movimiento.",
            "Puede afectar acabados y estructuras débiles. Quédate en zona segura sin evacuar hasta que termine.",
            "Puede haber desprendimientos ligeros. Al finalizar revisa zonas elevadas y posibles grietas."
        ]

    elif 6.0 <= magnitud < 7.0:
        nivel = "alto"
        mensajes = [
            "Un sismo fuerte puede causar daños severos. Protégete en zona estructural y evita salir mientras tiembla.",
            "Puede provocar colapsos parciales. Evacúa solo cuando termine, por rutas despejadas.",
            "Estructuras debilitadas pueden fallar. No reingreses si notas grietas grandes o deformaciones.",
            "El movimiento intenso puede dañar instalaciones. Evita techos sueltos y conexiones expuestas."
        ]

    else:  # 7.0 – 10.0
        nivel = "crítico"
        mensajes = [
            "Un sismo extremo puede causar colapsos. Protégete en zona sólida y evacúa al finalizar.",
            "Riesgo severo de daños. Busca un punto firme durante el movimiento y después aléjate de estructuras.",
            "Muchas estructuras pueden volverse inseguras. Evacúa cuando sea seguro, sin acercarte a muros altos.",
            "Evita permanecer cerca de edificios tras el movimiento. Mantente en espacios abiertos."
        ]

    recomendacion = random.choice(mensajes)

    return jsonify({
        "recomendacion": recomendacion,
        "nivel": nivel,
        "magnitud": magnitud
    })

if __name__ == "__main__":
    app.run()
