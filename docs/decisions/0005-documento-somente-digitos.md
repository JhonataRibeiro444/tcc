---
type: decision
status: accepted
number: 5
date: 2026-08-29
superseded_by:
---
# 0005 CPF/CNPJ validado e gravado só com dígitos

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

O mesmo documento chega com e sem pontuação (digitado com máscara, colado, importado de planilha), o que gera duplicidade e falhas de busca.

## Decisão

Validar CPF e CNPJ pelo algoritmo de dígitos verificadores módulo 11 conforme o tipo de pessoa, gravar só os dígitos com índice único e formatar apenas na exibição. A mesma regra vale para telefone e CEP.

## Consequências

- Duplicidade detectada independentemente da forma digitada.
- Busca por documento funciona com ou sem máscara.
- Toda entrada (formulário, importação) precisa passar por `apenas_digitos`.

## Alternativas rejeitadas

- **Gravar formatado** — a mesma pessoa poderia entrar duas vezes com pontuações diferentes.
