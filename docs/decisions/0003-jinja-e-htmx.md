---
type: decision
status: accepted
number: 3
date: 2026-08-29
superseded_by:
---
# 0003 Renderização no servidor com Jinja e HTMX

> Registrada retroativamente em 2026-10-13. O motivo foi reconstruído a partir do código e do
> README; confirmar com o Daniel.

## Contexto

Buscas e o painel de contatos precisavam atualizar sem recarregar a página, sem que a dupla tivesse de manter um frontend separado.

## Decisão

Renderizar tudo no servidor com Jinja2 e usar HTMX para trocar fragmentos. Rotas detectam o cabeçalho `HX-Request` e devolvem só o fragmento (templates com prefixo `_`); sem HTMX, devolvem a página inteira.

## Consequências

- Uma única base de código e uma única linguagem para a lógica.
- As rotas continuam funcionando sem JavaScript.
- Interações muito ricas (arrastar, gráficos interativos) ficam mais trabalhosas do que num SPA.

## Alternativas rejeitadas

- **SPA em React ou Vue com API JSON** — dois projetos, duas stacks e duplicação de validação para uma dupla com prazo de TCC.
