# Agente de IA para Atendimento de Farmácia

Um modelo profissional e eficiente de Agente de IA para atendimento de farmácia, com integração para teste no Telegram e integração profissional para WhatsApp.

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Licença](https://img.shields.io/badge/licença-MIT-orange)

## Visão Geral

Este projeto implementa um Agente de IA para atendimento de farmácia, capaz de responder a perguntas sobre medicamentos, verificar disponibilidade de produtos, informar horários de funcionamento e muito mais. O sistema utiliza processamento de linguagem natural para entender as intenções dos usuários e fornecer respostas relevantes.

### Funcionalidades Principais

- **Processamento de Linguagem Natural**: Entende a intenção do usuário em linguagem natural
- **Gerenciamento de Contexto**: Mantém o contexto da conversa para uma experiência mais fluida
- **Base de Conhecimento**: Informações sobre medicamentos, sintomas e serviços da farmácia
- **Integração com Telegram**: Para testes e demonstração
- **Integração com WhatsApp**: Para uso profissional
- **Banco de Dados**: Armazenamento de informações de usuários, produtos e histórico de conversas

## Estrutura do Projeto

```
farmacia_bot/
├── app.py                  # Aplicação Flask principal
├── config.py               # Configurações do projeto
├── context_manager.py      # Gerenciador de contexto para fluxos de conversação
├── data_initializer.py     # Inicializador de dados de exemplo
├── docs/                   # Documentação
│   ├── demonstracao.md     # Demonstração do funcionamento do bot
│   ├── guia_implantacao.md # Guia de implantação e configuração
│   └── guia_usuario.md     # Guia do usuário
├── models.py               # Modelos de dados
├── nlp_processor.py        # Processador de linguagem natural
├── requirements.txt        # Dependências do projeto
├── response_generator.py   # Gerador de respostas
├── telegram_bot.py         # Integração com Telegram (completa)
├── telegram_bot_no_db.py   # Integração com Telegram (sem banco de dados)
├── test_bot.py             # Script para testar o bot com banco de dados
├── test_bot_no_db.py       # Script para testar o bot sem banco de dados
├── whatsapp_bot.py         # Integração com WhatsApp (completa)
└── whatsapp_bot_no_db.py   # Integração com WhatsApp (sem banco de dados)
```

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal
- **spaCy**: Biblioteca de processamento de linguagem natural
- **NLTK**: Biblioteca para tokenização e análise de texto
- **Python-Telegram-Bot**: API para integração com Telegram
- **Flask**: Framework web para a API do WhatsApp
- **MongoDB**: Banco de dados para armazenamento de informações
- **WhatsApp Business API**: Para integração com WhatsApp

## Requisitos

- Python 3.8+
- MongoDB (opcional, para versões completas)
- Token do Telegram (para integração com Telegram)
- Token do WhatsApp Business API (para integração com WhatsApp)

## Instalação Rápida

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/farmacia-bot.git
cd farmacia-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Baixe o modelo de linguagem em português para o spaCy:
```bash
python -m spacy download pt_core_news_sm
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` e adicione seus tokens e configurações.

5. Execute o bot do Telegram (versão sem banco de dados):
```bash
python telegram_bot_no_db.py
```

6. Para o WhatsApp, execute o servidor Flask:
```bash
python app.py
```

## Documentação

Para informações detalhadas sobre o projeto, consulte os seguintes documentos:

- [Guia de Implantação e Configuração](docs/guia_implantacao.md): Instruções detalhadas para implantar e configurar o bot
- [Guia do Usuário](docs/guia_usuario.md): Guia para usuários finais do bot
- [Demonstração](docs/demonstracao.md): Exemplos de uso e fluxos de conversação

## Versões Disponíveis

O projeto oferece duas versões para cada integração:

### Versão Completa (com Banco de Dados)

- Armazena informações de usuários e histórico de conversas
- Mantém contexto entre sessões
- Requer MongoDB instalado e configurado
- Arquivos: `telegram_bot.py`, `whatsapp_bot.py`

### Versão Simplificada (sem Banco de Dados)

- Não requer banco de dados
- Funciona de forma independente
- Ideal para testes e demonstrações
- Arquivos: `telegram_bot_no_db.py`, `whatsapp_bot_no_db.py`

## Personalização

Para personalizar o bot para sua farmácia:

1. Edite os dados de exemplo em `data_initializer.py` para incluir seus produtos e FAQs.
2. Modifique as respostas em `response_generator.py` para refletir as informações da sua farmácia.
3. Ajuste as intenções e entidades em `nlp_processor.py` conforme necessário.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

markdown
Despliegue forzado para corregir spaCy.

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Autor

Desenvolvido por Manus AI - 2025

