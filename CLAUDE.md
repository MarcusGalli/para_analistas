# Ambiente do Analista

Espaco de trabalho onde o analista, junto com o Claude, **le e altera codigo-fonte**, **consulta
bancos de dados** e **gera documentos** que vao para o SVN do cliente. Tudo gira em torno de
Projetos, Superintendencias, Ordens de Servico (OS), orcamento e entregas.

## Estrutura

| Pasta | Conteudo | No git deste repo? |
|---|---|---|
| `.projetos/<nome>/` | Clones git dos projetos do cliente | Nao (local do analista) |
| `.SVN/<nome>/` | Working copies SVN com a documentacao do cliente | Nao (local do analista) |
| `.secrets/` | Credenciais (`bancos.toml` e outros) | Nao — nunca |
| `saidas/` | Resultados temporarios (CSV de consultas, rascunhos) | Nao |
| `ferramentas/db.py` | Consulta somente leitura aos bancos | Sim |
| `contexto/` | Fichas de projetos, SVN e bancos — **mantidas pelo Claude** | Sim |

## Contexto disponivel (atualize sempre que algo mudar)

@contexto/PROJETOS.md
@contexto/SVN.md
@contexto/BANCOS.md

Skills recomendadas e instalacao: `contexto/SKILLS.md`.

## Regras

### Segredos
- Nunca ler, exibir, copiar ou editar arquivos de `.secrets/`. O analista preenche; o `db.py` le.
- Nunca escrever senha, token ou string de conexao com senha em `.md`, SQL, codigo, commit ou resposta.
- Se precisar de uma credencial nova, diga ao analista qual arquivo/chave preencher (veja `.secrets/README.md`).

### Banco de dados
- Consultar **somente** via `uv run ferramentas/db.py <apelido> ...` (`--listar` mostra os apelidos).
  O script so aceita SELECT/WITH, roda em transacao READ ONLY e nunca faz commit.
- Antes de consultar, consulte `contexto/BANCOS.md` para escolher o apelido e entender o ambiente.
  Ao usar um apelido de **producao**, diga isso ao analista na resposta.
- Comece com `--max` pequeno; resultado grande vai para `--csv saidas/<nome>.csv`.
- Consulta potencialmente pesada em producao (sem filtro, full scan em tabela grande): pergunte antes.
- Alteracao de dados (UPDATE/INSERT/DELETE/DDL): gere o script em arquivo `.sql`, com SELECT de
  conferencia antes/depois e rollback comentado. **Quem executa e o analista**, na ferramenta dele.
- Aprendeu algo do modelo de dados (significado de codigos, relacoes, armadilhas)? Registre em
  `contexto/BANCOS.md` na secao do banco.

### Codigo-fonte (`.projetos/`)
- Antes de trabalhar num projeto, leia a ficha dele em `contexto/PROJETOS.md` e o README/CLAUDE.md do proprio projeto.
- Alteracoes sempre em branch propria; nunca commit, push ou merge sem o analista pedir.
- Siga as convencoes do projeto (estilo, testes, estrutura) — nao as deste repositorio.

### Documentos e SVN (`.SVN/`)
- Documento gerado (relatorio, especificacao, design/plano de skills, SQL que vale guardar) e salvo
  **dentro da working copy SVN** do projeto, na pasta indicada em `contexto/SVN.md`.
  Sem SVN definido para o assunto: salve em `saidas/` e avise.
- Nome de arquivo: `AAAA-MM-DD-tema-curto.ext` (ex.: `2026-10-23-relatorio-titulos-pendentes.md`).
- `svn add`/`svn commit` so depois de mostrar a lista de arquivos e o analista confirmar.
  Mensagem de commit em portugues, descrevendo o que e o documento (e a OS, quando houver).
- Rode `svn update` antes de editar documento existente.
- Dados pessoais (CPF, nome de pessoa fisica, endereco) nao vao para documentos sem o analista
  aprovar; prefira agregados ou mascarar.

### Fichas em `contexto/`
- Ao clonar projeto, fazer checkout SVN ou o analista cadastrar banco novo: crie/atualize a ficha
  correspondente seguindo o modelo do proprio arquivo, e informe o que registrou.
- Fichas sao curtas e factuais (sao carregadas em toda sessao). Detalhe longo vai para documento no SVN, com link na ficha.
