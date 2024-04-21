import json
from flask import Flask, request, jsonify
import requests
from utils.db import db
import flow

# Obtém variáveis de ambiente
WEBHOOK_VERIFY_TOKEN = "zuck_seu_merda"
GRAPH_API_TOKEN = "EAALU15sZAfHoBO64eEZC8rvlRtyD89vuxO9yKQ4nZAFj9dz1ZC8ZCot3aX9NTSHAwOZAQN0yJdh6OZC1cMSZBTryxYKx1gzNS7sA508ZCuLpICrJQNqHqGHwygpIH9Vbz2MTmZCS40mKGhwex1biOes71WOwSuCNJ3b7QJWkT1bHOWQTVjVIG4a0uCzUZAqn2Qm5a9mqyBW2fFCdjuQOCQ8xZAbhQyWzj4u2"
PORT = "5000"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:HareWare%402024@localhost/HareInteract?client_encoding=utf8'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/webhook', methods=['POST'])
def webhook():
    # Obtém os dados da mensagem recebida
    mensagem = request.json.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]

    # Verifica se a mensagem é do tipo texto
    if mensagem.get('type') == "text":
        # Extrai o ID do número de telefone comercial
        business_phone_number_id = request.json.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('metadata', {}).get('phone_number_id')

        # Envia uma resposta de eco para a mensagem recebida
        flow.responder(business_phone_number_id, GRAPH_API_TOKEN, mensagem.get('from'), mensagem.get('id'), mensagem.get('text', {}).get('body'))

        # Marca a mensagem como lida
        response = requests.post(
            f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
            headers={"Authorization": f"Bearer {GRAPH_API_TOKEN}"},
            json={
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": mensagem['id']
            }
        )

    return jsonify({}), 200

# Rota para lidar com requisições GET do webhook (verificação)
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # Verifica se o modo e o token correspondem aos esperados
    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        return challenge, 200
    else:
        return "", 403

# Rota padrão
@app.route('/')
def index():
    # Retorna uma mensagem padrão
    return "<pre>HareWare ;).</pre>"

# Executa o aplicativo Flask
if __name__ == "__main__":
    app.run(port=int(PORT))
