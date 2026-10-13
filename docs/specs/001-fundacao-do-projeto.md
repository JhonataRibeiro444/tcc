---
type: spec
status: current
labels: []
depends_on: []
---
# 001 Fundação do projeto

> Spec retroativo — documenta o que foi entregue no commit `4be6685` (2026-08-29).

## Problema

A dupla precisava de uma base de código que qualquer um dos dois conseguisse rodar na própria
máquina em poucos minutos, com separação clara de responsabilidades para sustentar o argumento
de arquitetura MVC no texto do TCC.

## Solução

Aplicação Flask organizada em MVC com *application factory*, configuração por ambiente,
scripts de instalação para Windows e Linux e comandos de linha de comando para preparar o banco
e criar o primeiro usuário.

## Histórias de usuário

1. Como desenvolvedor, quero rodar um único script na primeira vez, para ter ambiente virtual,
   dependências, `.env` e banco prontos.
2. Como desenvolvedor, quero criar as tabelas com um comando, para não depender de SQL manual.
3. Como desenvolvedor, quero criar um usuário pela linha de comando, para acessar o sistema
   sem tela de cadastro.
4. Como desenvolvedor, quero configurações separadas para desenvolvimento, teste e produção,
   para que os testes usem banco em memória.
5. Como autor do TCC, quero camadas `models`, `controllers`, `forms` e `views` separadas, para
   descrever a arquitetura com base no código real.

## Decisões de implementação

- Flask com *application factory* (`create_app`) e Blueprints por módulo — ver
  [decisão 0001](../decisions/0001-flask-mvc-com-blueprints.md).
- SQLite via Flask-SQLAlchemy no desenvolvimento — ver [decisão 0002](../decisions/0002-sqlite-no-desenvolvimento.md).
- Configurações `development`, `testing` e `production`; o ambiente de teste usa SQLite em
  memória e desliga o CSRF.
- Comandos `flask init-db` e `flask criar-usuario` registrados no app.
- `setup.bat` e `setup.sh` automatizam a primeira instalação.

## Decisões de teste

- pytest com *fixtures* de app, cliente HTTP e cliente já autenticado (`tests/conftest.py`).
- Cada teste roda contra um banco em memória novo.

## Fora de escopo

- Migrations de banco (as tabelas são criadas com `create_all`).
- Deploy em servidor.

## Entregue em

| Fatia | Commit |
|---|---|
| Estrutura MVC e configuração por ambiente | `4be6685` |
| Scripts de setup e comandos CLI | `4be6685` |
