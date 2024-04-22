

def caracteres_numericos(conteudo_mensagem):
    return any(char.isdigit() for char in conteudo_mensagem)


def caracteres_estranhos(conteudo_mensagem):
    caracteres_invalidos = [caractere for caractere in conteudo_mensagem if not (caractere.isalnum())]
    return caracteres_invalidos