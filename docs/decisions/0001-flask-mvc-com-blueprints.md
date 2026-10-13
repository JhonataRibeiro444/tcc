---
type: decision
status: accepted
number: 1
date: 2026-08-29
superseded_by:
---
# 0001 Flask em MVC com Blueprints

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

O projeto precisava de um framework web em Python que a dupla dominasse rápido e cuja estrutura sustentasse a discussão de arquitetura MVC no texto do TCC.

## Decisão

Usar Flask com *application factory* (`create_app`) e um Blueprint por módulo (`auth`, `main`, `clientes`, `contatos`), separando `models`, `controllers`, `forms` e `views/templates`.

## Consequências

- A estrutura MVC fica explícita nas pastas, o que facilita descrevê-la no TCC.
- Cada extensão (SQLAlchemy, Login, WTF) foi escolhida e configurada à mão: mais decisões, mais controle.
- Configurações por ambiente e testes com banco em memória saem naturalmente da factory.

## Alternativas rejeitadas

- **Django** — traz admin, ORM e auth prontos, mas impõe sua própria estrutura (MTV) e esconde parte do que o TCC quer mostrar.
- **FastAPI** — focado em APIs JSON; a interface server-side seria trabalho extra.
