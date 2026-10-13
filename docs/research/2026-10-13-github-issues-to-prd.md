# Pesquisa — GitHub Issues, Milestones e Labels com `to-prd` / `to-issues`

Data: 2026-10-13 · Nível: comparison · Fontes: skills de `jgbriel-io/jgbriel-skills`
(commit `66d83ff`, 2026-10-10), docs oficiais do GitHub e do `gh`, ambiente local.

## Resumo e recomendação

Dá para usar o fluxo `to-prd` → `to-issues` no repo `JhonataRibeiro444/tcc` sem
escrever scripts de API, **desde que três coisas sejam feitas antes**:

1. **Instalar e autenticar o `gh` ≥ 2.94** — hoje ele não está instalado nesta máquina,
   e as duas skills dependem dele. A partir da 2.94, `gh issue create` aceita `--parent`
   (sub-issue), `--blocked-by` (dependência) e `--milestone`, o que substitui a parte
   da API que as skills deixavam para um "issue-tracker doc" inexistente.
2. **Copiar `to-prd` e `to-issues` para `.claude/skills/`** (ainda não estão no projeto) e
   ajustá-las ao nosso caso.
3. **Declarar a taxonomia de labels e milestones num `CLAUDE.md` do projeto** — as skills
   se recusam a inventar labels e procuram o vocabulário lá.

Recomendação de taxonomia (decisão de vocês, ver Opções):

- **Milestones = entregas do TCC com data** (progresso + prazo).
- **Labels em três eixos**: `state:` (fluxo), `type:` (natureza) e `area:` (módulo do CRM
  ou parte do texto). Descartar o eixo `model:` do autor.

## Contexto e requisitos implícitos

- Dupla (Jhonatan e Daniel), prazos acadêmicos, conteúdo em português.
- Repo pessoal no GitHub (não é organização) e espelho no GitLab (`origin`).
- O trabalho inclui **código** (módulos do CRM) e **texto** (capítulos do TCC) — os dois
  precisam caber no mesmo quadro.
- Windows; `gh` precisa funcionar no PowerShell e no Git Bash.

## O que é verdade hoje

| Fato | Evidência | Rótulo |
|---|---|---|
| `gh` não está instalado | `which gh` → not found; `gh: command not found` | tested-locally |
| `gh` disponível via winget, v2.102.0 | `winget show --id GitHub.cli` | tested-locally |
| `to-prd`/`to-issues` não estão em `.claude/skills/` | listagem da pasta nesta sessão | tested-locally |
| As skills exigem tracker e labels configurados no `CLAUDE.md` do projeto | `skills/delivery/to-prd/SKILL.md:9`, `to-issues/SKILL.md:11` | read-in-code |
| Provisionam labels com `gh label create` e **nunca inventam valores** fora da taxonomia | `to-prd/SKILL.md:11`, `to-issues/SKILL.md:13` | read-in-code |
| Taxonomia do autor: `state:`, `type:`, `model:`, `domain:` | `claude/CLAUDE.md:302` | read-in-code |
| Issue publicado pelas skills nasce `state:ready-for-agent`; aberto à mão nasce `needs-triage` | `claude/CLAUDE.md:333`, `to-prd/SKILL.md:21` | read-in-code |
| Repo pode optar por `domain:` como milestones (`Domain axis: milestones`), criados via `gh api .../milestones` | `claude/CLAUDE.md:352`, `:363` | read-in-code |
| `to-issues` cita um "issue-tracker doc" para sub-issues e bloqueios — **esse doc não existe no repo** | `to-issues/SKILL.md:55`; busca por "issue-tracker" sem resultado fora das skills | read-in-code |

## Achados externos

