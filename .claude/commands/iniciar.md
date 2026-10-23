---
description: Verifica e completa a configuracao inicial do ambiente do analista (projetos, SVN, bancos, skills)
---

# Verificacao do ambiente do analista

Voce esta ajudando um analista, possivelmente com pouca experiencia em Claude Code, a deixar o
ambiente pronto. Linguagem simples, **uma pergunta por vez**, e mostre o comando quando pedir
que ele faca algo. Nunca peca senha ou token no chat: o analista edita `.secrets/` sozinho.

Execute as etapas na ordem. Em cada uma: verifique, corrija o que puder, pergunte o que faltar.

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
Liste as fichas de `contexto/` que voce criou ou alterou. Se tudo estiver OK, sugira 2 ou 3
pedidos de exemplo usando os projetos e bancos que ele acabou de configurar.
