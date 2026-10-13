---
type: engineering
status: current
---
# Setup local

## Pré-requisitos

- Python 3.10 ou mais novo, de verdade instalado (no Windows, o atalho da Microsoft Store não serve)
- Git

## Primeira vez

```powershell
setup.bat
```

```bash
bash setup.sh
```

O script cria o `venv`, instala `requirements.txt`, copia `.env.example` para `.env`, cria as
tabelas e oferece o cadastro do primeiro usuário.

## Dia a dia

```powershell
venv\Scripts\activate
python run.py
```

A aplicação sobe em <http://127.0.0.1:5000>.

## Variáveis de ambiente

| Variável | Padrão no `.env.example` | Para quê |
|---|---|---|
| `SECRET_KEY` | `troque-esta-chave` | Assina a sessão e o CSRF; troque em qualquer ambiente compartilhado |
| `DATABASE_URL` | `sqlite:///app.db` | Banco; caminho relativo é resolvido dentro de `instance/` |
| `FLASK_CONFIG` | `development` | `development`, `testing` ou `production` |

O `.flaskenv` define `FLASK_APP=run.py` e `FLASK_DEBUG=1`.

Sem `.env`, o `config.py` usa `SECRET_KEY` de desenvolvimento e cria o banco em `app.db` na raiz
do projeto, não em `instance/`. Os dois caminhos estão no `.gitignore`.

## Comandos úteis

| Comando | Faz |
|---|---|
| `flask init-db` | Cria as tabelas |
| `flask criar-usuario "Nome" email senha` | Cria um usuário |
| `python -m pytest` | Roda a suíte de testes |

## Recriar o banco

Não há migrations. Para aplicar mudanças de schema no desenvolvimento, apague
`instance/app.db` e rode `flask init-db` e `flask criar-usuario` de novo.
