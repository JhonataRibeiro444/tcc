---
type: spec
status: current
labels: []
depends_on: [1, 2, 3, 4, 5, 6]
---
# 007 Cobertura de testes

## Problema

A suíte atual (60 testes, pytest) passa e cobre 83% de linhas e branches de `app/`, mas:

- não há medição de cobertura nem meta, então a cobertura pode cair sem ninguém notar;
- caminhos de erro importantes não são exercitados — CLI (40%), importação de planilhas (73%),
  autenticação e contatos (76%);
- nada roda num navegador de verdade: máscaras em JavaScript, trocas HTMX e o fluxo completo de
  importação nunca foram testados como o usuário os usa;
- os testes só rodam na máquina de quem lembrar de rodá-los.

Para o TCC, a qualidade do software precisa ser demonstrável com números, não afirmada.

## Solução

- Cobertura medida com pytest-cov em linhas e branches, com a suíte **falhando abaixo de 90%**.
- Testes novos de unidade e integração para os caminhos de erro sem cobertura.
- Testes end-to-end com Playwright (pytest-playwright) contra a aplicação rodando de verdade,
  cobrindo os fluxos principais no navegador.
- GitHub Actions rodando tudo a cada push e pull request, com o resultado visível no README.

## Histórias de usuário

1. Como desenvolvedor, quero rodar um único comando que execute os testes e mostre a cobertura.
2. Como desenvolvedor, quero que a suíte falhe se a cobertura cair abaixo de 90%.
3. Como desenvolvedor, quero ver quais linhas e branches não estão cobertos.
4. Como desenvolvedor, quero separar dependências de desenvolvimento das de produção.
5. Como desenvolvedor, quero testes dos comandos `flask init-db` e `flask criar-usuario`.
6. Como responsável pela segurança, quero testes que provem que o login não redireciona para
   domínios externos e que contas desativadas não entram.
7. Como desenvolvedor, quero testes da edição de contatos e das respostas HTMX e não HTMX.
8. Como gestor, quero que os erros da importação (arquivo inválido, planilha vazia, importação
   expirada, documento cadastrado entre a prévia e a confirmação) estejam cobertos por testes.
9. Como desenvolvedor, quero testes unitários da leitura de `.xlsx`, da planilha modelo, do
   relatório de erros e da proteção contra *CSV injection*.
10. Como desenvolvedor, quero rodar os testes de navegador separadamente dos rápidos.
11. Como usuário, quero que o login e a navegação funcionem num navegador real.
12. Como vendedor, quero que as máscaras de CPF, CNPJ, telefone e CEP funcionem no navegador e
    que o cadastro com máscara grave o documento certo.
13. Como vendedor, quero que a busca de clientes e a busca global atualizem a tela sem recarregar.
14. Como vendedor, quero que adicionar, editar e remover contatos funcione no painel do cliente.
15. Como gestor, quero que o fluxo completo de importação funcione no navegador: modelo, envio,
    prévia, relatório de erros e confirmação.
16. Como dupla, queremos que os testes rodem sozinhos no GitHub a cada push e pull request.
17. Como autor do TCC, quero um selo de status e o número da cobertura para citar no texto.

## Decisões de implementação

- **pytest-cov** com `--cov=app --cov-branch` e `fail_under = 90`, configurado no repositório
  para valer em todo comando `pytest`.
- Ferramentas de teste num `requirements-dev.txt` que inclui o `requirements.txt`.
- O modelo de exemplo, sem uso, é removido em vez de testado.
- **Testes de unidade** para funções puras (`app/utils/`); **integração** pelo cliente de teste do
  Flask para rotas, formulários e banco — o padrão que a suíte já usa.
- **E2E com pytest-playwright** (Chromium), num marcador `e2e` excluído da execução padrão. Uma
  fixture sobe a aplicação num servidor real em porta livre, com banco SQLite temporário e um
  usuário criado, e o encerra ao fim da sessão.
- Os E2E não entram no cálculo da meta de cobertura; ela é medida na suíte rápida.
- **GitHub Actions**: um job com a suíte rápida e a cobertura, outro com os E2E (instala o
  Chromium do Playwright); relatório de cobertura publicado como artefato e selo no README.

## Decisões de teste

- Um bom teste verifica comportamento visível — status, HTML, registros no banco, arquivo
  baixado — e não detalhes internos; refatorar não deve quebrá-lo.
- Seams: o cliente de teste do Flask (integração), as funções de `app/utils/` (unidade), o
  `test_cli_runner` do Flask (CLI) e a página no navegador (E2E). Nenhum seam novo no código de
  produção.
- Referências na própria suíte: `tests/test_clientes.py` (integração), `tests/test_validators.py`
  (unidade), `tests/test_importacao_planilhas.py` (arquivos em memória).
- Nada de mock do banco: SQLite em memória (integração) ou em arquivo temporário (E2E).

## Fora de escopo

- Testes de carga e desempenho.
- Testes de acessibilidade automatizados (axe) — candidato a spec próprio.
- Navegadores além do Chromium.
- Testes de mutação.

## Entrega

Fatias publicadas como sub-issues do PRD no GitHub.
