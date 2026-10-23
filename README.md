# Ambiente do Analista + Claude

Base para cada analista usar o Claude Code no dia a dia: ler e alterar o codigo-fonte dos
projetos, consultar os bancos do cliente e gerar documentos que vao para o SVN.

As regras que o Claude segue estao em [`CLAUDE.md`](CLAUDE.md).

## Pre-requisitos (uma vez por maquina)

| Ferramenta | Para que | Como |
|---|---|---|
| Claude Code | — | https://claude.com/claude-code |
| Git | clonar projetos | https://git-scm.com |
| uv | rodar `ferramentas/db.py` (instala Python e drivers sozinho) | `winget install astral-sh.uv` |
| SVN de linha de comando | Claude ler/enviar documentos ao SVN | TortoiseSVN marcando **"command line client tools"** na instalacao |
| Oracle Instant Client (opcional) | so para bancos Oracle antigos que recusam o modo thin | descompactar em `C:\oracle\` |

## Primeiro uso

```bash
git clone <url-deste-repositorio> ambiente-analista
cd ambiente-analista
cp .secrets/bancos.toml.exemplo .secrets/bancos.toml   # e preencha com seus acessos
uv run ferramentas/db.py --autoteste
uv run ferramentas/db.py --listar
```

1. Clone seus projetos em `.projetos/` e faca checkout dos SVNs em `.SVN/` (veja o README de cada pasta).
2. Abra o Claude Code nesta pasta, aceite os plugins sugeridos e instale os demais de [`contexto/SKILLS.md`](contexto/SKILLS.md).
3. Peca ao Claude para registrar o que voce adicionou:
   *"registre os projetos, SVNs e bancos que eu configurei"* — ele preenche as fichas em `contexto/`.

## Exemplos de pedidos

- "No banco `prod_legado`, quantos titulos AUTEX de 2026 estao sem integracao? Explique a consulta."
- "Procure no projeto `<nome>` onde e feita a validacao de <regra> e explique o fluxo."
- "Gere um relatorio em .md com o resultado e salve no SVN do projeto."
- "Monte o script de correcao para esses registros, com conferencia antes/depois." *(voce executa)*

## Seguranca

- `.secrets/`, `.projetos/`, `.SVN/` e `saidas/` sao ignorados pelo git — nada disso sobe.
- O Claude e bloqueado de ler `.secrets/`; o `db.py` so faz leitura (SELECT/WITH, transacao READ ONLY).
- Use usuario de banco somente leitura sempre que possivel.

## Proximos passos (planejado)

Fluxo centrado em **Ordem de Servico**: coleta de requisito → criacao da OS → orcamento →
documentacao → atividades e sprint → homologacao e producao → documentacao ao cliente →
atividades no Redmine → acompanhamento da OS, e-mails protocolares e reunioes.
