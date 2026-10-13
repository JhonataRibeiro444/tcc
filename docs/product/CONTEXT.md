---
type: product
status: current
---
# Glossário do domínio

Vocabulário usado no código, nas issues e no texto do TCC. Ao nomear algo novo, use estes termos;
ao precisar de um termo novo, acrescente-o aqui primeiro.

| Termo | Significado | No código |
|---|---|---|
| Usuário | Pessoa que acessa o sistema com e-mail e senha | `Usuario` |
| Cliente | Pessoa física ou jurídica com quem a empresa se relaciona | `Cliente` |
| Tipo de pessoa | `F` (pessoa física, CPF) ou `J` (pessoa jurídica, CNPJ) | `Cliente.tipo_pessoa` |
| Documento | CPF ou CNPJ do cliente, guardado só com dígitos e único na base | `Cliente.documento` |
| Nome fantasia | Nome comercial de uma pessoa jurídica | `Cliente.nome_fantasia` |
| Situação | Cliente ativo ou inativo | `Cliente.ativo` |
| Inativar | Tirar o cliente de circulação sem apagá-lo; reversível | `alternar_situacao` |
| Contato | Pessoa vinculada a um cliente (comprador, financeiro, diretor…) | `Contato` |
| Contato principal | O contato a procurar primeiro; no máximo um por cliente | `Contato.principal` |
| Cadastro incompleto | Cliente ativo sem e-mail ou sem telefone | `filtro=incompleto` |
| Sem contato | Cliente ativo sem nenhum contato cadastrado | `filtro=sem_contato` |
| Painel | Tela inicial, composta por portlets | `main.index` |
| Portlet | Bloco independente do painel, com título, template e função de dados | `app/portlets.py` |
| Lembrete | Item do portlet de lembretes que aponta uma situação que pede atenção | `_dados_lembretes` |
| Busca global | Busca da barra superior, em clientes e contatos ao mesmo tempo | `main.busca` |
| Importação pendente | Resultado validado de uma planilha, ainda não gravado, identificado por um token | `planilhas.salvar_pendente` |

## Termos a evitar

- **Excluir cliente** — o sistema inativa; "excluir" só vale para contatos.
- **Lead / oportunidade** — ainda não existem no sistema (previstos nos próximos passos).
