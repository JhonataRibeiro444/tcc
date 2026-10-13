---
type: decision
status: accepted
number: 7
date: 2026-09-06
superseded_by:
---
# 0007 Importação de planilhas em duas etapas

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

Importar uma planilha errada grava dezenas de cadastros ruins de uma vez, e desfazer isso é caro.

## Decisão

Separar validar de gravar: o envio valida linha a linha e salva o resultado em disco (pasta temporária do sistema) sob um token; o usuário confere a pré-visualização, pode baixar as linhas com erro e só então confirma. Na confirmação, cada cliente é gravado em sua própria transação e a duplicidade é revalidada.

## Consequências

- Nada é gravado sem conferência humana.
- Uma linha problemática não derruba as outras.
- Pendentes ficam em arquivos temporários até a confirmação; não há limpeza automática dos abandonados.

## Alternativas rejeitadas

- **Gravar direto no envio** — rápido, mas sem chance de conferir.
- **Uma transação para a planilha inteira** — um erro descartaria todas as linhas válidas.
