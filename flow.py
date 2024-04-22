import requests
from model import contato, conversaStatus
import termos
from model.contato import Hico
from model.conversaStatus import Hist
from datetime import datetime
from utils.validacoes import caracteres_numericos, caracteres_estranhos


def identifica_resposta(conteudo_mensagem, telefone):
    registro_status = Hist.pesquisar_status(telefone)

    if conteudo_mensagem in termos.saudacoes:
        registro_contato = Hico.pesquisar_registro(telefone)

        if registro_contato is not None:
            return (f"Olá {registro_contato.HICONOME}!\n"
                    f"Seja bem-vindo novamente a central de atendimento da HareWare!")
        else:
            novo_status = Hist(telefone, "NM3", datetime.now())
            Hist.gravar_status(novo_status)
            return ("Olá! Seja bem-vindo a central de atendimento da HareWare!\n"
                    "Por favor digite o seu nome...")
    elif registro_status.HISTSTAT == "NM3":
        if caracteres_estranhos(conteudo_mensagem) or caracteres_numericos(conteudo_mensagem):
            return "Por favor, insira um nome válido!"
        novo_contato = Hico(conteudo_mensagem, telefone, None, False)
        Hico.gravar_registro(novo_contato)
        registro_contato = Hico.pesquisar_registro(telefone)
        registro_contato.Hist.deletar_status()
        return f"Prazer em te conhecer {registro_contato.HICONOME}!\n"
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
