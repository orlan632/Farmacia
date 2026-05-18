import logging
import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

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

# Criar aplicação Flask
app = Flask(__name__)

def send_whatsapp_message(phone_number, message_text):
    """Envia uma mensagem para o WhatsApp (não implementado)"""
    logger.info(f"Mensagem para {phone_number}: {message_text}")
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
    """Endpoint para receber mensagens do WhatsApp (versão simplificada)"""
    data = request.json
    logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")
    return jsonify({"status": "success"}), 200

@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz para verificar se o servidor está em execução"""
    return "WhatsApp Bot para Farmácia está em execução!", 200

def main():
    """Função principal para iniciar o servidor Flask"""
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()
