---
type: spec
status: current
labels: [area:auth]
depends_on: [1]
---
# 002 Autenticação

> Spec retroativo — documenta o que foi entregue no commit `4be6685` (2026-08-29).

## Problema

Um CRM guarda dados pessoais de clientes (CPF, telefone, e-mail). Só quem tem conta pode ver
ou alterar esses dados.

## Solução

Login por e-mail e senha, com a senha guardada apenas como hash, todas as rotas internas
protegidas e proteção CSRF em todos os formulários.

## Histórias de usuário

1. Como usuário, quero entrar com e-mail e senha, para acessar o CRM.
2. Como usuário, quero sair do sistema, para encerrar minha sessão num computador compartilhado.
3. Como usuário, quero opcionalmente continuar conectado, para não digitar a senha toda vez.
4. Como visitante sem login, quero ser levado à tela de entrada ao abrir qualquer página interna.
5. Como usuário, quero voltar à página que tentei abrir depois de fazer login.
6. Como responsável pelos dados, quero que a senha nunca fique gravada em texto puro.
7. Como responsável pelos dados, quero que a mensagem de erro não revele se um e-mail existe.
8. Como administrador, quero que contas desativadas não consigam entrar.

## Decisões de implementação

- Flask-Login para a sessão; hash de senha pelo Werkzeug (`generate_password_hash`).
- `@login_required` em todas as rotas internas.
- Parâmetro `next` aceito apenas como caminho relativo, para evitar *open redirect*.
- Mensagem única "E-mail ou senha incorretos." para e-mail inexistente e senha errada.
- `Usuario.ativo` alimenta `is_active` do Flask-Login, bloqueando contas desativadas.
- Flask-WTF com `CSRFProtect` global.
- Não há tela de cadastro de usuários: eles são criados por `flask criar-usuario`.

## Decisões de teste

- `tests/test_auth.py`: rota protegida redireciona, senha errada não autentica, login válido
  abre o painel, logout encerra a sessão, senha não é gravada em texto puro.

## Fora de escopo

- Perfis de acesso (administrador e vendedor) — previsto nos próximos passos.
- Recuperação de senha, limite de tentativas de login, MFA.

## Entregue em

| Fatia | Commit |
|---|---|
| Login e logout com hash de senha | `4be6685` |
| Proteção de rotas, CSRF e redirecionamento seguro | `4be6685` |
