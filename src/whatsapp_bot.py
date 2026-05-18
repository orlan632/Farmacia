import logging
import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
PORT = int(os.getenv('PORT', 5000))

app = Flask(__name__)

# ------------------------------------------------------------
# MENÚ Y RESPUESTAS EN ESPAÑOL (ya traducido)
# ------------------------------------------------------------
MENU_OPTIONS = {
    '1': (f"🏪 Nuestra tienda queda en Calle Monagas, San Casimiro, Aragua\n\n"
          f"💟 ¡Aquí cuidamos de ti! 💟\n"
          f"✔️ Abrimos de Lunes a Domingo de 8:00 AM a 8:00 PM 🕜\n\n"
          f"📍 ¡Todo en perfumería y medicamentos con precios que caben en tu bolsillo! 💲\n\n"
          f"¡Contamos con atención personalizada!\n\n"
          f"Digita 1️⃣ para volver al Menú principal\n"
          f"Digita 2️⃣ para ver PROMOCIONES\n"),
    '2': (f"¡Bienvenido(a) al registro en Farmacia Centro Casa Blanca!\n\n"
          f"⚠️ Atención ⚠️\n"
          f"Para continuar con el registro es necesario que aceptes nuestra POLÍTICA DE PRIVACIDAD\n\n"
          f"Digita la opción elegida:\n\n"
          f"1️⃣ Acepto los términos\n"
          f"2️⃣ No acepto los términos\n"),
    '3': (f"🔥 ¡Entérate de las PROMOCIONES de la semana en nuestra página!\n\n"
          f"Síguenos en Instagram: @farmaciacasablanca\n\n"),
    '4': ("💬 Entendemos que estás presentando algunos síntomas.\n\n"
          "Cuéntanos más sobre ellos para poder sugerirte una medicación\n\n"
          "Digita 0️⃣ para volver al menú principal\n"),
    '5': (f"Algunas preguntas Frecuentes:\n\n"
          f"Digita el N° para recibir respuesta:\n\n"
          f"1️⃣ ¿Cuál es el horario de atención?\n"
          f"2️⃣ ¿Qué formas de pago aceptan?\n"
          f"3️⃣ ¿Hacen envíos a domicilio?\n"
          f"4️⃣ ¿Necesito receta para comprar antibióticos?\n"
          f"5️⃣ ¿Aceptan recetas digitales?\n"
          f"6️⃣ ¿Aplican vacunas en la farmacia?\n"
          f"7️⃣ ¿Miden la presión arterial y la glicemia?\n"
          f"0️⃣ Volver al menú principal\n\n"),
    '6': "🔔 Otras opciones: hablar con un asesor, ubicación en el mapa, etc."
}

FAQ_ANSWERS = {
    '1': "Nuestra farmacia atiende de Lunes a Domingo, de 8:00 AM a 8:00 PM.",
    '2': "Aceptamos efectivo, tarjetas de crédito y débito, y PIX.",
    '3': "Sí, hacemos envíos a domicilio en San Casimiro. Consulta la disponibilidad para tu zona.",
    '4': "Sí, solo vendemos antibióticos con receta médica.",
    '5': "Sí, aceptamos recetas digitales válidas según la legislación.",
    '6': "Sí, aplicamos vacunas contra la gripe, covid y otras.",
    '7': "Sí, medimos la presión arterial y la glicemia de forma gratuita."
}

WELCOME_MESSAGE = (
    "👋 ¡Hola! Bienvenido(a) a Farmacia Centro Casa Blanca 👋\n\n"
    "📍 Tu Farmacia de confianza en San Casimiro, Aragua 📍\n\n"
    "Nuestro objetivo es ayudarte a elegir el medicamento ideal para cada situación.\n\n"
    "¿Tienes algún síntoma? ¡Describe lo que sientes y te indicaremos la medicación correcta!\n\n"
    "NO INDICAMOS MEDICACIÓN CON PRESCRIPCIÓN MÉDICA\n\n\n"
    "O digita el número de la opción:\n\n"
    "1️⃣ Conoce nuestra tienda y horarios 🏥\n"
    "2️⃣ Registrarse en la tienda 🕜\n"
    "3️⃣ Promociones 💯\n"
    "4️⃣ Tengo síntomas, necesito recomendaciones 💊\n"
    "5️⃣ Preguntas Frecuentes ❔\n"
    "6️⃣ Sugerencias/Reclamos 📢\n\n"
    "💟 ¿Cómo podemos ayudarte hoy? 💟"
)

def generar_respuesta(mensaje):
    """Genera una respuesta basada en el texto ingresado por el usuario"""
    texto = mensaje.strip()
    
    # Menú principal
    if texto in MENU_OPTIONS:
        if texto == '5':  # Preguntas frecuentes
            return MENU_OPTIONS['5']
        return MENU_OPTIONS[texto]
    
    # FAQ submenú
    if texto in FAQ_ANSWERS:
        return FAQ_ANSWERS[texto] + "\n\nDigita otro número o 0️⃣ para volver al menú principal."
    
    # Síntomas
    if texto == '4':
        return MENU_OPTIONS['4']
    
    # Volver al menú principal
    if texto == '0':
        return WELCOME_MESSAGE
    
    # Respuesta por defecto
    return WELCOME_MESSAGE

# ------------------------------------------------------------
# RUTAS
# ------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    """Página principal con chat simple"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Farmacia Centro Casa Blanca - Chat</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; }
            #chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #f9f9f9; }
            .msg { margin: 5px 0; }
            .user { color: blue; }
            .bot { color: green; }
            input[type="text"] { width: 80%; padding: 10px; }
            button { padding: 10px 20px; }
        </style>
    </head>
    <body>
        <h2>Farmacia Centro Casa Blanca 💊</h2>
        <div id="chat"></div>
        <input type="text" id="mensaje" placeholder="Escribe un número o tu síntoma...">
        <button onclick="enviar()">Enviar</button>
        <script>
            function addMessage(text, sender) {
                var chat = document.getElementById('chat');
                var msg = document.createElement('div');
                msg.className = 'msg ' + sender;
                msg.innerText = text;
                chat.appendChild(msg);
                chat.scrollTop = chat.scrollHeight;
            }
            function enviar() {
                var input = document.getElementById('mensaje');
                var texto = input.value;
                if (!texto) return;
                addMessage(texto, 'user');
                input.value = '';
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mensaje: texto})
                })
                .then(r => r.json())
                .then(d => addMessage(d.respuesta, 'bot'));
            }
            document.getElementById('mensaje').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') enviar();
            });
        </script>
    </body>
    </html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint del chatbot"""
    data = request.json
    mensaje = data.get('mensaje', '')
    respuesta = generar_respuesta(mensaje)
    return jsonify({"respuesta": respuesta})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

def main():
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()
