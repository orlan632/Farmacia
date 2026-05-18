import logging
import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
//from response_generator import ResponseGenerator
//from models import User

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'farmacia_bot_verify_token')
PORT = int(os.getenv('PORT', 5000))

# Verificar se os tokens estão configurados
if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
    logger.error("Token do WhatsApp ou Phone ID não configurados. Configure as variáveis WHATSAPP_TOKEN e WHATSAPP_PHONE_ID no arquivo .env")
    exit(1)

# Criar aplicação Flask
app = Flask(__name__)

def send_whatsapp_message(phone_number, message_text):
    """Envia uma mensagem para o WhatsApp"""
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar mensagem para o WhatsApp: {e}")
        return None

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Endpoint para verificação do webhook do WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verificado com sucesso!")
            return challenge, 200
        else:
            logger.warning("Falha na verificação do webhook")
            return "Falha na verificação", 403
    
    return "Parâmetros inválidos", 400

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint para receber mensagens do WhatsApp"""
    data = request.json
    
    # Log para depuração
    logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")
    
    # Verificar se é uma mensagem do WhatsApp
    if 'object' in data and data['object'] == 'whatsapp_business_account':
        if 'entry' in data and data['entry']:
            for entry in data['entry']:
                if 'changes' in entry and entry['changes']:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            for message in change['value']['messages']:
                                if message['type'] == 'text':
                                    # Extrair informações da mensagem
                                    phone_number = message['from']
                                    message_text = message['text']['body']
                                    message_id = message['id']
                                    
                                    # Log para depuração
                                    logger.info(f"Mensagem recebida de {phone_number}: {message_text}")
                                    
                                    # Registrar ou atualizar o usuário no banco de dados
                                    try:
                                        User.create_or_update(
                                            user_id=phone_number,
                                            platform="whatsapp",
                                            first_name=None,  # WhatsApp não fornece nome por padrão
                                            last_name=None,
                                            username=None
                                        )
                                    except Exception as e:
                                        logger.error(f"Erro ao registrar usuário: {e}")
                                        # Continuar mesmo com erro no banco de dados
                                    
                                    try:
                                        # Gerar resposta usando o ResponseGenerator
                                        response = ResponseGenerator.generate_response(phone_number, "whatsapp", message_text)
                                        
                                        # Enviar a resposta
                                        send_whatsapp_message(phone_number, response)
                                    except Exception as e:
                                        logger.error(f"Erro ao processar mensagem: {e}")
                                        send_whatsapp_message(
                                            phone_number,
                                            "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde."
                                        )
        
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error", "message": "Formato inválido"}), 400

@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz para verificar se o servidor está em execução"""
    return "WhatsApp Bot para Farmácia está em execução!", 200

def main():
    """Função principal para iniciar o servidor Flask"""
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()