| Afirmação | Fonte | Rótulo |
|---|---|---|
| `gh label create <nome> -c <hex> -d <desc>`; `--force` atualiza se já existir | [manual gh label create](https://cli.github.com/manual/gh_label_create) | verified-fetch |
| `gh` não tem subcomando de milestone; associa-se com `gh issue create -m <título>` | [manual gh issue create](https://cli.github.com/manual/gh_issue_create) | verified-fetch |
| Milestone se cria via `POST /repos/{owner}/{repo}/milestones` (`title` obrigatório; `description`, `due_on` ISO 8601 opcionais); erro documentado só `422` genérico | [REST milestones](https://docs.github.com/en/rest/issues/milestones) | verified-fetch |
| `gh issue create` tem `--parent`, `--blocked-by`, `--blocking`, `--type`, `--milestone`, `--label`, `--assignee`, `--project`, `--body-file` | [manual gh issue create](https://cli.github.com/manual/gh_issue_create) | verified-fetch |
| Esses flags de hierarquia e dependência chegaram no **gh v2.94.0** | [changelog GitHub 2026-06-10](https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/) | verified-fetch |
| `--type` (issue types) só funciona em **organizações** que definiram tipos → não serve para repo pessoal | mesmo changelog | verified-fetch |
| Pela API, sub-issue e "blocked by" pedem o `id` numérico, não o `number` | [REST sub-issues](https://docs.github.com/en/rest/issues/sub-issues), [REST issue dependencies](https://docs.github.com/en/rest/issues/issue-dependencies) | verified-fetch (inferido do schema) |

## Opções

**Milestones**

| Opção | Prós | Contras |
|---|---|---|
| A. Milestones = **entregas do TCC** (ex.: "Entrega parcial", "Qualificação", "Versão final", "Defesa"), com `due_on` | Barra de progresso + prazo real; espelha o calendário acadêmico | Diverge da convenção do autor (lá milestone = domínio) — precisa ajustar o texto das skills |
| B. Milestones = **domínio** (convenção do autor: "Clientes", "Oportunidades", "Escrita TCC"…) | Skills funcionam como escritas | Perde a noção de prazo, que é o que mais importa num TCC |

**Labels**

| Eixo | Proposta | Observação |
|---|---|---|
| `state:` | `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` | Mantém compatível com as skills e com `triage` |
| `type:` | `bug`, `enhancement`, `docs` + **`tcc`** (texto acadêmico) | `tcc` separa trabalho de escrita de trabalho de código |
| `area:` (no lugar de `domain:`) | `auth`, `clientes`, `contatos`, `painel`, `planilhas`, + módulos futuros | Declarado no `CLAUDE.md` do projeto |
| `model:` | **descartar** | Serve ao autor para escolher modelo por issue; aqui só adiciona burocracia |

**Recomendação:** A + labels acima. Milestone dá o "quando", label dá o "o quê" e o "em que estado".

## Contra-revisão (feita na própria sessão, sem subagente)

1. **"ready-for-agent" pressupõe agentes autônomos pegando issues.** Para a dupla, o
   significado vira "especificado, pode começar". Aceitável, mas vale renomear o
   sentido no `CLAUDE.md` para não confundir o Daniel. → risco declarado.
2. **Dois remotos.** Referências `#12` e "closes #12" nos commits só fecham issues
   quando o commit chega ao GitHub; no GitLab ficam texto morto. Como a `main` agora
   acompanha `github/main`, o efeito é pequeno, mas o GitLab vira só espelho. → risco declarado.
3. **Divergência da convenção do autor (opção A).** As skills dizem, em texto, para criar
   milestone de domínio. Precisa editar as duas skills para não brigarem com o `CLAUDE.md`. → custo da recomendação.

## Riscos e pegadinhas

- `gh` antigo (< 2.94) ignora `--parent`/`--blocked-by` → conferir com
  `gh issue create --help`.
- `gh auth login` é interativo — tem de ser feito por vocês (`! gh auth login`).
- O Daniel precisa ser **colaborador** do repo para ser assignee.
- `--project` (GitHub Projects/quadro) exige escopo extra: `gh auth refresh -s project`.
- Criar muitos issues/dependências em sequência pode bater em rate limit secundário.

## Refutado

- "É preciso escrever chamadas de API com id numérico para sub-issues e bloqueios" —
  refutado para o nosso caso: `gh` ≥ 2.94 faz isso por flag com o **número** do issue.
- "Dá para usar issue types (`--type`)" — refutado: só em organizações.

## Perguntas abertas

- Datas reais das entregas do TCC (para os `due_on` dos milestones).
- Vão querer um **GitHub Project** (quadro kanban) além de labels/milestones?
- Comportamento exato de `gh label create` sem `--force` quando o label já existe
  (a doc não diz; testar após instalar).
- Limites de quantidade/profundidade de sub-issues — não encontrados na doc oficial.

## Próximo passo

`plan`: (1) instalar `gh` via winget + `gh auth login`; (2) copiar `to-prd`, `to-issues`
(e `triage`, opcional) adaptadas; (3) criar `CLAUDE.md` do projeto com tracker, labels
e milestones; (4) provisionar labels/milestones; (5) primeiro `/to-prd` real (ex.: módulo
de Oportunidades).
