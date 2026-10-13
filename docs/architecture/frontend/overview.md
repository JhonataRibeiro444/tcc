---
type: architecture
status: current
---
# Frontend

Páginas renderizadas no servidor com Jinja2 sobre Bootstrap 5. HTMX troca pedaços da página sem
recarregá-la; o JavaScript próprio cuida só de máscaras e de detalhes de interface.

## Templates

| Arquivo | Papel |
|---|---|
| `base.html` | Layout: faixa superior com busca global e usuário, faixa de módulos, mensagens |
| `_macros.html` | Macros de campos de formulário |
| `_mensagens.html` | Mensagens *flash* |
| `_busca_resultados.html` | Fragmento da busca global |
| `index.html` | Painel; itera os portlets de cada coluna |
| `portlets/_*.html` | Um template por portlet |
| `clientes/` | Lista, tabela (fragmento), formulário, detalhe, importação e pré-visualização |
| `contatos/` | Painel de contatos do cliente (fragmento), lista e tabela |
| `auth/login.html` | Tela de entrada |

Convenção: arquivos com prefixo `_` são fragmentos, devolvidos sozinhos em requisições HTMX.

## HTMX

- Busca da listagem de clientes e de contatos: a cada digitação, a tabela é substituída.
- Busca global: o fragmento de resultados aparece sob o campo da barra superior.
- Painel de contatos do cliente: abrir, cancelar, salvar e remover contato trocam só o painel.

O controller decide pelo cabeçalho `HX-Request` se devolve o fragmento ou a página inteira, então
as rotas continuam funcionando sem JavaScript.

## Portlets

O painel é montado a partir do registro em `app/portlets.py`. Cada `Portlet` declara chave,
título, coluna (`esquerda`/`direita`), template, função de dados e ordem. Portlets atuais:
configurações rápidas, lembretes, resumo de clientes e últimos cadastros. Ver
[decisão 0006](../../decisions/0006-registro-de-portlets.md).

## Estilo e scripts

| Arquivo | Papel |
|---|---|
| `static/css/tema.css` | Camada de tema inspirada no NetSuite (cores, faixas, portlets) |
| `static/css/style.css` | Estilos da aplicação |
| `static/js/mascaras.js` | Máscaras de CPF, CNPJ, telefone e CEP |
| `static/js/interface.js` | Comportamentos de interface |

## Pontos em aberto

- Acessibilidade não auditada (skill `accessibility-audit`).
