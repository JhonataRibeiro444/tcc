---
type: decision
status: accepted
number: 2
date: 2026-08-29
superseded_by:
---
# 0002 SQLite no desenvolvimento

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

Cada autor roda o sistema na própria máquina e o setup precisa ser trivial.

## Decisão

Usar SQLite via Flask-SQLAlchemy, com a URL do banco vinda de `DATABASE_URL`, e criar as tabelas com `db.create_all()` (`flask init-db`).

## Consequências

- Zero instalação de servidor de banco; testes usam SQLite em memória.
- Sem migrations: mudar o schema exige recriar o banco de desenvolvimento.
- Para uso multiusuário em produção, trocar para PostgreSQL mudando só a `DATABASE_URL` (o ORM isola o resto).

## Alternativas rejeitadas

- **PostgreSQL desde o início** — mais próximo de produção, mas exige servidor ou Docker em cada máquina.
