---
type: spec
status: current
labels: [area:contatos]
depends_on: [3]
---
# 004 Contatos

> Spec retroativo — documenta o que foi entregue nos commits `4be6685` (2026-08-29) e
> `f0746ac` (2026-08-29).

## Problema

Um cliente pessoa jurídica tem várias pessoas com quem o vendedor fala (comprador, financeiro,
diretor). O CRM precisa registrar essas pessoas e indicar quem é o contato principal.

## Solução

Contatos vinculados a cada cliente, gerenciados na própria página do cliente sem recarregar a
tela, com no máximo um contato principal por cliente, e uma listagem geral de contatos com busca.

## Histórias de usuário

1. Como vendedor, quero adicionar um contato ao cliente com nome, cargo, e-mail e telefone.
2. Como vendedor, quero editar ou remover um contato sem sair da página do cliente.
3. Como vendedor, quero marcar um contato como principal, para saber com quem falar primeiro.
4. Como vendedor, quero que marcar um novo principal desmarque o anterior automaticamente.
5. Como vendedor, quero que um contato sem nome seja recusado.
6. Como vendedor, quero uma lista de todos os contatos, com busca, para achar uma pessoa sem
   saber de qual cliente ela é.

## Decisões de implementação

- Relação 1:N `Cliente` → `Contato`, com exclusão em cascata caso um cliente seja apagado.
- Regra de "no máximo um principal" aplicada no controller ao salvar.
- O painel de contatos no detalhe do cliente é um fragmento HTMX; sem HTMX, a ação redireciona
  para a página do cliente.

## Decisões de teste

- `tests/test_contatos.py`: adicionar contato, recusar contato sem nome, apenas um principal por
  cliente, remover contato, exclusão do cliente remove seus contatos.
- `tests/test_painel.py` (`TestListagemDeContatos`): listagem geral, busca pelo nome do cliente,
  busca sem resultado, exigência de login.

## Fora de escopo

- Contato vinculado a mais de um cliente.
- Histórico de interações com o contato — previsto nos próximos passos.

## Entregue em

| Fatia | Commit |
|---|---|
| Contatos no detalhe do cliente, com contato principal | `4be6685` |
| Listagem geral de contatos com busca | `f0746ac` |
