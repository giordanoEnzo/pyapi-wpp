from nameparser import HumanName


def validar_nome(conteudo_mensagem):
    parsed_name = HumanName(conteudo_mensagem)
    return parsed_name.is_valid
