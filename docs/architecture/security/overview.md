---
type: architecture
status: current
---
# Segurança

## Autenticação

- Sessão pelo Flask-Login; `@login_required` em todas as rotas internas.
- Senha guardada só como hash (`generate_password_hash` do Werkzeug); nunca em texto puro.
- Mensagem de erro única para e-mail inexistente e senha errada, para não revelar quais e-mails
  existem.
- Conta desativada (`Usuario.ativo = False`) não consegue entrar.
- Parâmetro `next` aceito só como caminho relativo (`_destino_seguro`), evitando *open redirect*.
- Usuários são criados apenas pela CLI; não há cadastro público.

## Autorização

Ainda não há perfis: todo usuário autenticado pode tudo. Perfis de administrador e vendedor estão
previstos (ver [escopo](../../product/scope.md)).

## CSRF

`CSRFProtect` global (Flask-WTF). Desligado apenas na configuração de testes.

## Validação de entrada

| Entrada | Validação |
|---|---|
| Formulários | WTForms, com regra de documento e duplicidade em `ClienteForm.validate_documento` |
| Documento | CPF/CNPJ pelo módulo 11, gravado só com dígitos |
| Planilhas | Extensão `.xlsx`/`.csv`, leitura real do arquivo, validação linha a linha com as mesmas regras do formulário |
| Token de importação | Formato hexadecimal de 32 caracteres antes de montar o caminho do arquivo |
| Exportação CSV | Células iniciadas por `=`, `+`, `-` ou `@` são neutralizadas contra *CSV injection* |

## Dados pessoais

O sistema guarda nome, CPF, e-mail, telefone e endereço de pessoas físicas — dados pessoais
segundo a LGPD. A análise de conformidade ainda não foi feita (skill `lgpd-checklist`).

## Pontos em aberto

- `SECRET_KEY` tem um valor padrão de desenvolvimento em `config.py`; produção precisa defini-la
  pelo ambiente.
- Cookies de sessão sem `Secure`/`SameSite` explícitos.
- Sem limite de tentativas de login.
- Sem limite de tamanho de upload (`MAX_CONTENT_LENGTH`).
