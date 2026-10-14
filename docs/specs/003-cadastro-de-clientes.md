---
type: spec
status: current
labels: [area:clientes]
depends_on: [1, 2]
---
# 003 Cadastro de clientes

> Spec retroativo — documenta o que foi entregue nos commits `4be6685` (2026-08-29) e
> `f0746ac` (2026-08-29).

## Problema

A empresa que usa o CRM precisa de uma base única e confiável de clientes, pessoas físicas e
jurídicas, sem documentos inválidos ou duplicados, e consegue achar um cliente rapidamente.

## Solução

Cadastro, edição e consulta de clientes PF e PJ, com validação de CPF e CNPJ, bloqueio de
duplicidade, busca dinâmica sem recarregar a página, filtros, paginação e inativação no lugar
da exclusão.

## Histórias de usuário

1. Como vendedor, quero cadastrar um cliente pessoa física com CPF, para registrar um novo comprador.
2. Como vendedor, quero cadastrar um cliente pessoa jurídica com CNPJ e nome fantasia.
3. Como vendedor, quero que um CPF ou CNPJ inválido seja recusado no próprio formulário.
4. Como vendedor, quero ser avisado quando o documento já pertence a outro cliente.
5. Como vendedor, quero editar um cliente sem que o sistema acuse duplicidade com ele mesmo.
6. Como vendedor, quero registrar e-mail, telefone, endereço e observações do cliente.
7. Como vendedor, quero digitar documento, telefone e CEP com máscara, sem me preocupar com pontuação.
8. Como vendedor, quero que o endereço seja preenchido a partir do CEP, para digitar menos.
9. Como vendedor, quero buscar clientes por nome, nome fantasia, documento ou e-mail enquanto digito.
10. Como vendedor, quero filtrar a lista por clientes ativos ou inativos.
11. Como vendedor, quero navegar pela lista em páginas.
12. Como gestor, quero inativar um cliente em vez de apagá-lo, para preservar o histórico.
13. Como gestor, quero reativar um cliente inativado.
14. Como gestor, quero ver só clientes ativos sem contato cadastrado.
15. Como gestor, quero ver só clientes sem e-mail ou telefone (cadastro incompleto).
16. Como gestor, quero filtrar só pessoas físicas ou só pessoas jurídicas.

## Decisões de implementação

- Documento validado pelo algoritmo de dígitos verificadores módulo 11 e gravado só com dígitos,
  com restrição de unicidade — ver [decisão 0005](../decisions/0005-documento-somente-digitos.md).
- Telefone e CEP também gravados só com dígitos; a formatação é feita na exibição.
- Ao sair do campo CEP, o navegador consulta o ViaCEP e preenche logradouro, bairro, cidade e UF
  ainda vazios; sem conexão, o usuário digita o endereço normalmente.
- Inativação (`ativo = False`) no lugar da exclusão — ver [decisão 0004](../decisions/0004-inativacao-em-vez-de-exclusao.md).
- A listagem devolve só a tabela quando a requisição vem do HTMX — ver
  [decisão 0003](../decisions/0003-jinja-e-htmx.md).
- Uma única função monta a consulta filtrada; listagem e exportação (spec 006) a reaproveitam.
- Filtros `filtro=sem_contato|incompleto` e `tipo=F|J` existem para os portlets do painel
  apontarem direto para um recorte.

## Decisões de teste

- `tests/test_clientes.py`: cadastro válido, CPF inválido, documento duplicado, edição mantendo o
  próprio documento, inativação preservando o registro, busca HTMX devolvendo só a tabela.
- `tests/test_validators.py`: CPF e CNPJ válidos e inválidos, sequências repetidas, formatação.
- `tests/test_painel.py` (`TestFiltrosDaListagem`): filtros sem contato, incompleto e por tipo,
  e o filtro sobrevivendo à busca via HTMX.

## Fora de escopo

- Consulta automática de CNPJ em serviços externos.
- Exclusão definitiva de clientes pela interface.

## Entregue em

| Fatia | Commit |
|---|---|
| Cadastro PF/PJ com validação de CPF/CNPJ e duplicidade | `4be6685` |
| Busca dinâmica, filtro de situação e paginação | `4be6685` |
| Inativação e reativação | `4be6685` |
| Filtros de apoio (sem contato, incompleto, tipo) | `f0746ac` |
