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

    # ===== CLASIFICACIÓN DE RIESGO (MENSAJE BASE POR MAGNITUD) =====
    if 1.0 <= magnitud < 3.0:
        nivel = "muy bajo"
        mensajes = [
            "En Iztapalapa, un sismo tan leve rara vez causa daños, pero el suelo blando puede amplificar ligeramente la sensación. Permanece en un punto estable dentro del inmueble.",
            "El movimiento es casi imperceptible, aunque en zonas de suelo blando como Iztapalapa puede notarse un poco más. Mantén la calma y revisa objetos altos que pudieran haberse movido.",
            "Aunque el riesgo es muy bajo, un sismo leve puede servir para identificar zonas seguras y rutas de salida en tu vivienda en Iztapalapa. Aprovecha para observar si hay muebles inestables.",
            "El movimiento es ligero pero perceptible en algunos casos. Permanece en una zona segura y evita colocarte junto a vidrios u objetos que puedan caer en futuros sismos."
        ]

    elif 3.0 <= magnitud < 4.0:
        nivel = "bajo"
        mensajes = [
            "Un sismo de este rango puede mover muebles ligeros y generar fisuras pequeñas, especialmente en Iztapalapa por la amplificación del suelo. Ubícate en una zona de seguridad dentro del inmueble.",
            "El movimiento puede sentirse moderado y causar caída de objetos mal fijados. Quédate lejos de ventanas y revisa después muros ligeros y repisas.",
            "Aunque el nivel de riesgo sigue siendo bajo, en suelos blandos la sacudida puede ser notoria. Permanece firme en un punto seguro y verifica si hay desprendimientos menores.",
            "Este tipo de sismo puede afectar acabados superficiales sin comprometer la estructura principal. Revisa techos ligeros, repisas y áreas con elementos inestables."
        ]

    elif 4.0 <= magnitud < 6.0:
        nivel = "medio"
        mensajes = [
            "Este tipo de sismo puede generar daños visibles en muros o acabados, sobre todo en construcciones vulnerables de Iztapalapa. Permanece en la zona de menor riesgo y revisa techos y muros al finalizar.",
            "La sacudida puede amplificarse notablemente en suelos blandos, provocando caída de materiales ligeros. Evita ventanas y objetos pesados mientras permanezcas en el interior.",
            "Puede afectar estructuras débiles y causar fisuras diagonales o desprendimientos. Mantente en un punto seguro sin evacuar hasta que el movimiento termine por completo.",
            "En este rango pueden darse desprendimientos ligeros y daños en acabados. Al finalizar el sismo, inspecciona con precaución grietas nuevas o deformaciones inusuales."
        ]

    elif 6.0 <= magnitud < 7.0:
        nivel = "alto"
        mensajes = [
            "Un sismo fuerte puede causar daños severos y caída de elementos estructurales en zonas como Iztapalapa. Protégete en un punto sólido del inmueble y evita evacuar mientras haya movimiento.",
            "Este nivel puede provocar colapsos parciales en construcciones vulnerables. Permanece en un área segura sin acercarte a ventanas y evacúa solo cuando el movimiento haya terminado.",
            "Estructuras debilitadas pueden fallar tras un sismo de esta magnitud. No reingreses a un inmueble si observas grietas grandes, desplomes o ruidos estructurales anormales.",
            "El movimiento intenso puede dañar instalaciones eléctricas, de gas o techos sueltos. Al concluir el sismo, evita escaleras, áreas elevadas y zonas con conexiones expuestas."
        ]

    else:  # 7.0 – 10.0
        nivel = "crítico"
        mensajes = [
            "Un sismo extremo puede causar colapsos totales o severos, especialmente en suelos blandos. Protégete en la zona más resistente disponible y prepárate para evacuar en cuanto el movimiento termine.",
            "En este nivel el riesgo estructural es muy alto y muchas construcciones pueden volverse inseguras. Mantente protegido durante el sismo y al salir aléjate de edificios, bardas y postes.",
            "Un evento de esta magnitud puede dejar graves daños en infraestructura y servicios. Evacúa hacia espacios abiertos sin permanecer cerca de muros altos, fachadas o cables.",
            "Tras un sismo extremo es posible que existan réplicas significativas y riesgos de nuevos colapsos. No regreses al inmueble y mantente atento a las indicaciones de Protección Civil."
        ]

    base = random.choice(mensajes)

    # ===== COMPLEMENTO SEGÚN PISO =====
    textos_piso = {
        "baja": (
            "Si te encuentras en planta baja, evita acercarte a ventanales, bardas exteriores u objetos que puedan caer, "
            "y considera evacuar solo cuando el movimiento haya cesado y la ruta sea segura."
        ),
        "media": (
            "En pisos intermedios, mantente alejado de escaleras, ventanas y balcones, y espera a que el sismo termine "
            "antes de intentar evacuar siguiendo las rutas establecidas."
        ),
        "alta": (
            "En pisos altos el movimiento suele amplificarse, por lo que es más seguro replegarte a la zona de menor riesgo "
            "lejos de ventanas y muros divisorios, sin usar elevadores durante el sismo."
        ),
    }

    # ===== COMPLEMENTO SEGÚN TIPO DE MOVIMIENTO =====
    textos_movimiento = {
        "oscilatorio": (
            "El movimiento oscilatorio desplaza lateralmente muebles y personas, así que mantente lejos de libreros, repisas "
            "y paredes largas que puedan fracturarse o desprender objetos."
        ),
        "trepidatorio": (
            "El movimiento trepidatorio genera sacudidas verticales que pueden desprender plafones, lámparas y objetos suspendidos, "
            "por lo que debes evitar permanecer debajo de ellos y proteger tu cabeza."
        ),
        "mixto": (
            "Un movimiento mixto combina sacudidas laterales y verticales, de modo que es importante elegir un punto firme, "
            "proteger cabeza y cuello y alejarte de cualquier objeto inestable."
        ),
    }

    complemento_piso = textos_piso[piso]
    complemento_mov = textos_movimiento[movimiento]

    recomendacion = f"{base} {complemento_piso} {complemento_mov}"

    return jsonify({
        "recomendacion": recomendacion,
        "nivel": nivel,
        "magnitud": magnitud
    })

if __name__ == "__main__":
    app.run()

