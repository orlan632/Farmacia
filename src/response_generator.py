from nlp_processor import NLPProcessor
from context_manager import ContextManager
from models import Product, FAQ, Conversation
import json

with open(r'C:\Users\syafo\VIX_Intelligence\Farmacia\json\sintomas_med.json', 'r', encoding='utf-8') as f:
    known_symptoms = json.load(f)

instagram_link = "https://www.instagram.com/xxxxx"
instagram_link_promos = "https://www.instagram.com/xxxxx"

MENU_OPTIONS = {
    '1': (f"🏪 Nuestra tienda queda en XXXX, n° 123 - XXXX - XX\n\n"
          f"💟 ¡Aquí cuidamos de ti! 💟\n"
          f"✔️ Abrimos de Lunes a Sábado de 08h a 22h 🕜\n\n"
          f"📍 ¡Todo en perfumería y medicamentos con precios que caben en tu bolsillo! 💲\n\n"
          f"¡Contamos con estacionamiento para PCD, además de atención personalizada!\n\n"
          f"\n"
          f"¡Visita nuestra página en Instagram y entérate de las mejores promociones del mercado!"
          f"\n\n"
          f"{instagram_link}\n\n"
          f"Digita 1️⃣ para volver al Menú principal\n"
          f"Digita 2️⃣ para ver PROMOCIONES\n"
         ),
    '2': (f"¡Bienvenido(a) al registro en Farmacia XXXX!\n\n"
          f"⚠️ Atención ⚠️\n"
          f"Para continuar con el registro es necesario que aceptes nuestra POLÍTICA DE PRIVACIDAD, conforme a lo establecido por la Ley General de Protección de Datos (LGPD)\n\n"
          f"Accede:\n"
          f"https:/www.xxxxx.com.br/institucional/politica-de-privacidade\n\n\n"
          f"Digita la opción elegida:\n\n"
          f"1️⃣ Acepto los términos\n"
          f"2️⃣ No acepto los términos"
          ),
    '3': (f"🔥 ¡Entérate de las PROMOCIONES de la semana en nuestra página!\n\n"
          f"{instagram_link_promos}\n\n"
          ),
    '4': ("💬 Entendemos que estás presentando algunos síntomas.\n\n Cuéntanos más sobre ellos para poder sugerirte una medicación\n\n"
          "Digita 0️⃣ para volver al menú principal"),
    '5': (f"Algunas preguntas Frecuentes en nuestro canal:\n\n"
          f"Digita el N° para recibir respuesta:\n\n"
          f"1️⃣ ¿Cuál es el horario de atención de la farmacia?\n\n"
          f"2️⃣ ¿Qué formas de pago aceptan?\n\n"
          f"3️⃣ ¿Hacen envíos a domicilio?\n\n"
          f"4️⃣ ¿Necesito receta para comprar antibióticos?\n\n"
          f"5️⃣ ¿Aceptan recetas digitales?\n\n"
          f"6️⃣ ¿Aplican vacunas en la farmacia?\n\n"
          f"7️⃣ ¿Miden la presión arterial y la glicemia?\n\n"
          f"8️⃣ ¿Es posible registrarse para recibir promociones?\n\n"
          f"9️⃣ ¿Venden medicamentos manipulados?\n\n"
          f"1️⃣0️⃣ ¿Puedo cambiar un producto comprado en la farmacia?\n\n"
          f"1️⃣1️⃣ ¿Cómo funciona el programa de fidelidad de la farmacia?\n\n"
          f"1️⃣2️⃣ ¿Tienen estacionamiento para clientes?\n\n"
          f"1️⃣3️⃣ ¿Hay descuento para convenios o planes de salud?\n\n"
          f"1️⃣4️⃣ ¿Cuáles son los canales de atención de la farmacia?\n\n\n"
          f"Digita 0️⃣ para regresar al menú principal."
          ),
    '6': "🔔 Otras opciones: hablar con un asesor, ubicación en el mapa, etc."
}

