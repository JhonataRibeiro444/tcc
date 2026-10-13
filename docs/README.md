---
type: index
status: current
---
# Documentação do CRM

Fonte única da documentação técnica do projeto. O `README.md` da raiz cobre o que é o sistema e
como rodá-lo; aqui fica o porquê e o como por dentro. O texto acadêmico do TCC tem regras
próprias e não segue este guia (ver `.claude/skills/tcc-writing/`).

## Leia primeiro

1. [Visão do produto](product/vision.md)
2. [Glossário do domínio](product/CONTEXT.md)
3. [Arquitetura — visão geral](architecture/overview.md)
4. [Setup local](engineering/local-setup.md)

## Pastas

| Pasta | Responde |
|---|---|
| [product/](product/) | O que é o sistema, para quem e o que está no escopo |
| [architecture/](architecture/overview.md) | Como o sistema funciona hoje |
| [engineering/](engineering/) | Como construímos, testamos e rodamos |
| [decisions/](decisions/README.md) | Por que o sistema é assim |
| [specs/](specs/) | O que foi e o que será construído — cada spec vira um PRD no GitHub |
| [research/](research/) | Investigações com fontes |

## Specs

| Nº | Spec | PRD no GitHub |
|---|---|---|
| 001 | [Fundação do projeto](specs/001-fundacao-do-projeto.md) | #1 |
| 002 | [Autenticação](specs/002-autenticacao.md) | #4 |
| 003 | [Cadastro de clientes](specs/003-cadastro-de-clientes.md) | #7 |
| 004 | [Contatos](specs/004-contatos.md) | #12 |
| 005 | [Painel e interface](specs/005-painel-e-interface.md) | #15 |
| 006 | [Importação e exportação de planilhas](specs/006-importacao-e-exportacao-de-planilhas.md) | #19 |
| 007 | [Cobertura de testes](specs/007-cobertura-de-testes.md) | #22 |

O arquivo do spec é a verdade; a issue no GitHub é uma cópia. Ao mudar um, atualize o outro.

## Convenções

- Arquivos e pastas em kebab-case; decisões `NNNN-slug.md`, specs `NNN-slug.md`, pesquisas
  `AAAA-MM-DD-slug.md`.
- Todo doc tem frontmatter com `type` e `status`.
- Links entre docs são relativos (`../decisions/0001-...md`).
- Uma decisão nova só entra junto com a atualização de todo doc que ela contradiz.
