---
type: decision
status: accepted
number: 4
date: 2026-08-29
superseded_by:
---
# 0004 Inativar clientes em vez de excluir

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

Apagar um cliente perde o histórico cadastral e, no futuro, quebraria oportunidades e interações ligadas a ele.

## Decisão

Clientes têm o campo `ativo`; a interface só oferece inativar e reativar (`POST /clientes/<id>/situacao`). Contatos, subordinados ao cliente, podem ser excluídos e são removidos em cascata se um cliente for apagado direto no banco.

## Consequências

- Histórico preservado e ação reversível.
- Listagens e indicadores precisam filtrar por situação.
- Exclusão definitiva (por exemplo, a pedido do titular pela LGPD) ainda não tem fluxo.

## Alternativas rejeitadas

- **Exclusão física** — simples, mas irreversível e destrutiva para o histórico.
