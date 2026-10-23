# Skills e plugins base

Os tres primeiros ja estao declarados em `.claude/settings.json`: ao abrir esta pasta no Claude
Code e confiar nela, ele oferece instalar. Os demais sao instalados uma vez por maquina.

| Skill | Para que serve | Instalacao |
|---|---|---|
| **superpowers** | Metodo de trabalho: brainstorming → design → plano → execucao, debug sistematico, revisao | Automatico (settings). Manual: `/plugin install superpowers@claude-plugins-official` |
| **ponytail** | Forca a solucao mais simples que funciona; evita over-engineering no codigo | Automatico (settings). Manual: `/plugin marketplace add DietrichGebert/ponytail` e `/plugin install ponytail@ponytail` |
| **humanizer** | Reescreve texto com cara de IA para soar natural (e-mails, documentos ao cliente) | Automatico (settings). Manual: `/plugin marketplace add blader/humanizer` e `/plugin install humanizer@humanizer` |
| **scrapling** | Raspagem/extracao de dados de paginas web | `npx skills add D4Vinci/Scrapling --skill scrapling-official` |
| **browser-harness** | Claude usa o seu Chrome real (logado) via DevTools — sistemas web do cliente | Ver abaixo |
| **notebooklm-py** | Cria cadernos no NotebookLM, adiciona fontes, gera resumos/audios | Ver abaixo |

## browser-harness — [browser-use/browser-harness](https://github.com/browser-use/browser-harness)

Requer `uv` e Chrome 144+. Cole no Claude Code:

> Install or upgrade browser-harness to the latest stable version with uv using Python 3.12,
> register the skill from `browser-harness skill`, and connect it to my browser.

Depois, no Chrome: `chrome://inspect/#remote-debugging` → marcar remote debugging → aprovar.

## notebooklm-py — [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)

```bash
uv tool install "notebooklm-py[browser]"
notebooklm login
notebooklm skill install
```

`notebooklm login` abre o login Google (baixa ~170 MB de Chromium na primeira vez).
Conferir: `notebooklm auth check --test --json` deve retornar `"status": "ok"`.
