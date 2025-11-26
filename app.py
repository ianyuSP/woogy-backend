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

    # ===== CLASIFICACIÓN DE RIESGO POR MAGNITUD =====
    if 1.0 <= magnitud < 3.0:
        nivel = "muy bajo"
        color = "verde"
        intervalo = "1.0 – 2.9"
        mensajes = [
            "En Iztapalapa, un sismo tan leve rara vez causa daños. Únete a una zona estable dentro del inmueble y aprovecha para reconocer rutas de salida sin exponerte innecesariamente.",
            "En este rango el movimiento es casi imperceptible, pero en Iztapalapa puede sentirse un poco más. Mantente en un área despejada y revisa que muebles altos sigan bien asegurados.",
            "Aunque el riesgo es muy bajo, en Iztapalapa el suelo blando puede intensificar la sensación. Quédate en un punto firme del interior y verifica que no haya objetos sueltos.",
            "El movimiento es ligero, pero en Iztapalapa puede amplificarse. Permanece dentro, evita zonas con vidrios y usa el momento para detectar áreas seguras del hogar."
        ]

    elif 3.0 <= magnitud < 4.0:
        nivel = "bajo"
        color = "verde"
        intervalo = "3.0 – 3.9"
        mensajes = [
            "En Iztapalapa, un sismo así puede mover muebles y generar fisuras menores. Ubícate en zona segura dentro del inmueble y revisa después puertas y muros por cambios nuevos.",
            "Este nivel puede sentirse fuerte en Iztapalapa. Quédate lejos de ventanas y objetos pesados y revisa al terminar si estructuras ligeras muestran desprendimientos.",
            "Aunque el riesgo es bajo, en Iztapalapa la sacudida puede ser más notoria. Mantente en punto firme y observa si hay desniveles o grietas nuevas al finalizar.",
            "Puede causar caída de objetos mal fijados en Iztapalapa. Mantente alejado de repisas y cristales y revisa al terminar techos y bardas por seguridad."
        ]

    elif 4.0 <= magnitud < 6.0:
        nivel = "medio"
        color = "amarillo"   # riesgo medio -> amarillo
        intervalo = "4.0 – 5.9"
        mensajes = [
            "En Iztapalapa, un sismo de esta magnitud puede causar daños visibles. Permanece en zona segura dentro del inmueble y revisa después muros, techos y conexiones de gas.",
            "El suelo blando de Iztapalapa amplifica este tipo de sismo. Quédate alejado de ventanas y objetos pesados y verifica al terminar si hay grietas diagonales nuevas.",
            "Puede afectar acabados y estructuras débiles en Iztapalapa. Mantente en área segura, evita evacuar mientras tiembla y revisa después instalaciones y bardas.",
            "En Iztapalapa, estos sismos pueden provocar desprendimientos ligeros. Ubícate en punto firme, evita escaleras mientras dura y revisa al finalizar zonas elevadas."
        ]

    elif 6.0 <= magnitud < 7.0:
        nivel = "alto"
        color = "naranja"     # alto -> naranja
        intervalo = "6.0 – 6.9"
        mensajes = [
            "En Iztapalapa, un sismo fuerte puede generar daños serios. Protégete en zona estructural y al terminar mantente lejos de fachadas, postes y cables sueltos.",
            "Este nivel puede provocar colapsos parciales en Iztapalapa. Quédate en área segura sin acercarte a ventanas y evacúa solo cuando termine por rutas despejadas.",
            "En Iztapalapa, estructuras debilitadas pueden fallar. Protégete dentro del inmueble y al finalizar no reingreses si ves grietas grandes o deformaciones.",
            "El movimiento intenso puede dañar instalaciones en Iztapalapa. Permanece en zona segura y al terminar evita escaleras, techos sueltos y conexiones expuestas."
        ]

    else:  # 7.0 – 10.0
        nivel = "crítico"
        color = "rojo"
        intervalo = "7.0 – 10.0"
        mensajes = [
            "En Iztapalapa, un sismo extremo puede causar colapsos. Protégete en zona sólida y evacúa al terminar manteniéndote lejos de edificios, bardas y cables caídos.",
            "Este nivel representa riesgo severo en Iztapalapa. Resguárdate en punto firme y al finalizar aléjate de construcciones y espera indicaciones oficiales.",
            "En Iztapalapa, un sismo así puede volver inseguras muchas estructuras. Protégete dentro y evacúa cuando sea seguro, sin permanecer cerca de muros o postes.",
            "El riesgo estructural es muy alto en Iztapalapa. Mantén protección interna y al terminar busca espacios abiertos sin regresar por objetos personales."
        ]

    # ===== ELECCIÓN DE UNA SOLA RECOMENDACIÓN =====
    recomendacion = random.choice(mensajes)

    # ===== POSICIÓN NORMALIZADA PARA LA FLECHA (0 a 1) =====
    # magnitud 1  -> 0.0   |   magnitud 10 -> 1.0
    y_pos = (magnitud - 1.0) / 9.0

    # ===== MAPA SEGÚN COLOR =====
    if color == "verde":
        mapa = "mapa_verde.png"
    elif color == "amarillo":
        mapa = "mapa_amarillo.png"
    elif color == "naranja":
        mapa = "mapa_naranja.png"
    else:  # rojo
        mapa = "mapa_rojo.png"

    return jsonify({
        "recomendacion": recomendacion,
        "nivel": nivel,
        "color": color,
        "intervalo": intervalo,
        "magnitud": magnitud,
        "y_pos": round(y_pos, 3),
        "mapa": mapa
    })

if __name__ == "__main__":
    app.run()
