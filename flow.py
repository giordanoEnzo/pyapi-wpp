import requests
from model import contato
import termos
from model.contato import Hico
from model.conversaStatus import Hist
import time


def identifica_resposta(conteudo_mensagem, telefone):
    registro_status = Hist.pesquisar_status(telefone)

    if conteudo_mensagem in termos.saudacoes:
        registro_contato = Hico.pesquisar_registro(telefone)

        if registro_contato is not None:
            return (f"Olá {registro_contato.HICONOME}!\n"
                    f"Seja bem-vindo novamente a central de atendimento da HareWare!")
        else:
            Hist.gravar_status(telefone, "NM3", time.strftime("%H:%M"))
            return ("Olá! Seja bem-vindo a central de atendimento da HareWare!\n"
                    "Por favor digite o seu nome...")
    elif registro_status == "NM3":
        Hico.gravar_registro(conteudo_mensagem)
        registro = Hico.pesquisar_registro(telefone)
        return f"Prazer em te conhecer {registro.HICONOME}!\n"
    else:
        return ("Não entendi!")


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
