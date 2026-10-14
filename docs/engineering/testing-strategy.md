---
type: engineering
status: current
---
# Estratégia de testes

## Rodar

```powershell
pip install -r requirements-dev.txt
python -m pytest
```

Todo `pytest` mede a cobertura de linhas e branches de `app/` (`.coveragerc`) e lista as linhas
faltantes dos arquivos não totalmente cobertos. A suíte **falha abaixo do piso** definido em
`fail_under = 90`. Em 2026-10-14 a cobertura medida era 98%. O piso só sobe, nunca desce.

## Hoje

Suíte pytest em `tests/`. Cada teste recebe uma aplicação na
configuração `testing` (SQLite em memória, CSRF desligado) com um usuário já criado.

| Fixture (`tests/conftest.py`) | Entrega |
|---|---|
| `app` | Aplicação com banco criado e usuário de teste |
| `client` | Cliente HTTP sem login |
| `client_logado` | Cliente HTTP já autenticado |

| Arquivo | Cobre |
|---|---|
| `test_validators.py` | CPF, CNPJ, formatação (unitário) |
| `test_planilhas_unidade.py` | Leitura, validação, modelo, relatório e tokens de planilhas (unitário) |
| `test_cli.py` | `flask init-db` e `flask criar-usuario` |
| `test_auth.py` | Login, logout, proteção de rotas, `next` seguro, conta desativada, hash de senha |
| `test_clientes.py` | Cadastro, edição, validação, duplicidade, inativação e reativação, 404, busca HTMX |
| `test_contatos.py` | Contatos, edição, contato principal, respostas com e sem HTMX, 404, cascata |
| `test_painel.py` | Portlets, busca global, filtros da listagem, listagem de contatos |
| `test_importacao_planilhas.py` | Importação (incluindo arquivos ruins e tokens expirados) e exportação |

A maioria é teste de integração pelo cliente HTTP do Flask: exercita rota, formulário, model e
banco juntos, verificando o comportamento visível (status, HTML, registros gravados).

## Princípios

- Testar comportamento pela interface pública (rota ou função), não detalhes de implementação.
- Um teste novo para cada bug corrigido, que falha antes da correção.
- Dados de teste criados no próprio teste ou em fixtures; nunca dados reais.

## Lacunas conhecidas

- Sem testes no navegador (o JavaScript de máscaras e as trocas HTMX não são exercitados de verdade).
- Sem testes de acessibilidade.

A ampliação da suíte (cobertura, testes unitários e end-to-end com Playwright) está no
[spec 007](../specs/007-cobertura-de-testes.md).
