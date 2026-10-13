# CRM — TCC Daniel e Jhonatan

Sistema de CRM em Flask (ver `README.md`) e o texto do TCC (`docs/tcc/`, normas em
`.claude/skills/tcc-writing/`). Interface e textos do TCC em português.

## Issue tracker

- **Repo:** GitHub `JhonataRibeiro444/tcc` (remoto `github`, que a `main` acompanha).
  O remoto `origin` no GitLab é só espelho do código — issues vivem apenas no GitHub.
- **CLI:** `gh` ≥ 2.94 (usa `--parent`, `--blocked-by`, `--milestone`, `--project`).
- **Quadro:** GitHub Project `TCC CRM` (#1). Toda issue nova entra nele (`--project "TCC CRM"`).
- **Idioma:** títulos e corpos das issues em português.
- **Fluxo:** `/to-prd` publica o PRD como issue-pai → `/to-issues` quebra em fatias
  verticais (sub-issues, com bloqueios) → `/implement` → commit com `closes #N`.
  Issue aberta à mão passa por `/triage`.

### Labels

Três eixos, sempre com prefixo. Não criar labels fora desta lista — se faltar um, perguntar.

| Eixo | Valores | Cardinalidade |
|---|---|---|
| `state:` | `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` | exatamente 1 em toda issue aberta |
| `type:` | `bug`, `enhancement`, `docs`, `tcc` | 0 ou 1 |
| `area:` | `auth`, `clientes`, `contatos`, `painel`, `planilhas` | 0..n |

Significado de `state:` aqui:

- `needs-triage` — aberta à mão, ainda não avaliada.
- `needs-info` — esperando alguém de fora: orientador, banca, um usuário consultado.
- `ready-for-agent` — especificada com critérios de aceite; pode começar (por um de nós ou pelo Claude).
  Issues criadas por `/to-prd` e `/to-issues` nascem aqui.
- `ready-for-human` — só uma pessoa pode fazer: decisão da dupla, reunião, conta, entrega formal.
- `wontfix` — não será feita.

`type:tcc` é trabalho de texto acadêmico (capítulos, revisões, referências); `type:docs` é
documentação técnica do repositório. Um módulo novo do CRM ganha um `area:` novo — adicionar
aqui primeiro, depois `gh label create`.

### Milestones

Milestones são **as entregas do TCC**, não domínios. Toda issue aberta pertence a
exatamente um milestone desta lista:

| Milestone | Prazo |
|---|---|
| Entrega parcial | TODO |
| Qualificação | TODO |
| Versão final | TODO |
| Defesa | TODO |

Ao definir uma data: `gh api -X PATCH repos/JhonataRibeiro444/tcc/milestones/<n> -f due_on=AAAA-MM-DDT23:59:59Z`
e atualizar a tabela.
