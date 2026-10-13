---
type: spec
status: current
labels: [area:painel]
depends_on: [3, 4]
---
# 005 Painel e interface

> Spec retroativo — documenta o que foi entregue nos commits `f0746ac` (2026-08-29) e
> `5faeffc` (2026-08-30).

## Problema

A primeira versão tinha telas funcionais, mas sem a cara de um sistema de gestão. O usuário
precisava de uma tela inicial que mostrasse o que pede atenção e de um jeito rápido de achar
qualquer cliente ou contato de qualquer página.

## Solução

Interface inspirada na organização de tela do Oracle NetSuite, painel inicial em portlets e
busca global na barra superior.

## Histórias de usuário

1. Como usuário, quero uma barra superior com a busca e minha identificação, e uma faixa com os
   módulos, para navegar como num sistema de gestão.
2. Como usuário, quero atalhos para as ações mais comuns no painel inicial.
3. Como gestor, quero lembretes no painel (clientes sem contato, cadastros incompletos), cada um
   levando à lista já filtrada.
4. Como gestor, quero um resumo da base (totais por situação e tipo de pessoa).
5. Como vendedor, quero ver os últimos clientes cadastrados.
6. Como usuário, quero buscar clientes e contatos ao mesmo tempo pela barra superior, com
   resultados enquanto digito.

## Decisões de implementação

- Camada de tema (`tema.css`) sobre o Bootstrap, separada do CSS da aplicação.
- Portlets declarados num registro em `app/portlets.py` (chave, título, coluna, template, função
  de dados, ordem) — ver [decisão 0006](../decisions/0006-registro-de-portlets.md).
- Quatro portlets: configurações rápidas, lembretes, resumo de clientes e últimos cadastros.
- Busca global responde um fragmento HTMX, só a partir de 2 caracteres e com até 5 resultados
  por tipo, para não consultar o banco a cada tecla.

## Decisões de teste

- `tests/test_painel.py`: o painel monta os quatro portlets; a barra de módulos só aparece para
  quem está logado; lembretes contam clientes sem contato e cadastros incompletos (e lembrete
  zerado não vira link); resumo totaliza por tipo e situação; busca global ignora termo curto,
  acha cliente por nome e por documento com máscara, acha contato mostrando o cliente e exige
  login; cliente recém-cadastrado aparece nos últimos cadastros.

## Fora de escopo

- Painel configurável por usuário (reordenar, mostrar/ocultar) — previsto nos próximos passos;
  o registro já foi pensado para receber essa preferência.

## Entregue em

| Fatia | Commit |
|---|---|
| Layout inspirado no NetSuite | `f0746ac`, `5faeffc` |
| Registro de portlets e quatro portlets | `f0746ac` |
| Busca global no topo | `f0746ac` |
