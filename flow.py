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
            novo_status = Hist(telefone, "TPS", datetime.now())
            Hist.gravar_status(novo_status)

            return (f"Olá {registro_contato.HICONOME}!\n"
                    f"Seja bem-vindo novamente a central de atendimento da HareWare!\n\n"
                    f"Em que posso ajuda-lo? Digite o número correspondente ao serviço que procura:\n\n"
                    f"1) Suporte técnico\n"
                    f"2) Atendimento comercial\n")
        else:
            novo_status = Hist(telefone, "NM3", datetime.now())
            Hist.gravar_status(novo_status)

            return ("Olá! Seja bem-vindo a central de atendimento da HareWare!\n"
                    "Por favor digite o seu nome!")
    elif registro_status.HISTSTAT == "NM3":

        if caracteres_estranhos(conteudo_mensagem) or caracteres_numericos(conteudo_mensagem):
            return "Por favor, insira um nome válido!"

        novo_contato = Hico(conteudo_mensagem, telefone, None, False)
        Hico.gravar_registro(novo_contato)
        registro_contato = Hico.pesquisar_registro(telefone)

        registro_status.deletar_status()

        novo_status = Hist(telefone, "TPS", datetime.now())
        Hist.gravar_status(novo_status)

        return (f"Prazer em te conhecer {registro_contato.HICONOME}!\n\n"
                f"Como posso ajudar? Digite o número correspondente ao serviço que precisa:\n\n"
                f"1) Suporte técnico\n"
                f"2) Atendimento cormercial\n")
    elif registro_status.HISTSTAT == "TPS":

        if conteudo_mensagem == "1":
            registro_status.deletar_status()

            novo_status = Hist(telefone, "SIS", datetime.now())
            Hist.gravar_status(novo_status)

            return ("Ótimo! você optou pelo suporte técnico!\n\n"
                    "Qual das soluções listadas abaixo você gostaria de receber assistência?\n\n"
                    "1) HareWeb - Desenvolvimento de sites\n"
                    "2) HareInteract - Chatbot multicanal\n"
                    "3) HareCloud - Serviços em nuvem\n")
        elif conteudo_mensagem == "2":
            registro_status.deletar_status()

            novo_status = Hist(telefone, "CIS", datetime.now())
            return ("Excelente! você optou pelo Atendimento comercial!\n\n"
                    "Qual das soluções listadas abaixo você gostaria de explorar detalhadamente?\n\n"
                    "1) HareWeb - Desenvolvimento de sites\n"
                    "2) HareInteract - Chatbot multicanal\n"
                    "3) HareCloud - Serviços em nuvem\n")
        else:
            return "Insira uma opção válida!"
    elif registro_status.HISTSTAT == "SIS":

        if conteudo_mensagem == "1":
            registro_status.deletar_status()

            return "HareWeb - Desenvolvimento de sites"
        elif conteudo_mensagem == "2":
            registro_status.deletar_status()

            return "HareInteract - Chatbot multicanal"
        elif conteudo_mensagem == "3":
            registro_status.deletar_status()

            return "HareCloud - Serviços em nuvem\n"
        else:
            return "Insira uma opção válida!"
    elif registro_status.HISTSTAT == "CIS":

        if conteudo_mensagem == "1":
            registro_status.deletar_status()

            return "HareWeb - Desenvolvimento de sites"
        elif conteudo_mensagem == "2":
            registro_status.deletar_status()

            return "HareInteract - Chatbot multicanal"
        elif conteudo_mensagem == "3":
            registro_status.deletar_status()

            return "HareCloud - Serviços em nuvem\n"
        else:
            return "Insira uma opção válida!"
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
