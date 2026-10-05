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
| Interface | Jinja2 + Bootstrap 5 + HTMX + JavaScript proprio |
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
|   |   |-- validators.py     # Validacao de CPF/CNPJ e formatacao
|   |   `-- planilhas.py      # Importacao/exportacao de clientes via .xlsx/.csv
|   |-- portlets.py          # Registro dos blocos do painel inicial
|   |-- views/templates/      # Camada de apresentacao (Jinja2)
|   |   `-- portlets/         # Um template por portlet
|   `-- static/
|       |-- css/tema.css      # Camada de tema sobre o Bootstrap
|       `-- js/               # Mascaras, validacao e interface
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

A suite cobre os validadores de documento, o fluxo de autenticacao, o CRUD de
clientes e contatos (incluindo as respostas parciais usadas pelo HTMX) e a
importacao/exportacao de planilhas.

## Interface

O layout se inspira na organizacao de tela dos sistemas de gestao
empresarial (o Oracle NetSuite serviu de referencia): uma faixa superior
clara com a busca global e a identificacao do usuario, uma faixa escura
com os modulos, e o conteudo dividido em portlets.

Os portlets do painel inicial vem de um registro em `app/portlets.py`:
cada um declara chave, titulo, coluna e a funcao que busca seus dados.
Adicionar um portlet novo e acrescentar uma entrada nesse registro. Nesta
versao o layout e fixo; a personalizacao por usuario esta prevista nos
proximos passos e reaproveita esse mesmo registro.

## Funcionalidades implementadas

- [x] Login e logout com senha protegida por hash
- [x] Protecao de todas as rotas internas e protecao CSRF nos formularios
- [x] Cadastro, edicao e consulta de clientes (PF e PJ)
- [x] Validacao de CPF e CNPJ com verificacao de duplicidade
- [x] Busca dinamica por nome, documento ou e-mail (sem recarregar a pagina)
- [x] Filtro por situacao e paginacao dos resultados
- [x] Inativacao e reativacao de clientes
- [x] Cadastro, edicao e remocao de contatos por cliente, com contato principal
- [x] Painel inicial em portlets: configuracoes rapidas, lembretes,
      resumo da base e ultimos cadastros
- [x] Busca global de clientes e contatos na barra superior
- [x] Listagem geral de contatos com busca
- [x] Filtros de apoio na listagem (sem contato, cadastro incompleto, tipo)
- [x] Importacao de clientes (com contato principal opcional) a partir de
      planilha .xlsx ou .csv, com pre-visualizacao e relatorio de erros antes
      de gravar
- [x] Exportacao de clientes para .xlsx ou .csv, respeitando os filtros da
      listagem

## Proximos passos

- Modulo de oportunidades com estagios de funil de vendas
- Registro de interacoes (ligacoes, e-mails, reunioes) por cliente
- Perfis de acesso (administrador e vendedor), exibidos junto ao nome do
  usuario na barra superior
- Painel configuravel: reordenar e mostrar/ocultar portlets, salvo por
  usuario
- Relatorios gerenciais (alem da exportacao de clientes ja disponivel)

Desenvolvido por Daniel Amaral e Jhonatan Ribeiro
