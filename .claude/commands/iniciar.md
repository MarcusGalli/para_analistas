---
description: Verifica e completa a configuracao inicial do ambiente do analista (projetos, SVN, bancos, skills)
---

# Verificacao do ambiente do analista

Voce esta ajudando um analista, possivelmente com pouca experiencia em Claude Code, a deixar o
ambiente pronto. Linguagem simples, **uma pergunta por vez**, e mostre o comando quando pedir
que ele faca algo. Nunca peca senha ou token no chat: o analista edita `.secrets/` sozinho.

Execute as etapas na ordem. Em cada uma: verifique, corrija o que puder, pergunte o que faltar.

## 0. Repositorio do projeto

Rode `git remote get-url origin`. Se **nao** terminar em `/para_analistas.git` (ou `/para_analistas`),
esta pasta ja e o repositorio de um projeto: pule para a etapa 1.

Se terminar, esta pasta e um clone do **seed** (modelo em branco). Explique isso ao analista: as
fichas que vamos preencher sao do projeto dele e nao podem ir para o seed. Entao:

1. Pergunte se a equipe do projeto **ja tem** um repositorio criado a partir do seed.
   - Sim: oriente a clonar o da equipe em outra pasta (`git clone <url>`), abrir o Claude Code
     nela e rodar `/iniciar` la. Encerre aqui.
2. Nao: confirme o login com `gh auth status` (se falhar, oriente
   `gh auth login --hostname github.com --git-protocol https --web` e `gh auth setup-git`).
3. Pergunte a sigla do projeto/superintendencia e sugira o nome `analistas-<sigla>` (minusculas).
   Pergunte o dono: a conta do analista (`gh api user -q .login`) ou uma organizacao.
4. Com o OK dele, crie o repositorio privado e mude a pasta para ele, mantendo o seed como `seed`:

   ```bash
   gh repo create <dono>/analistas-<sigla> --private --description "Ambiente dos analistas <SIGLA> com o Claude (seed para_analistas)"
   git remote rename origin seed
   git remote add origin https://github.com/<dono>/analistas-<sigla>.git
   git push -u origin main
   ```

   (O repositorio novo recebe o historico do seed; assim melhorias futuras entram com `git pull seed main`.)
5. No topo do `README.md`, troque o aviso "Este repositorio e um seed" por uma frase dizendo que
   este e o repositorio do projeto `<SIGLA>`, criado a partir do seed. Faca commit e push.

## 1. Ferramentas

Verifique (sem instalar nada ainda): `git --version`, `uv --version`, `svn --version --quiet`,
`node --version` (precisa >= 18), `gh auth status`.
Para o que faltar, mostre o comando de instalacao da tabela de `PRIMEIROS_PASSOS.md` e pergunte
se pode instalar ou se o analista prefere fazer.

## 2. Projetos (`.projetos/`)

- Liste as subpastas de `.projetos/` (ignore `README.md`).
- Nenhuma: pergunte se ele trabalha em algum projeto e qual a URL git. Se informar, clone em
  `.projetos/<nome>`. Pode ser mais de um; pergunte se ha outros.
- Para cada projeto sem ficha em `contexto/PROJETOS.md`: leia README, estrutura e arquivos de
  build, preencha a ficha pelo modelo e pergunte so o que o codigo nao responde
  (cliente/superintendencia, observacoes).

## 3. SVN (`.SVN/`)

- Liste as subpastas de `.SVN/` e rode `svn info` em cada uma.
- Nenhuma: pergunte a URL do SVN de documentacao e faca `svn checkout <url> .SVN/<nome>`
  (se pedir login, o analista digita no terminal dele; alternativa: TortoiseSVN > SVN Checkout).
- Para cada working copy sem ficha em `contexto/SVN.md`: liste as pastas principais, pergunte
  onde salvar relatorios, especificacoes, scripts SQL e documentos ao cliente, e o padrao de
  mensagem de commit. Preencha a ficha.

## 4. Bancos (`.secrets/bancos.toml`)

- Verifique se o arquivo existe com `test -f .secrets/bancos.toml` (nao abra o arquivo).
- Nao existe: oriente a copiar `.secrets/bancos.toml.exemplo` para `.secrets/bancos.toml` e
  preencher no Bloco de Notas. Espere ele avisar que terminou.
- Rode `uv run ferramentas/db.py --autoteste` e `uv run ferramentas/db.py --listar`.
  Se os apelidos ainda forem os do exemplo (`prod_legado`, `homolog_sistema` com `troque-me`), avise.
- Teste cada apelido com `uv run ferramentas/db.py <apelido> "select 1 from dual"`.
  Erro de conexao: explique a provavel causa (VPN/rede, usuario/senha, DSN, modo thick) sem
  mostrar credenciais.
- Para cada apelido sem ficha em `contexto/BANCOS.md`: pergunte ambiente (producao/homologacao/
  desenvolvimento) e sistema; liste os schemas acessiveis
  (`select username from all_users order by 1`) e pergunte quais importam. Preencha a ficha.

## 5. Skills

- Plugins: `claude plugin list` deve mostrar superpowers, ponytail e humanizer habilitados.
- Skills: devem existir `~/.claude/skills/scrapling-official`, `~/.claude/skills/browser-harness`
  e `~/.claude/skills/notebooklm`.
- Para o que faltar, ofereca instalar seguindo `contexto/SKILLS.md` (explique em uma linha para
  que serve cada uma). Passos que dependem do analista: login do NotebookLM
  (`notebooklm login`) e remote debugging do Chrome para o browser-harness.

## 6. Resumo

Termine com uma tabela: etapa | situacao (OK / pendente / com erro) | o que falta fazer.
Liste as fichas de `contexto/` que voce criou ou alterou e ofereca fazer commit e push delas no
repositorio do projeto (nunca no seed). Se tudo estiver OK, sugira 2 ou 3
pedidos de exemplo usando os projetos e bancos que ele acabou de configurar.
