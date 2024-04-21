import requests
from model import contato
import termos
from model.contato import Hico


def identifica_resposta(conteudo_mensagem, telefone):
    if conteudo_mensagem in termos.saudacoes:
        registro = Hico.pesquisar_registro(telefone)

        if registro is not None:
            return (f"Olá {registro.HICONOME}!\n"
                    f"Seja bem-vindo novamente a central de atendimento da HareWare!")
        else:
            return ("Olá! Seja bem-vindo a central de atendimento da HareWare!\n"
                    "Por favor digite nome!")
    else:
        return "Não entendi!"


def responder(business_phone_number_id, GRAPH_API_TOKEN, remetente, id_mensagem_anterior, conteudo_mensagem):
    mensagem = identifica_resposta(conteudo_mensagem, remetente)

    response = requests.post(
        f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
        headers={"Authorization": f"Bearer {GRAPH_API_TOKEN}"},
        json={
            "messaging_product": "whatsapp",
            "to": remetente,
            "text": {"body": mensagem},
            "context": {
                "message_id": id_mensagem_anterior
            }
        }
    )
