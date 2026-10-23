# Skills e plugins base

Os tres primeiros ja estao declarados em `.claude/settings.json`: ao abrir esta pasta no Claude
Code e confiar nela, ele oferece instalar. Os demais sao instalados uma vez por maquina.

| Skill | Para que serve | Instalacao |
|---|---|---|
| **superpowers** | Metodo de trabalho: brainstorming → design → plano → execucao, debug sistematico, revisao | Automatico (settings). Manual: `/plugin install superpowers@claude-plugins-official` |
| **ponytail** | Forca a solucao mais simples que funciona; evita over-engineering no codigo | Automatico (settings). Manual: `/plugin marketplace add DietrichGebert/ponytail` e `/plugin install ponytail@ponytail` |
| **humanizer** | Reescreve texto com cara de IA para soar natural (e-mails, documentos ao cliente) | Automatico (settings). Manual: `/plugin marketplace add blader/humanizer` e `/plugin install humanizer@humanizer` |
| **scrapling** | Raspagem/extracao de dados de paginas web | Ver abaixo |
| **browser-harness** | Claude usa o seu Chrome real (logado) via DevTools — sistemas web do cliente | Ver abaixo |
| **notebooklm-py** | Cria cadernos no NotebookLM, adiciona fontes, gera resumos/audios | Ver abaixo |

## scrapling — [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)

Com Node.js 18 ou mais novo (`node --version`):

```bash
npx skills add D4Vinci/Scrapling --skill scrapling-official --global --agent claude-code -y
```

Com Node 16 ou mais antigo o comando falha (`styleText` nao encontrado). Alternativa sem Node:
baixar o zip oficial e extrair a pasta em `~/.claude/skills/scrapling-official`:

```bash
curl -sSL -o Scrapling-Skill.zip https://github.com/D4Vinci/Scrapling/raw/refs/heads/main/agent-skill/Scrapling-Skill.zip
unzip -q Scrapling-Skill.zip -d scrapling_tmp
cp -r scrapling_tmp/Scrapling-Skill ~/.claude/skills/scrapling-official
```

## browser-harness — [browser-use/browser-harness](https://github.com/browser-use/browser-harness)

Requer `uv` e Chrome 144+. A documentacao oficial so traz comandos de Linux/Mac; no Windows
(Git Bash) funciona assim:

```bash
uv tool install --python 3.12 --upgrade --force browser-harness
mkdir -p ~/.claude/skills/browser-harness
~/.local/bin/browser-harness skill > ~/.claude/skills/browser-harness/SKILL.md
```

O ultimo comando imprime a skill e grava no lugar onde o Claude Code procura. Nao gere esse
arquivo pelo PowerShell 5.1 (`>` grava com BOM/UTF-16 e o Claude nao reconhece a skill).

Depois, no Chrome: `chrome://inspect/#remote-debugging` → marcar
**"Allow remote debugging for this browser instance"** → aprovar a conexao. Sem isso o teste
falha com `DevToolsActivePort not found`. Teste:

```bash
printf 'print(page_info())\n' | browser-harness
```

## notebooklm-py — [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)

```bash
uv tool install "notebooklm-py[browser]"
notebooklm login
notebooklm skill install
```

`notebooklm login` abre o login Google (baixa ~170 MB de Chromium na primeira vez).
Conferir: `notebooklm auth check --test --json` deve retornar `"status": "ok"`.
