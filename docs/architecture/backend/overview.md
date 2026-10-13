---
type: architecture
status: current
---
# Backend

A aplicação nasce em `create_app` (`app/__init__.py`), que carrega a configuração do ambiente,
inicializa SQLAlchemy, Flask-Login e CSRF, registra os quatro Blueprints e os comandos de CLI.

## Blueprints e rotas

Todas as rotas, exceto `/auth/login`, exigem login.

### `auth` — `/auth` (`app/controllers/auth_controller.py`)

| Método | Rota | Função |
|---|---|---|
| GET, POST | `/auth/login` | Formulário e autenticação |
| GET | `/auth/logout` | Encerra a sessão |

### `main` — `/` (`app/controllers/main_controller.py`)

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Painel montado a partir do registro de portlets |
| GET | `/busca?q=` | Busca global (fragmento HTMX; mínimo 2 caracteres, até 5 por tipo) |

### `clientes` — `/clientes` (`app/controllers/cliente_controller.py`)

| Método | Rota | Função |
|---|---|---|
| GET | `/clientes/` | Listagem com `busca`, `situacao`, `filtro`, `tipo`, `pagina` |
| GET, POST | `/clientes/novo` | Cadastro |
| GET | `/clientes/<id>` | Detalhe, com o painel de contatos |
| GET, POST | `/clientes/<id>/editar` | Edição |
| POST | `/clientes/<id>/situacao` | Inativa ou reativa |
| GET | `/clientes/exportar?formato=` | Exportação `.xlsx`/`.csv` com os filtros da listagem |
| GET | `/clientes/importar/modelo` | Planilha modelo |
| GET, POST | `/clientes/importar` | Envio e validação da planilha |
| GET | `/clientes/importar/<token>` | Pré-visualização |
| GET | `/clientes/importar/<token>/erros` | CSV das linhas não importadas |
| POST | `/clientes/importar/<token>/confirmar` | Grava as linhas válidas |

### `contatos` (`app/controllers/contato_controller.py`)

| Método | Rota | Função |
|---|---|---|
| GET | `/contatos` | Listagem geral com busca |
| GET | `/clientes/<id>/contatos/novo` | Abre o formulário no painel (HTMX) |
| GET | `/clientes/<id>/contatos/cancelar` | Fecha o formulário (HTMX) |
| POST | `/clientes/<id>/contatos` | Cria contato |
| GET, POST | `/contatos/<id>/editar` | Edita contato |
| POST | `/contatos/<id>/excluir` | Remove contato |

## Padrões usados nos controllers

- **Resposta parcial para HTMX**: quando o cabeçalho `HX-Request` vem `true`, a rota devolve só o
  fragmento (`_tabela.html`, `_painel.html`); sem HTMX devolve a página inteira ou redireciona.
- **Normalização na borda**: `_aplicar_form_no_cliente` e `_aplicar_form_no_contato` copiam o
  formulário para o model já com `strip`, minúsculas no e-mail e só dígitos em documento,
  telefone e CEP.
- **Consulta compartilhada**: `_consulta_clientes_filtrada` é usada pela listagem e pela
  exportação, garantindo que o arquivo exportado é o mesmo recorte da tela.

## Importação de planilhas

Implementada em `app/utils/planilhas.py`:

1. `ler_planilha` lê `.xlsx` (openpyxl) ou `.csv` em dicionários brutos.
2. `validar_linhas` classifica cada linha como `ok`, `duplicado` ou `erro`, com o motivo.
3. `salvar_pendente` grava o resultado em JSON numa pasta temporária do sistema
   (`crm_importacoes/`) e devolve um token hexadecimal de 32 caracteres.
4. A confirmação revalida a duplicidade, grava cada cliente (e o contato principal, se houver) em
   sua própria transação e descarta o pendente.

## CLI

| Comando | Faz |
|---|---|
| `flask init-db` | Cria as tabelas |
| `flask criar-usuario NOME EMAIL SENHA` | Cria um usuário (recusa e-mail repetido) |
