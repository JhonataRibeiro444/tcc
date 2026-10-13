---
name: tcc-writing
description: Local norms and status index of the CRM TCC (Daniel e Jhonatan) — institution, formatting rules, chapter list with status, canonical metrics. Read by tcc-rascunho, tcc-revisao-impessoal, tcc-status, tcc-defesa and the tcc-orientador agent. Use when writing or formatting any part of the TCC text. Written in Portuguese.
---

# TCC — Normas e índice do projeto

Fonte única das regras locais do TCC. As outras skills `tcc-*` leem este arquivo.
Campos marcados com `TODO` ainda precisam ser preenchidos pelos autores — nunca
invente um valor para eles; pergunte.

## Identificação

- **Título:** TODO
- **Autores:** Daniel e Jhonatan
- **Instituição / curso:** TODO
- **Orientador(a):** TODO
- **Norma:** ABNT (NBR 14724, 6023, 10520) — TODO: a instituição tem template próprio? Onde está?
- **Entrega / defesa:** TODO (datas)

## Onde fica o texto

- Capítulos: `docs/tcc/cap{N}-{slug}.md`
- Referência do projeto (problema, objetivos, RFs, RNFs): `docs/tcc/tcc-referencia.md`
- Referências bibliográficas: `docs/tcc/referencias.md`
- Fragmentos (matéria-prima): `docs/tcc/_fragmentos/cap{N}-fragmentos.md`
- Relatórios de revisão: `docs/tcc/_revisoes/cap{N}-revisao-{data}.md`

## Status dos capítulos

Estrutura proposta — ajustar ao modelo da instituição.

| Cap. | Título | Conteúdo | Status |
|---|---|---|---|
| 1 | Introdução | Contexto, problema, objetivos, justificativa | 🔴 Pendente |
| 2 | Referencial Teórico | CRM, gestão de relacionamento, tecnologias web | 🔴 Pendente |
| 3 | Metodologia | Tipo de pesquisa, levantamento de requisitos, processo de desenvolvimento | 🔴 Pendente |
| 4 | Desenvolvimento | Requisitos, arquitetura MVC, modelo de dados, telas | 🔴 Pendente |
| 5 | Resultados e Discussão | O que foi entregue, testes, avaliação | 🔴 Pendente |
| 6 | Conclusão | Contribuições, limitações, trabalhos futuros | 🔴 Pendente |

Status: ✅ Concluído · 🟠 Rascunho · 🔴 Pendente

## Regras de redação

- Voz impessoal absoluta (voz passiva ou 3ª pessoa do singular). Nunca "eu", "nós", "fizemos".
- Português brasileiro formal.
- Citação direta curta: entre aspas no texto + `(AUTOR, ano, p. X)`. Longa (>3 linhas): recuo 4 cm, fonte 10, sem aspas.
- Citação indireta: paráfrase + `(AUTOR, ano)`.
- Figuras e tabelas: chamadas no texto **antes** de aparecerem; título acima ("Figura X – Título"), fonte abaixo ("Fonte: Os autores (ano).").
- Primeira ocorrência de termo técnico ou sigla: explicar/expandir (ex.: "Customer Relationship Management (CRM)").
- Sem clichês: "é importante", "é crucial", "atualmente", "nos dias de hoje".

## Métricas canônicas

Números citados no texto e na defesa saem **só daqui**. Atualizar quando mudarem.

| Métrica | Valor | Como medir |
|---|---|---|
| Testes automatizados | TODO | `pytest --collect-only -q` |
| Módulos entregues | Autenticação, Clientes, Contatos, Painel, Importação/Exportação de planilhas | `app/controllers/` |
| Commits | TODO | `git rev-list --count HEAD` |
