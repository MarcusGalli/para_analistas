# Ambiente do Analista + Claude

Base para cada analista usar o Claude Code no dia a dia: ler e alterar o codigo-fonte dos
projetos, consultar os bancos do cliente e gerar documentos que vao para o SVN.

As regras que o Claude segue estao em [`CLAUDE.md`](CLAUDE.md).

## Comece por aqui

Siga o roteiro em **[PRIMEIROS_PASSOS.md](PRIMEIROS_PASSOS.md)**. Resumo:

1. Instale as ferramentas (Git, GitHub CLI, uv, Node 18+, TortoiseSVN com linha de comando).
2. Clone este repositorio.
3. Configure seus bancos em `.secrets/bancos.toml` (copiado de `bancos.toml.exemplo`).
4. Clone seus projetos em `.projetos/`.
5. Faca checkout do SVN de documentacao em `.SVN/`.
6. Abra o Claude Code nesta pasta e digite **`/iniciar`**: ele confere tudo, pergunta o que
   faltar, instala as skills e registra projetos, SVN e bancos nas fichas de `contexto/`.

Adicionou um projeto, SVN ou banco depois? Rode `/iniciar` de novo.

## Skills: o que sao e quais usamos

Uma **skill** e um pacote de instrucoes que ensina o Claude a fazer um tipo de tarefa de um jeito
especifico. Depois de instalada, **voce nao precisa chamar nada**: basta pedir normalmente
("reescreva esse e-mail para soar mais natural") e o Claude usa a skill quando ela se aplica.
Se quiser forcar, digite `/` no Claude Code e escolha a skill na lista.

Algumas vem como **plugin** (pacote que pode trazer varias skills e comandos). Para quem usa, nao
muda nada.

| Skill | Para que serve | Exemplo de pedido |
|---|---|---|
| [superpowers](https://github.com/obra/superpowers) | Da metodo ao trabalho: antes de mexer, entende o pedido, propoe um desenho, faz um plano e so entao executa. Tambem guia investigacao de bugs | "Quero criar uma tela de falhas de coleta, vamos planejar" |
| [ponytail](https://github.com/DietrichGebert/ponytail) | Faz o Claude escrever o codigo mais simples que resolve, sem complicar | Atua sozinho sempre que ha codigo |
| [humanizer](https://github.com/blader/humanizer) | Tira a "cara de IA" de textos: e-mails, relatorios e documentos para o cliente | "Revise esse e-mail para o cliente com a humanizer" |
| [scrapling](https://github.com/D4Vinci/Scrapling) | Coleta dados de paginas web, inclusive paginas dificeis de ler | "Extraia a tabela de normas desta pagina para CSV" |
| [browser-harness](https://github.com/browser-use/browser-harness) | Deixa o Claude usar o **seu** Chrome, ja logado, para navegar e preencher telas de sistemas web | "Abra o Redmine e liste minhas tarefas abertas" |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | Cria cadernos no NotebookLM do Google a partir de documentos e gera resumos e audios | "Crie um caderno com os documentos da OS e gere um resumo" |

Superpowers, ponytail e humanizer sao oferecidas automaticamente quando voce abre esta pasta no
Claude Code. As demais sao instaladas uma vez por maquina: peca ao Claude
*"instale as skills de contexto/SKILLS.md"* (comandos e detalhes em [`contexto/SKILLS.md`](contexto/SKILLS.md)).

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
