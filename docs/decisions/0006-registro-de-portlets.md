---
type: decision
status: accepted
number: 6
date: 2026-08-29
superseded_by:
---
# 0006 Registro declarativo de portlets no painel

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

O painel inicial, inspirado no NetSuite, é composto de blocos independentes, e está previsto que cada usuário possa reordená-los e escondê-los.

## Decisão

Declarar os portlets num registro (`app/portlets.py`): cada `Portlet` tem chave, título, coluna, template, função de dados e ordem. O painel itera o registro; adicionar um portlet é adicionar uma entrada.

## Consequências

- Portlet novo não exige mexer no template do painel.
- A personalização por usuário pode vir como uma tabela de preferências que sobrepõe coluna e ordem.
- Todas as funções de dados rodam a cada carregamento do painel.

## Alternativas rejeitadas

- **Blocos fixos no template** — mais simples hoje, mas cada portlet novo ou a personalização exigiriam reescrever o painel.