class ResponseGenerator:
    """Generador de respuestas para el bot de farmacia"""

    @staticmethod
    def get_welcome_message(first_name=None):
        """Retorna el mensaje de bienvenida personalizado"""
        num_loja = 27999999999
        name_greeting = f", {first_name}" if first_name else ""
        
        return (
            f"👋 ¡Hola{name_greeting}! 👋\n\n"
            "📍 ¡Bienvenido(a) a Salud Virtual📍\n🔹 Tu Farmacéutico Virtual en asociación con Farmacia XXX 🔹\n\n" 
            "Nuestro objetivo es ayudarte a elegir el medicamento ideal para cada situación.\n\n"
            "¿Tienes algún síntoma? ¡Describe lo que sientes y te indicaremos la medicación correcta!\n\n"
            "NO INDICAMOS MEDICACIÓN CON PRESCRIPCIÓN MÉDICA\n\n\n"
            "O digita el número de la opción:\n\n"
            "1️⃣ Conoce nuestra tienda y horarios 🏥\n\n"
            "2️⃣ Registrarse en la tienda 🕜\n\n"
            "3️⃣ Entérate de las PROMOCIONES 💯\n\n"
            "4️⃣ Tengo síntomas, necesito recomendaciones 💊\n\n"
            "5️⃣ Preguntas Frecuentes ❔\n\n"
            "6️⃣ Sugerencias/Reclamos 📢\n\n\n"
            f"Este es un canal de atención automatizado, para hablar con un vendedor llama a nuestra tienda:\n\n"
            f"{num_loja}\n\n"
            "💟 ¿Cómo podemos ayudarte hoy? 💟"
        )

    @staticmethod
    def _get_main_menu_text():
        """Retorna el texto del menú principal"""
        return ResponseGenerator.get_welcome_message()

    @staticmethod
    def generate_response(user_id, platform, message_text):
        """Genera una respuesta basada en el mensaje del usuario y el contexto"""
        Conversation.save_message(user_id, platform, message_text, is_from_user=True)

        opcao = message_text.strip()
        current_context = ContextManager.get_current_context(user_id, platform)

        # Tratamiento del submenú de la opción '1' (información de la tienda)
        if current_context == ContextManager.CONTEXT_TYPES.get('INFO_LOJA_SUBMENU'):
            if opcao == '1':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['MAIN_MENU'], {})
                resposta = ResponseGenerator._get_main_menu_text()
            elif opcao == '2':
                resposta = MENU_OPTIONS['3']
            else:
                resposta = "Por favor, digita 1️⃣ para volver al Menú principal o 2️⃣ para ver PROMOCIONES."
            
            Conversation.save_message(user_id, platform, resposta, is_from_user=False)
            return resposta

        # Si está en el menú principal y digita una opción numérica
        elif current_context == ContextManager.CONTEXT_TYPES.get('MAIN_MENU') and opcao in MENU_OPTIONS:
            if opcao == '1':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['INFO_LOJA_SUBMENU'], {})
                resposta = MENU_OPTIONS['1']
            elif opcao == '2':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['WAITING_LGPD_RESPONSE'], {})
                resposta = MENU_OPTIONS['2']
            elif opcao == '3':
                resposta = MENU_OPTIONS['3']
            elif opcao == '4':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['WAITING_SYMPTOM'], {})
                resposta = MENU_OPTIONS['4']
            elif opcao == '5':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['FAQ'], {})
                resposta = MENU_OPTIONS['5']
            elif opcao == '6':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['OTHER_OPTIONS'], {})
                resposta = MENU_OPTIONS['6']

            Conversation.save_message(user_id, platform, resposta, is_from_user=False)
            return resposta

        # Tratamiento de respuestas dentro del contexto WAITING_LGPD_RESPONSE
        elif current_context == ContextManager.CONTEXT_TYPES.get('WAITING_LGPD_RESPONSE'):
            if opcao == '1':
                resposta = "Gracias por aceptar nuestra Política de Privacidad. Ahora podemos continuar con tu registro."
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['MAIN_MENU'], {})
            elif opcao == '2':
                resposta = "Necesitas aceptar la Política de Privacidad para continuar. Si deseas, digita 1️⃣ para aceptar."
            else:
                resposta = "Por favor, digita 1️⃣ para aceptar o 2️⃣ para rechazar la Política de Privacidad."

            Conversation.save_message(user_id, platform, resposta, is_from_user=False)
            return resposta

        # Tratamiento del contexto FAQ
        elif current_context == ContextManager.CONTEXT_TYPES.get('FAQ'):
            faq_answers = {
                '1': "Nuestra farmacia atiende de lunes a sábado, de 08h a 22h.",
                '2': "Aceptamos efectivo, tarjetas de crédito y débito, y PIX.",
                '3': "Sí, hacemos envíos a domicilio en la ciudad. Consulta la disponibilidad para tu zona.",
                '4': "Sí, solo vendemos antibióticos con receta médica.",
                '5': "Sí, aceptamos recetas digitales válidas según la legislación.",
                '6': "Sí, aplicamos vacunas contra la gripe, covid y otras.",
                '7': "Sí, medimos la presión arterial y la glicemia de forma gratuita.",
                '8': "Sí, puedes registrarte para recibir nuestras promociones por WhatsApp y correo electrónico.",
                '9': "No, no trabajamos con medicamentos manipulados.",
                '10': "Sí, el cambio de productos se puede hacer según nuestra política de cambios en hasta 7 días.",
                '11': "Nuestro programa de fidelidad ofrece descuentos y puntos en compras.",
                '12': "Sí, tenemos estacionamiento gratuito para clientes.",
                '13': "Ofrecemos descuentos para convenios asociados. Consulta en la tienda.",
                '14': "Atendemos por teléfono, WhatsApp y de forma presencial en la tienda."
            }
            if opcao == '0':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['MAIN_MENU'], {})
                resposta = ResponseGenerator._get_main_menu_text()
            elif opcao in faq_answers:
                resposta = faq_answers[opcao] + "\n\nDigita otro número para más preguntas o 0️⃣ para volver al menú principal."
            else:
                resposta = "Por favor, digita un número válido de las preguntas frecuentes o 0️⃣ para volver al menú principal."

            Conversation.save_message(user_id, platform, resposta, is_from_user=False)
            return resposta

        # Contexto de síntomas
        elif current_context == ContextManager.CONTEXT_TYPES.get('WAITING_SYMPTOM'):
            if opcao == '0':
                ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['MAIN_MENU'], {})
                resposta = ResponseGenerator._get_main_menu_text()
            else:
                resposta = f"Mencionaste: {message_text}. Estamos analizando tus síntomas para sugerirte un medicamento."
            
            Conversation.save_message(user_id, platform, resposta, is_from_user=False)
            return resposta

        # Verificación de síntomas/medicamentos
        entities = NLPProcessor.get_entities_from_products()
        message_lower = message_text.lower()

        if any(ent.lower() in message_lower for ent in entities['sintomas'] + entities['medicamentos']):
            ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['WAITING_SYMPTOM'], {})
            print('OK hasta aquí')
            # Ahora ya procesa directamente
            resposta, new_context_type, context_data = ContextManager.process_in_context(user_id, platform, message_text, {'intent': None})
            if resposta:
                ContextManager.set_context(user_id, platform, new_context_type, context_data or {})
                Conversation.save_message(user_id, platform, resposta, is_from_user=False)
                return resposta

        # Caso por defecto - mostrar menú principal
        ContextManager.set_context(user_id, platform, ContextManager.CONTEXT_TYPES['MAIN_MENU'], {})
        resposta = ResponseGenerator._get_main_menu_text()
        Conversation.save_message(user_id, platform, resposta, is_from_user=False)
        return resposta
