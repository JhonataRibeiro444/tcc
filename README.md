# CRM - TCC Daniel e Jhonatan

Sistema de CRM (Customer Relationship Management) desenvolvido como Trabalho de
Conclusao de Curso. Esta etapa contempla o nucleo cadastral do sistema:
autenticacao de usuarios, gestao de clientes (pessoa fisica e juridica) e
gestao dos contatos vinculados a cada cliente.

## Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.10+ |
| Framework web | Flask 3 |
| ORM | Flask-SQLAlchemy |
| Banco de dados | SQLite (desenvolvimento) |
| Autenticacao | Flask-Login + hash de senha (Werkzeug) |
| Formularios e CSRF | Flask-WTF / WTForms |
| Interface | Jinja2 + Bootstrap 5 + HTMX |
| Testes | pytest |

## Arquitetura

O projeto segue o padrao **MVC** adaptado ao Flask, com o *application factory*
(`create_app`) e Blueprints para separar os modulos:

```
tcc-crm-daniel-e-jhonatan/
|-- config.py                 # Configuracoes por ambiente (dev, teste, producao)
|-- run.py                    # Ponto de entrada da aplicacao
|-- app/
|   |-- __init__.py           # Application factory e registro das extensoes
|   |-- cli.py                # Comandos: init-db, criar-usuario
|   |-- models/               # Camada de dominio (SQLAlchemy)
|   |   |-- usuario.py
|   |   |-- cliente.py
|   |   `-- contato.py
|   |-- forms/                # Validacao das entradas (WTForms)
|   |-- controllers/          # Blueprints (rotas e regras de aplicacao)
|   |   |-- auth_controller.py
|   |   |-- cliente_controller.py
|   |   |-- contato_controller.py
|   |   `-- main_controller.py
|   |-- utils/
|   |   `-- validators.py     # Validacao de CPF/CNPJ e formatacao
|   |-- views/templates/      # Camada de apresentacao (Jinja2)
|   `-- static/css/
`-- tests/                    # Suite de testes automatizados
```

## Modelo de dados

- **Usuario** - quem acessa o sistema. A senha nunca e armazenada em texto
  puro, apenas o hash gerado pelo Werkzeug.
- **Cliente** - pessoa fisica ou juridica. O documento (CPF/CNPJ) e validado
  pelo algoritmo de digitos verificadores modulo 11, gravado somente com
  digitos e restrito a valores unicos.
- **Contato** - pessoa vinculada a um cliente (relacao 1:N). Cada cliente pode
  ter no maximo um contato marcado como principal.

Clientes nao sao excluidos: sao **inativados**, o que preserva o historico
cadastral. Os contatos, por serem subordinados ao cliente, sao removidos em
cascata caso o cliente seja apagado.

## Como executar

### Caminho rapido (recomendado)

Na primeira vez, execute o script de configuracao. Ele cria o ambiente virtual,
instala as dependencias, gera o `.env`, cria as tabelas e oferece o cadastro do
primeiro usuario.

```bash
setup.bat        # Windows (ou dois cliques no arquivo)
bash setup.sh    # Linux / macOS
```

Depois disso, no dia a dia:

```bash
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS
python run.py
```

### Caminho manual

```bash
# 1. Ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

# 2. Dependencias
pip install -r requirements.txt

# 3. Variaveis de ambiente
copy .env.example .env       # Windows
# cp .env.example .env       # Linux / macOS

# 4. Banco de dados e primeiro usuario
flask init-db
flask criar-usuario "Daniel" "daniel@exemplo.com" "uma-senha-boa"

# 5. Executar
python run.py
```

O arquivo `.flaskenv` ja define `FLASK_APP=run.py`, entao o comando `flask` funciona
sem configuracao extra. O banco SQLite e criado em `instance/app.db` — o Flask
resolve caminhos relativos dentro dessa pasta, que esta no `.gitignore`.

A aplicacao fica disponivel em <http://127.0.0.1:5000>.

## Testes

```bash
python -m pytest
```

A suite cobre os validadores de documento, o fluxo de autenticacao e o CRUD de
clientes e contatos, incluindo as respostas parciais usadas pelo HTMX.

## Funcionalidades implementadas

- [x] Login e logout com senha protegida por hash
- [x] Protecao de todas as rotas internas e protecao CSRF nos formularios
- [x] Cadastro, edicao e consulta de clientes (PF e PJ)
- [x] Validacao de CPF e CNPJ com verificacao de duplicidade
- [x] Busca dinamica por nome, documento ou e-mail (sem recarregar a pagina)
- [x] Filtro por situacao e paginacao dos resultados
- [x] Inativacao e reativacao de clientes
- [x] Cadastro, edicao e remocao de contatos por cliente, com contato principal
- [x] Painel com indicadores da base de clientes

## Proximos passos

- Modulo de oportunidades com estagios de funil de vendas
- Registro de interacoes (ligacoes, e-mails, reunioes) por cliente
- Perfis de acesso (administrador e vendedor)
- Relatorios e exportacao de dados
