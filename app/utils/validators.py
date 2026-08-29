"""Validacao e formatacao de documentos brasileiros (CPF e CNPJ).

As regras seguem o algoritmo de digitos verificadores modulo 11 usado pela
Receita Federal. Os documentos sao armazenados no banco apenas com digitos,
sem pontuacao, e formatados na hora da exibicao.
"""

import re

CPF_TAMANHO = 11
CNPJ_TAMANHO = 14


def apenas_digitos(valor):
    """Remove qualquer caractere que nao seja numero."""
    if not valor:
        return ""
    return re.sub(r"\D", "", str(valor))


def _digito_verificador(digitos, pesos):
    soma = sum(int(d) * p for d, p in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def validar_cpf(cpf):
    """Retorna True quando o CPF informado e valido."""
    numeros = apenas_digitos(cpf)

    if len(numeros) != CPF_TAMANHO:
        return False

    # Sequencias repetidas (000.000.000-00, 111.111.111-11, ...) sao invalidas.
    if numeros == numeros[0] * CPF_TAMANHO:
        return False

    primeiro = _digito_verificador(numeros[:9], range(10, 1, -1))
    segundo = _digito_verificador(numeros[:10], range(11, 1, -1))

    return numeros[9:] == f"{primeiro}{segundo}"


def validar_cnpj(cnpj):
    """Retorna True quando o CNPJ informado e valido."""
    numeros = apenas_digitos(cnpj)

    if len(numeros) != CNPJ_TAMANHO:
        return False

    if numeros == numeros[0] * CNPJ_TAMANHO:
        return False

    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_segundo = [6] + pesos_primeiro

    primeiro = _digito_verificador(numeros[:12], pesos_primeiro)
    segundo = _digito_verificador(numeros[:13], pesos_segundo)

    return numeros[12:] == f"{primeiro}{segundo}"


def validar_documento(documento, tipo_pessoa):
    """Valida o documento de acordo com o tipo de pessoa (F ou J)."""
    if tipo_pessoa == "F":
        return validar_cpf(documento)
    if tipo_pessoa == "J":
        return validar_cnpj(documento)
    return False


def formatar_documento(documento):
    """Devolve o documento com a mascara usual de CPF ou CNPJ."""
    numeros = apenas_digitos(documento)

    if len(numeros) == CPF_TAMANHO:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    if len(numeros) == CNPJ_TAMANHO:
        return (
            f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}"
            f"/{numeros[8:12]}-{numeros[12:]}"
        )
    return documento or ""


def formatar_telefone(telefone):
    """Formata telefones brasileiros de 10 ou 11 digitos."""
    numeros = apenas_digitos(telefone)

    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    if len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return telefone or ""
