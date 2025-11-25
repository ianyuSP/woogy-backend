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
    data = request.get_json(silent=True) or {}

    #valida la magnitud
    try:
        magnitud = float(data.get("magnitude", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "La magnitud debe ser un número."}), 400

    #Erro en caso de que se ingresen datos no permitidos.
    if magnitud < 1.0 or magnitud > 10.0:
        return jsonify({
            "error": "La magnitud ingresada no es realista. Usa valores entre 1.0 y 10.0."
        }), 400

    # Valida el piso y el movimiento
    piso = data.get("floor")
    movimiento = data.get("movement")

    if piso not in ("baja", "media", "alta"):
        return jsonify({"error": "Piso inválido."}), 400

    if movimiento not in ("oscilatorio", "trepidatorio", "mixto"):
        return jsonify({"error": "Movimiento inválido."}), 400

    if 1.0 <= magnitud < 3.0:
        nivel = "muy bajo"
        color = "verde"
        intervalo = "1.0 – 2.9"
        base_msgs = [
            "En este rango la mayoría de los sismos solo se perciben ligeramente, incluso en suelos blandos como los de Iztapalapa. Aun así, aprovecha para identificar dentro de tu casa las columnas y muros de carga que servirán como zonas de menor riesgo en un sismo más fuerte.",
            "Aunque la magnitud es baja, el suelo lacustre de Iztapalapa puede hacer que el movimiento se sienta más de lo normal. Usa estos eventos leves para practicar tu ruta de evacuación y revisar que muebles altos, libreros y televisores estén bien asegurados."
        ]
    elif 3.0 <= magnitud < 4.0:
        nivel = "bajo"
        color = "verde"
        intervalo = "3.0 – 3.9"
        base_msgs = [
            "Este tipo de sismo suele provocar alarma pero pocos daños, aunque en Iztapalapa el suelo blando amplifica la sacudida. Dentro del inmueble, ubícate junto a un muro de carga o columna y verifica después si hay grietas finas nuevas en los muros o desniveles en el piso.",
            "En Iztapalapa, construcciones con autoconstrucción o ampliaciones pueden resentir más estos sismos. Durante el movimiento, mantente lejos de ventanas y muebles pesados; al terminar, revisa si puertas y ventanas se atoran, ya que puede ser un indicio de desplazamientos leves en la estructura.",
            "Este nivel de sismo difícilmente provoca colapsos, pero sí caída de objetos mal fijados. En viviendas de Iztapalapa, es buena práctica asegurar repisas, televisores y vitrinas y revisar si no hay desprendimientos ligeros de aplanado o plafones después del evento.",
            "En suelos blandos como los de Iztapalapa, incluso sismos moderados pueden aumentar la sensación de mareo. Si te sucede, siéntate en una zona de menor riesgo dentro del inmueble, recupérate y revisa posteriormente muros y losas en busca de marcas o fisuras nuevas."
        ]
    elif 4.0 <= magnitud < 5.0:
        nivel = "medio"
        color = "naranja"
        intervalo = "4.0 – 4.9"
        base_msgs = [
            "En Iztapalapa, un sismo de esta magnitud puede provocar daño ligero en bardas y acabados, sobre todo en casas autoconstruidas. Mientras tiembla, ubícate junto a una columna o muro de carga, lejos de ventanas; al terminar, revisa bardas perimetrales, azoteas y techos ligeros por si presentan desprendimientos.",
            "Este rango de magnitud, amplificado por el suelo lacustre de Iztapalapa, puede cuartear muros mal reforzados. Durante el sismo evita evacuar; al terminar, recorre tu vivienda buscando grietas diagonales grandes, inclinaciones de muros o hundimientos del piso y reporta anomalías a Protección Civil.",
            "En edificios de Iztapalapa, los sismos moderados pueden afectar acabados, losetas y plafones. Mientras dura el movimiento, mantente en una zona de menor riesgo lejos de cristales; después, revisa pasillos, escaleras y plafones por posibles desprendimientos antes de circular bajo ellos.",
            "Este tipo de sismo puede dañar conexiones de gas y agua en viviendas con instalaciones viejas. Cuando termine el movimiento, antes de encender luces o flamas, verifica si hay olor a gas, escucha fugas y cierra llaves principales si notas algo anormal."
        ]
    elif 5.0 <= magnitud < 6.0:
        nivel = "medio"
        color = "naranja"
        intervalo = "5.0 – 5.9"
        base_msgs = [
            "En Iztapalapa, un sismo de esta magnitud puede generar daños moderados en construcciones vulnerables. Durante la sacudida no uses escaleras ni elevadores; al terminar, evacúa por las rutas señaladas y revisa fachadas, bardas altas y azoteas, evitando pasar pegado a ellas por riesgo de desprendimientos.",
            "Este rango de sismo, sumado al suelo blando de Iztapalapa, puede abrir grietas importantes en muros y losas sin buen refuerzo. Tras el evento, revisa columnas, trabes y muros que sostienen el edificio; si observas grietas anchas, deformaciones o desplomes, no reingreses al inmueble y repórtalo.",
            "En viviendas con ampliaciones ligeras en azoteas, frecuentes en Iztapalapa, la vibración puede concentrarse en esos niveles. Si detectas hundimientos, fisuras profundas o separación entre muros y losas, mantente fuera de esas áreas y solicita una revisión técnica antes de volver a habitarlas.",
            "Un sismo así puede afectar escaleras mal construidas o con refuerzo deficiente. Después del movimiento revisa descansos, trabes de apoyo y barandales; si notas vibración anormal, fracturas o pérdida de apoyo, evita usarlas y busca una ruta alterna o espera indicaciones de Protección Civil."
        ]
    elif 6.0 <= magnitud < 7.0:
        nivel = "alto"
        color = "rojo"
        intervalo = "6.0 – 6.9"
        base_msgs = [
            "En Iztapalapa, un sismo fuerte amplificado por el suelo lacustre puede provocar daños serios en edificios irregulares. Durante el movimiento, colócate junto a un muro de carga o columna gruesa, lejos de ventanas, y protege cabeza y cuello con mochila, cojín o brazos antes de pensar en evacuar.",
            "Este nivel de sismo puede tirar bardas completas, anuncios y partes de fachadas en Iztapalapa. Mientras tiembla no corras hacia la calle; cuando termine, evacúa usando las rutas marcadas y mantente alejado de muros altos, postes, tanques de gas y cables caídos.",
            "Con esta magnitud, las estructuras débiles o con grietas previas en Iztapalapa pueden colapsar parcialmente. Si al terminar observas columnas cortadas, losas desprendidas o muros muy fracturados, no intentes rescatar objetos personales ni dormir dentro del inmueble; repórtalo como zona de alto riesgo.",
            "Los sismos fuertes pueden dañar seriamente instalaciones de gas y electricidad en conjuntos habitacionales antiguos. Tras el movimiento, cierra llaves de gas y baja pastillas eléctricas si es seguro hacerlo; no enciendas interruptores ni aparatos hasta asegurarte de que no hay fugas ni cortocircuitos."
        ]
    else:  # 7.0 a 10.0
        nivel = "alto"
        color = "rojo"
        intervalo = "7.0 – 10.0"
        base_msgs = [
            "En un sismo muy fuerte, el suelo blando de Iztapalapa puede amplificar la sacudida al punto de provocar colapsos parciales o totales en construcciones vulnerables. Durante el evento, protégete en la zona estructuralmente más sólida del lugar y al finalizar aléjate lo más pronto posible de edificios y bardas dañadas.",
            "Para magnitudes tan altas, edificaciones sin diseño sismo–resistente en Iztapalapa pueden volverse inhabitables. Si observas grandes grietas en forma de X, pisos hundidos o techos separados de los muros, considera el inmueble como inseguro y espera valoración de especialistas antes de volver a entrar.",
            "En estas condiciones, los escombros, vidrios y cables caídos son tan peligrosos como el propio sismo. Tras evacuar, permanece en espacios abiertos alejados de marquesinas, espectaculares y árboles grandes, y sigue únicamente información oficial en radio, TV o canales de Protección Civil.",
            "Un sismo muy intenso puede agravar hundimientos diferenciales y agrietamientos del terreno en Iztapalapa. Evita circular en vehículo por calles donde notes deformaciones del pavimento, fracturas en banquetas o colapsos de drenaje, y reporta de inmediato estas zonas a las autoridades."
        ]

    base_text = random.choice(base_msgs)

    # AJUSTES POR PISO
    if piso == "baja":
        frase_piso = (
            "En planta baja evita salir corriendo mientras tiembla; muchas lesiones "
            "ocurren en puertas y bajo bardas que colapsan hacia la banqueta. Si decides evacuar, "
            "hazlo solo cuando el movimiento termine, usando rutas despejadas y manteniéndote "
            "alejado de portones pesados y ventanales hacia la calle."
        )
    elif piso == "media":
        frase_piso = (
            "En un piso intermedio, permanece dentro durante el sismo y no intentes bajar por las escaleras. "
            "Al terminar, revisa descansos, muros cercanos y barandales en busca de grietas o desprendimientos "
            "antes de utilizarlas como ruta de salida."
        )
    else:  # alta
        frase_piso = (
            "En pisos altos el balanceo será más notorio; evita acercarte a balcones, cristalera exterior "
            "o barandales ligeros. Espera a que disminuya el movimiento para iniciar el descenso y verifica "
            "que las escaleras no presenten daños visibles antes de seguir bajando."
        )

    #AJUSTES POR TIPO DE MOVIMIENTO
    if movimiento == "trepidatorio":
        frase_mov = (
            "Cuando el movimiento es trepidatorio, los impactos verticales afectan más a columnas, losas y azoteas pesadas. "
            "Procura no situarte bajo tanques de agua, marquesinas o plafones agrietados, y observa después si hay "
            "fisuras nuevas en los puntos donde descansan las vigas."
        )
    elif movimiento == "oscilatorio":
        frase_mov = (
            "Con movimiento oscilatorio, se incrementa el riesgo de que caigan lámparas, libreros, televisores y objetos colgantes. "
            "Mantente lejos de estos elementos y, al terminar, revisa que no hayan quedado inestables sobre repisas o muebles altos."
        )
    else:  # mixto
        frase_mov = (
            "Un movimiento mixto combina sacudidas horizontales y verticales, por lo que tanto los elementos pesados en azotea "
            "como las fachadas y ventanas pueden dañarse. Elige siempre la zona más despejada y estructuralmente firme del lugar "
            "y evita permanecer pegado a muros exteriores o cristales."
        )

    recomendacion = f"{base_text} {frase_piso} {frase_mov}"

    return jsonify({
        "recomendacion": recomendacion,
        "nivel": nivel,
        "color": color,
        "intervalo": intervalo,
        "magnitud": magnitud
    })

if __name__ == "__main__":
    app.run(debug=True)
