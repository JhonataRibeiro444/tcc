---
type: decision
status: accepted
number: 8
date: 2026-10-13
superseded_by:
---
# 0008 Issues no GitHub com milestones por entrega do TCC

## Contexto

A dupla precisava organizar o trabalho e documentar o que foi feito. As skills `to-prd` e `to-issues` publicam PRDs e fatias num issue tracker. Pesquisa em [docs/research/2026-10-13-github-issues-to-prd.md](../research/2026-10-13-github-issues-to-prd.md).

## Decisão

Usar GitHub Issues em `JhonataRibeiro444/tcc` com labels em três eixos (`state:`, `type:`, `area:`), milestones iguais às entregas do TCC e o quadro "TCC CRM". Specs em `docs/specs/` são a verdade e cada um vira um PRD no GitHub; o trabalho já feito foi registrado com PRDs retroativos fechados (#1 a #21). A configuração vive no `CLAUDE.md` da raiz.

## Consequências

- Progresso por entrega visível nas barras dos milestones.
- O GitLab (`origin`) passa a ser só espelho do código; referências a issues só funcionam no GitHub.
- Diverge da convenção do autor das skills, em que milestone representa domínio.

## Alternativas rejeitadas

- **Milestones por domínio** (convenção do autor) — perderia a noção de prazo.
- **Issues no GitLab** — as skills e o `gh` são feitos para o GitHub.
