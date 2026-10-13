---
type: spec
status: current
labels: [area:planilhas, area:clientes]
depends_on: [3, 4]
---
# 006 Importação e exportação de planilhas

> Spec retroativo — documenta o que foi entregue no commit `0fc72bf` (2026-09-06).

## Problema

Quem adota um CRM já tem clientes numa planilha. Digitar um por um inviabiliza a adoção. E o
gestor precisa tirar os dados do sistema para relatórios fora dele.

## Solução

Importação de clientes (com contato principal opcional) a partir de `.xlsx` ou `.csv`, com
pré-visualização e relatório de erros antes de gravar, e exportação para `.xlsx` ou `.csv`
respeitando os filtros da listagem.

## Histórias de usuário

1. Como gestor, quero baixar uma planilha modelo, para saber quais colunas preencher.
2. Como gestor, quero enviar uma planilha `.xlsx` ou `.csv` de clientes.
3. Como gestor, quero ver, antes de gravar, quais linhas estão ok, quais já existem e quais têm erro.
4. Como gestor, quero que linhas com CPF/CNPJ inválido não sejam importadas.
5. Como gestor, quero que documentos já cadastrados, ou repetidos na própria planilha, não
   sejam importados.
6. Como gestor, quero baixar um CSV com as linhas não importadas e o motivo, para corrigir e reenviar.
7. Como gestor, quero importar junto o contato principal de cada cliente.
8. Como gestor, quero confirmar a importação só depois de conferir.
9. Como gestor, quero exportar a lista de clientes para `.xlsx` ou `.csv`.
10. Como gestor, quero que a exportação traga exatamente o recorte filtrado que estou vendo.

## Decisões de implementação

- Importação em duas etapas, validar e confirmar, com o resultado da validação guardado em
  disco sob um token — ver [decisão 0007](../decisions/0007-importacao-em-duas-etapas.md).
- As linhas são validadas com as mesmas regras do formulário de clientes.
- Na confirmação, cada cliente é gravado na própria transação e o documento é revalidado.
- A exportação reaproveita a consulta filtrada da listagem (spec 003).
- Células exportadas para CSV que começam com `=`, `+`, `-` ou `@` são neutralizadas contra
  *CSV injection*.
- Leitura de `.xlsx` com openpyxl.

## Decisões de teste

- `tests/test_importacao_planilhas.py`: CSV válido com contato, CPF inválido, documento já
  cadastrado, documento repetido na planilha, exportação CSV e XLSX, exportação respeitando o
  filtro de situação.

## Fora de escopo

- Importação de contatos avulsos ou de outras entidades.
- Atualização de clientes existentes pela planilha (linhas duplicadas são só reportadas).

## Entregue em

| Fatia | Commit |
|---|---|
| Exportação `.xlsx`/`.csv` respeitando os filtros | `0fc72bf` |
| Importação com pré-visualização, relatório de erros e confirmação | `0fc72bf` |
