# Primeiros passos

Roteiro para deixar o ambiente pronto na sua maquina. Faca na ordem; no fim, o Claude confere
tudo com o comando `/iniciar`.

## 1. Instale as ferramentas (uma vez por maquina)

| Ferramenta | Para que | Como instalar |
|---|---|---|
| Claude Code | — | https://claude.com/claude-code |
| Git | clonar projetos | `winget install Git.Git` |
| GitHub CLI | login no GitHub | `winget install GitHub.cli` |
| uv | rodar `ferramentas/db.py` e instalar skills (instala Python sozinho) | `winget install astral-sh.uv` |
| Node.js 18 ou mais novo | instalar skills via `npx` | `winget install OpenJS.NodeJS.LTS` |
| SVN de linha de comando | o Claude ler/enviar documentos ao SVN | TortoiseSVN (https://tortoisesvn.net) marcando **"command line client tools"** na instalacao |
| Oracle Instant Client (opcional) | so para bancos Oracle antigos que recusam o modo thin | descompactar em `C:\oracle\` |

Depois de instalar, feche e abra o terminal para ele reconhecer os comandos novos.

## 2. Pegue o repositorio do seu projeto

Este repositorio (`para_analistas`) e o **seed**: um modelo em branco. Cada projeto/equipe tem
o seu proprio repositorio criado a partir dele, onde ficam as fichas de `contexto/` daquele
projeto, compartilhadas pela equipe.

Primeiro, login no GitHub (uma vez por maquina):

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

**A equipe do seu projeto ja tem repositorio?** Clone o dela:

```bash
git clone https://github.com/<dono>/<repositorio-do-projeto>.git
cd <repositorio-do-projeto>
```

**Projeto novo, ainda sem repositorio?** Clone o seed:

```bash
git clone https://github.com/MarcusGalli/para_analistas.git analistas-<sigla>
cd analistas-<sigla>
```

Nao se preocupe com o repositorio do projeto agora: ao rodar `/iniciar` (passo 6), o Claude
percebe que a pasta veio do seed, sugere o nome `analistas-<sigla>`, cria o repositorio privado
do seu projeto e passa a pasta para ele. O seed continua ligado como `seed`, para receber melhorias.

> Como os passos 3 a 5 so criam arquivos locais (ignorados pelo git), voce pode faze-los antes
> ou deixar o `/iniciar` guiar tudo.

## 3. Configure os bancos de dados

```bash
cp .secrets/bancos.toml.exemplo .secrets/bancos.toml
notepad .secrets/bancos.toml
```

Cada bloco `[bancos.<apelido>]` e uma conexao. Troque os exemplos pelos seus acessos:

| Campo | O que colocar |
|---|---|
| `[bancos.<apelido>]` | Nome curto que voce vai usar com o Claude, ex.: `prod_legado`, `hml_sinaflor` |
| `tipo` | `oracle` |
| `dsn` | `servidor:porta/servico`, ex.: `banco.cliente.gov.br:1521/orasema` |
| `usuario` / `senha` | Seu login do banco (de preferencia somente leitura) |

Pode ter quantos blocos quiser. Esse arquivo **nunca vai para o git** e o Claude nao le o
conteudo dele. Para testar:

```bash
uv run ferramentas/db.py --listar
uv run ferramentas/db.py <apelido> "select 1 from dual"
```

## 4. Adicione os projetos em que voce trabalha

Um clone por projeto, dentro de `.projetos/`:

```bash
git clone <url-do-projeto> .projetos/<nome-do-projeto>
```

## 5. Adicione o SVN de documentacao

Um checkout por repositorio SVN, dentro de `.SVN/`:

```bash
svn checkout <url-do-svn> .SVN/<nome>
```

Prefere o TortoiseSVN? Clique com o botao direito em `.SVN` → **SVN Checkout** e informe a URL
e a pasta `.SVN\<nome>`.

## 6. Abra o Claude Code e rode a verificacao

```bash
claude
```

1. Aceite confiar na pasta e instalar os plugins sugeridos (superpowers, ponytail, humanizer).
2. Digite:

   ```
   /iniciar
   ```

O Claude confere ferramentas, projetos, SVN, bancos e skills, pergunta o que estiver faltando,
instala as skills que faltam e registra tudo nas fichas de `contexto/`. Pode rodar `/iniciar`
de novo sempre que adicionar um projeto, SVN ou banco.

> Se `/iniciar` nao aparecer, digite:
> *"Leia .claude/commands/iniciar.md e siga as instrucoes."*
