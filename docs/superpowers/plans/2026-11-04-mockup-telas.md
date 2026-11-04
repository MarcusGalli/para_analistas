# Skill mockup-telas — Plano de implementacao

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar no seed `para_analistas` a skill `mockup-telas` (levantar, nova, alterar, ajustar, finalizar) e a ferramenta que empacota o mockup autocontido e gera os PNGs.

**Architecture:** A skill e um roteiro em Markdown (`.claude/skills/mockup-telas/SKILL.md`) com modelos ao lado. O que e mecanico e precisa ser exato (embutir CSS/imagens/fontes em base64, tirar print de cada estado pelo Edge) fica num script Python so de stdlib, `ferramentas/mockup.py`, no mesmo estilo do `ferramentas/db.py` (cabecalho `uv` + `--autoteste`). Estados da tela sao `<section class="estado" id="...">` mostrados por `:target` (CSS puro, sem JS).

**Tech Stack:** Markdown (skill do Claude Code), Python 3.11+ stdlib via `uv run`, Microsoft Edge headless (ja vem no Windows), HTML/CSS.

**Spec:** `docs/superpowers/specs/2026-11-04-mockup-telas-design.md`

## Global Constraints

- Escopo v1: somente telas; relatorios, tarefas para devs e desktop ficam fora.
- A skill **nunca altera** `.projetos/` (somente leitura) e nunca faz commit/branch nos projetos.
- Login no sistema sempre feito pelo analista; a skill nunca pede, digita ou guarda senha.
- Nao faz `svn add`/commit, nao envia e-mail, nao cria atividade no Redmine.
- Contrato do pacote: `entrega/mockup.html` (autocontido), `entrega/telas/NN-<estado>.png`, `entrega/especificacao.md`.
- Por projeto: `contexto/telas/<projeto>/{PADROES.md, CATALOGO.md, kit/{kit.css, componentes.html, amostra.html, mockup-base.css, assets/}}`.
- Rascunhos: `saidas/mockups/AAAA-MM-DD-<tema>/{atual.html, vN.html, NOTAS.md, entrega/}`.
- Ordem das fontes de CSS: sistema rodando → repositorio → pacote publicado na versao exata (CDN) → reconstrucao por tokens.
- Dados ficticios nos mockups; dado real so via `db.py`, com dados pessoais mascarados.
- Script so com stdlib; textos e nomes em portugues sem acento (padrao do repo); `--autoteste` como no `db.py`.
- Commits: so quando o analista pedir; mensagem em portugues.

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `ferramentas/mockup.py` (criar) | `empacotar` (HTML autocontido) e `prints` (PNG por estado via Edge); `--autoteste` |
| `.claude/skills/mockup-telas/SKILL.md` (criar) | Roteiro da skill: modos, regras, convencoes do HTML |
| `.claude/skills/mockup-telas/modelos/mockup-base.css` (criar) | CSS dos estados, marcacoes de revisao e barra de navegacao |
| `.claude/skills/mockup-telas/modelos/rascunho.html` (criar) | Esqueleto de um `vN.html` |
| `.claude/skills/mockup-telas/modelos/PADROES.md` (criar) | Modelo do guia visual do projeto |
| `.claude/skills/mockup-telas/modelos/CATALOGO.md` (criar) | Modelo do catalogo de telas |
| `.claude/skills/mockup-telas/modelos/NOTAS.md` (criar) | Modelo do historico do pedido |
| `.claude/skills/mockup-telas/modelos/especificacao.md` (criar) | Modelo padrao da especificacao |
| `.claude/settings.json` (modificar) | Liberar `uv run ferramentas/mockup.py` |
| `contexto/SKILLS.md`, `CLAUDE.md`, `contexto/PROJETOS.md` (modificar) | Documentar a skill e a linha "Mockups" no modelo da ficha |

---

### Task 1: `ferramentas/mockup.py empacotar`

**Files:**
- Create: `ferramentas/mockup.py`

**Interfaces:**
- Produces: `empacotar(origem: Path, destino: Path) -> list[str]` (retorna referencias locais que nao foram encontradas); CLI `uv run ferramentas/mockup.py empacotar <rascunho.html> <saida.html>` (sai com codigo 1 se faltou algo, mas grava o arquivo); `--autoteste`.

- [ ] **Step 1: Escrever o script com o autoteste primeiro e `empacotar` vazio**

Criar `ferramentas/mockup.py`:

```python
# /// script
# requires-python = ">=3.11"
# ///
"""Ferramentas do pacote de mockup (skill mockup-telas).

  uv run ferramentas/mockup.py empacotar <rascunho.html> <saida.html>
  uv run ferramentas/mockup.py prints <mockup.html> <pasta> <estado> [<estado> ...] [--largura 1366] [--altura 900]
  uv run ferramentas/mockup.py --autoteste

empacotar: embute CSS (inclusive @import), fontes, imagens e scripts locais em um HTML unico.
prints: gera <pasta>/NN-<estado>.png abrindo <mockup.html>#<estado> no Edge headless.
"""
import argparse
import base64
import mimetypes
import re
import sys
import tempfile
from pathlib import Path

LINK_CSS = re.compile(r"<link\b[^>]*\brel=[\"']?stylesheet[\"']?[^>]*>", re.I)
HREF = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.I)
SCRIPT_SRC = re.compile(r"<script\b([^>]*?)\bsrc=([\"'])([^\"']+)\2([^>]*)>\s*</script>", re.I)
SRC = re.compile(r"(<(?:img|source)\b[^>]*?\bsrc=)([\"'])([^\"']+)\2", re.I)
IMPORT = re.compile(r"@import\s+(?:url\(\s*)?[\"']?([^\"')\s;]+)[\"']?\s*\)?[^;]*;", re.I)
URL_CSS = re.compile(r"url\(\s*([\"']?)([^\"')]+)\1\s*\)", re.I)
STYLE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.I | re.S)


def empacotar(origem, destino):
    raise NotImplementedError


def autoteste():
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        kit = raiz / "kit"
        (kit / "assets").mkdir(parents=True)
        (kit / "assets" / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\nfake")
        (kit / "assets" / "fonte.woff2").write_bytes(b"wOF2fake")
        (kit / "base.css").write_text("h1{color:#123456}", encoding="utf-8")
        (kit / "kit.css").write_text(
            '@import "base.css";\n'
            '@font-face{font-family:F;src:url("assets/fonte.woff2?v=1#iefix") format("woff2")}\n'
            "body{background:url(https://exemplo.com/fundo.png)}\n",
            encoding="utf-8",
        )
        (kit / "app.js").write_text("window.ok=1;", encoding="utf-8")
        (raiz / "v1.html").write_text(
            '<html><head><link rel="stylesheet" href="kit/kit.css">'
            "<style>.x{background:url('kit/assets/logo.png')}</style></head><body>"
            '<img src="kit/assets/logo.png"><img src="kit/assets/sumiu.png">'
            '<script src="kit/app.js"></script><a href="#edicao">ir</a></body></html>',
            encoding="utf-8",
        )
        saida = raiz / "entrega" / "mockup.html"
        faltando = empacotar(raiz / "v1.html", saida)
        html = saida.read_text(encoding="utf-8")
        assert faltando == ["kit/assets/sumiu.png"], faltando
        assert "<link" not in html, "link de CSS nao foi embutido"
        assert "#123456" in html, "@import nao foi embutido"
        assert "data:font/woff2;base64," in html or "data:application/octet-stream;base64," in html, "fonte nao embutida"
        assert html.count("data:image/png;base64,") == 2, "imagens (img e url no <style>) nao embutidas"
        assert "window.ok=1;" in html and 'src="kit/app.js"' not in html, "script nao embutido"
        assert "https://exemplo.com/fundo.png" in html, "url externa deveria ficar como esta"
        assert 'href="#edicao"' in html, "ancora deveria ficar como esta"
    print("autoteste empacotar: ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--autoteste", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("empacotar")
    e.add_argument("origem", type=Path)
    e.add_argument("destino", type=Path)
    a = ap.parse_args()
    if a.autoteste:
        autoteste()
    elif a.cmd == "empacotar":
        faltando = empacotar(a.origem, a.destino)
        print(f"gravado: {a.destino}")
        if faltando:
            print("AVISO - referencias locais nao encontradas (ficaram como estao):")
            for f in faltando:
                print(f"  {f}")
            sys.exit(1)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o autoteste e ver falhar**

Run (na raiz do seed): `uv run ferramentas/mockup.py --autoteste`
Expected: FAIL com `NotImplementedError`

- [ ] **Step 3: Implementar `empacotar`**

Substituir `def empacotar(origem, destino): raise NotImplementedError` por:

```python
def externo(ref):
    return ref.startswith(("http:", "https:", "data:", "//", "#", "mailto:"))


def limpo(ref):
    return ref.split("?")[0].split("#")[0]


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho.name)[0]
    if not tipo and caminho.suffix.lower() == ".woff2":
        tipo = "font/woff2"
    tipo = tipo or "application/octet-stream"
    return f"data:{tipo};base64,{base64.b64encode(caminho.read_bytes()).decode()}"


def embutir_css(css, base, faltando, raiz, vistos=None):
    """Embute @import e url() locais; `base` e a pasta do arquivo CSS."""
    vistos = vistos or set()

    def troca_import(m):
        ref = m.group(1)
        alvo = (base / limpo(ref)).resolve()
        if externo(ref):
            return m.group(0)
        if not alvo.is_file() or alvo in vistos:
            faltando.append(rel(alvo, raiz))
            return m.group(0)
        texto = alvo.read_text(encoding="utf-8", errors="replace")
        return embutir_css(texto, alvo.parent, faltando, raiz, vistos | {alvo})

    def troca_url(m):
        ref = m.group(2).strip()
        if externo(ref):
            return m.group(0)
        alvo = (base / limpo(ref)).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, raiz))
            return m.group(0)
        return f'url("{data_uri(alvo)}")'

    return URL_CSS.sub(troca_url, IMPORT.sub(troca_import, css))


def rel(alvo, raiz):
    try:
        return alvo.relative_to(raiz).as_posix()
    except ValueError:
        return alvo.as_posix()


def empacotar(origem, destino):
    origem = Path(origem).resolve()
    base = origem.parent
    html = origem.read_text(encoding="utf-8")
    faltando = []

    def troca_link(m):
        href = HREF.search(m.group(0))
        if not href or externo(href.group(1)):
            return m.group(0)
        alvo = (base / limpo(href.group(1))).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, base))
            return m.group(0)
        css = embutir_css(alvo.read_text(encoding="utf-8", errors="replace"), alvo.parent, faltando, base)
        return f"<style>\n{css}\n</style>"

    def troca_style(m):
        return m.group(1) + embutir_css(m.group(2), base, faltando, base) + m.group(3)

    def troca_script(m):
        ref = m.group(3)
        if externo(ref):
            return m.group(0)
        alvo = (base / limpo(ref)).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, base))
            return m.group(0)
        js = alvo.read_text(encoding="utf-8", errors="replace").replace("</script", "<\\/script")
        return f"<script{m.group(1)}{m.group(4)}>{js}</script>"

    def troca_src(m):
        ref = m.group(3)
        if externo(ref):
            return m.group(0)
        alvo = (base / limpo(ref)).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, base))
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}{data_uri(alvo)}{m.group(2)}"

    html = STYLE.sub(troca_style, html)  # antes do link: o CSS embutido do link ja vem resolvido
    html = LINK_CSS.sub(troca_link, html)
    html = SCRIPT_SRC.sub(troca_script, html)
    html = SRC.sub(troca_src, html)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")
    return sorted(set(faltando))
```

Observacao: `STYLE.sub` roda antes de `LINK_CSS.sub` para nao reprocessar o CSS ja embutido (que tem `data:` e seria ignorado de qualquer forma, mas evita custo com CSS grande do tema).

- [ ] **Step 4: Rodar o autoteste e ver passar**

Run: `uv run ferramentas/mockup.py --autoteste`
Expected: `autoteste empacotar: ok`

- [ ] **Step 5: Commit (quando o analista autorizar)**

```bash
git add ferramentas/mockup.py
git commit -m "Adiciona mockup.py empacotar: HTML autocontido para a skill mockup-telas"
```

---

### Task 2: `ferramentas/mockup.py prints`

**Files:**
- Modify: `ferramentas/mockup.py`

**Interfaces:**
- Consumes: `empacotar` (Task 1) apenas no autoteste final.
- Produces: `achar_edge() -> str | None`; `prints(html: Path, pasta: Path, estados: list[str], largura=1366, altura=900) -> list[Path]`; CLI `uv run ferramentas/mockup.py prints <mockup.html> <pasta> <estado>... [--largura N] [--altura N]`. Antes do print, injeta `<style>.mk-revisao{display:none!important}</style>` numa copia temporaria do HTML (na mesma pasta) para esconder a barra de revisao.

- [ ] **Step 1: Acrescentar o autoteste de `prints`**

Em `autoteste()`, depois do bloco do `empacotar` e antes do `print("autoteste empacotar: ok")`, nada muda; adicionar ao final da funcao:

```python
    if not achar_edge():
        print("autoteste prints: PULADO (Edge nao encontrado)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        pagina = raiz / "m.html"
        pagina.write_text(
            "<style>.estado{display:none;height:100vh}.estado:target{display:block}"
            "#a{background:#ff0000}#b{background:#0000ff}</style>"
            '<nav class="mk-revisao">barra</nav>'
            '<section class="estado" id="a"></section><section class="estado" id="b"></section>',
            encoding="utf-8",
        )
        pngs = prints(pagina, raiz / "telas", ["a", "b"], 400, 300)
        assert [p.name for p in pngs] == ["01-a.png", "02-b.png"], pngs
        assert all(p.stat().st_size > 0 for p in pngs), "png vazio"
        assert pngs[0].read_bytes() != pngs[1].read_bytes(), "estados geraram o mesmo print (ancora ignorada?)"
        assert sorted(x.name for x in raiz.iterdir()) == ["m.html", "telas"], "copia temporaria ficou para tras"
    print("autoteste prints: ok")
```

E adicionar o stub logo depois de `empacotar`:

```python
def achar_edge():
    return None


def prints(html, pasta, estados, largura=1366, altura=900):
    raise NotImplementedError
```

- [ ] **Step 2: Rodar e ver o stub ser detectado**

Run: `uv run ferramentas/mockup.py --autoteste`
Expected: `autoteste empacotar: ok` e `autoteste prints: PULADO (Edge nao encontrado)` — o stub retorna None. Isso confirma o caminho de "Edge ausente"; o proximo passo implementa e o teste passa a rodar de verdade.

- [ ] **Step 3: Implementar `achar_edge` e `prints`**

Adicionar `import shutil` e `import subprocess` aos imports e substituir os stubs por:

```python
EDGES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]


def achar_edge():
    for c in [shutil.which("msedge"), *EDGES]:
        if c and Path(c).is_file():
            return str(c)
    return None


def prints(html, pasta, estados, largura=1366, altura=900):
    edge = achar_edge()
    if not edge:
        sys.exit(
            "Edge nao encontrado. O HTML esta pronto; para gerar os PNGs depois rode:\n"
            f"  uv run ferramentas/mockup.py prints {html} {pasta} {' '.join(estados)}"
        )
    html = Path(html).resolve()
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    copia = html.with_name(f".print-{html.name}")
    copia.write_text(
        html.read_text(encoding="utf-8") + "\n<style>.mk-revisao{display:none!important}</style>\n",
        encoding="utf-8",
    )
    gerados = []
    try:
        for n, estado in enumerate(estados, 1):
            png = (pasta / f"{n:02d}-{estado}.png").resolve()
            png.unlink(missing_ok=True)
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as perfil:
                subprocess.run(
                    [edge, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                     f"--user-data-dir={perfil}", f"--window-size={largura},{altura}",
                     f"--screenshot={png}", f"{copia.as_uri()}#{estado}"],
                    capture_output=True, timeout=90,
                )
            if not png.is_file():
                sys.exit(f"Edge nao gerou {png}")
            gerados.append(png)
    finally:
        copia.unlink(missing_ok=True)
    return gerados
```

E no `main()`, registrar o subcomando (depois do parser `empacotar`):

```python
    p = sub.add_parser("prints")
    p.add_argument("html", type=Path)
    p.add_argument("pasta", type=Path)
    p.add_argument("estados", nargs="+")
    p.add_argument("--largura", type=int, default=1366)
    p.add_argument("--altura", type=int, default=900)
```

e o ramo:

```python
    elif a.cmd == "prints":
        for png in prints(a.html, a.pasta, a.estados, a.largura, a.altura):
            print(f"gerado: {png}")
```

- [ ] **Step 4: Rodar o autoteste completo**

Run: `uv run ferramentas/mockup.py --autoteste`
Expected:
```
autoteste empacotar: ok
autoteste prints: ok
```
Se `prints` falhar com "estados geraram o mesmo print", o Edge ignorou a ancora no `file://`: trocar o seletor `:target` por um script de uma linha no modelo (`document.body.dataset.estado=location.hash.slice(1)`) e CSS `[data-estado=a] #a{display:block}` — e ajustar `mockup-base.css` da Task 3 igual. Registrar a decisao no commit.

- [ ] **Step 5: Liberar o comando no settings e commitar**

Em `.claude/settings.json`, na lista `permissions.allow`, logo apos `"Bash(uv run ferramentas/db.py:*)",` adicionar:

```json
      "Bash(uv run ferramentas/mockup.py:*)",
```

```bash
git add ferramentas/mockup.py .claude/settings.json
git commit -m "Adiciona mockup.py prints: PNG por estado via Edge headless"
```

---

### Task 3: CSS base e esqueleto do rascunho

**Files:**
- Create: `.claude/skills/mockup-telas/modelos/mockup-base.css`
- Create: `.claude/skills/mockup-telas/modelos/rascunho.html`

**Interfaces:**
- Produces (convencoes usadas pelo SKILL.md e pelo `prints`):
  - Estado: `<section class="estado" id="<estado>">`; sem ancora, mostra o primeiro estado.
  - Revisao (somem nos prints): qualquer elemento com classe `mk-revisao`.
  - Marcacoes: `mk-novo`, `mk-alterado`, `mk-removido` + atributo `data-mk="<texto curto>"`; `<body class="mk-sem-marcas">` desliga.
  - Barra de revisao: `<nav class="mk-revisao mk-barra">` com links `#<estado>` e botao que alterna `mk-sem-marcas`.

- [ ] **Step 1: Criar `mockup-base.css`**

```css
/* Base dos mockups da skill mockup-telas. Copiado para contexto/telas/<projeto>/kit/ no levantamento. */

/* Estados: um <section class="estado" id="..."> por estado; #ancora escolhe; sem ancora mostra o primeiro. */
.estado { display: none; }
.estado:target { display: block; }
body:not(:has(.estado:target)) .estado:first-of-type { display: block; }

/* Marcacoes de alteracao (data-mk = texto da etiqueta). */
.mk-novo, .mk-alterado, .mk-removido { position: relative; outline: 2px dashed; outline-offset: 2px; }
.mk-novo { outline-color: #2e7d32; }
.mk-alterado { outline-color: #ef6c00; }
.mk-removido { outline-color: #c62828; opacity: .55; text-decoration: line-through; }
.mk-novo::after, .mk-alterado::after, .mk-removido::after {
  content: attr(data-mk); position: absolute; top: -10px; right: -4px; z-index: 9999;
  font: 600 10px/1.4 system-ui, sans-serif; color: #fff; padding: 0 5px; border-radius: 3px;
  text-decoration: none; white-space: nowrap;
}
.mk-novo::after { background: #2e7d32; }
.mk-alterado::after { background: #ef6c00; }
.mk-removido::after { background: #c62828; }
.mk-sem-marcas .mk-novo, .mk-sem-marcas .mk-alterado { outline: none; }
.mk-sem-marcas .mk-novo::after, .mk-sem-marcas .mk-alterado::after, .mk-sem-marcas .mk-removido::after { display: none; }
.mk-sem-marcas .mk-removido { display: none; }

/* Barra de revisao (escondida nos prints). */
.mk-barra {
  position: fixed; right: 12px; bottom: 12px; z-index: 10000; display: flex; flex-wrap: wrap; gap: 6px;
  max-width: 60vw; padding: 6px 8px; background: #263238; border-radius: 6px;
  font: 12px/1.4 system-ui, sans-serif; box-shadow: 0 2px 8px #0005;
}
.mk-barra a, .mk-barra button {
  color: #fff; background: #455a64; border: 0; border-radius: 4px; padding: 2px 8px;
  text-decoration: none; cursor: pointer; font: inherit;
}
```

- [ ] **Step 2: Criar `rascunho.html`**

```html
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>[TITULO DA TELA] — mockup vN</title>
<!-- Caminho relativo de saidas/mockups/<tema>/ ate o kit do projeto -->
<link rel="stylesheet" href="../../../contexto/telas/[PROJETO]/kit/kit.css">
<link rel="stylesheet" href="../../../contexto/telas/[PROJETO]/kit/mockup-base.css">
</head>
<body>
<!-- Copie o layout-base (menu, cabecalho) de kit/componentes.html e coloque os estados dentro da area de conteudo. -->

<section class="estado" id="listagem">
  <!-- estado 1 -->
</section>

<section class="estado" id="edicao">
  <!-- estado 2; marque mudancas assim: <div class="mk-novo" data-mk="novo">...</div> -->
</section>

<nav class="mk-revisao mk-barra">
  <a href="#listagem">listagem</a>
  <a href="#edicao">edicao</a>
  <button onclick="document.body.classList.toggle('mk-sem-marcas')">marcacoes</button>
</nav>
</body>
</html>
```

- [ ] **Step 3: Conferir as convencoes com o `mockup.py`**

Criar em `saidas/teste-base/` uma copia do `rascunho.html` com os `href` apontando para `../../.claude/skills/mockup-telas/modelos/mockup-base.css` (sem o kit.css), um `<div class="mk-novo" data-mk="novo">X</div>` no estado `edicao`, e rodar:

```bash
uv run ferramentas/mockup.py empacotar saidas/teste-base/v1.html saidas/teste-base/entrega/mockup.html
uv run ferramentas/mockup.py prints saidas/teste-base/entrega/mockup.html saidas/teste-base/entrega/telas listagem edicao
```

Expected: `gravado: ...` (sem AVISO), `gerado: ...01-listagem.png`, `gerado: ...02-edicao.png`. Abrir `02-edicao.png` (Read) e conferir: etiqueta verde "novo" visivel e **sem** a barra de revisao. Apagar `saidas/teste-base/`.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/mockup-telas/modelos/mockup-base.css .claude/skills/mockup-telas/modelos/rascunho.html
git commit -m "Adiciona CSS base e esqueleto de rascunho da skill mockup-telas"
```

---

### Task 4: Modelos de documento (PADROES, CATALOGO, NOTAS, especificacao)

**Files:**
- Create: `.claude/skills/mockup-telas/modelos/PADROES.md`
- Create: `.claude/skills/mockup-telas/modelos/CATALOGO.md`
- Create: `.claude/skills/mockup-telas/modelos/NOTAS.md`
- Create: `.claude/skills/mockup-telas/modelos/especificacao.md`

**Interfaces:**
- Produces: campos que o SKILL.md (Task 5) manda preencher — em especial `PADROES.md` → `Commit analisado`, `Pastas de tela e estilo` (usadas na verificacao de desatualizacao) e `Fonte do CSS`.

- [ ] **Step 1: Criar `PADROES.md`**

```markdown
# Padroes de tela — <projeto>

- **Commit analisado:** <hash> (<branch>) em AAAA-MM-DD
- **Pastas de tela e estilo:** <ex.: src/app/components src/app/shared src/styles.css> (usadas para detectar mudancas)
- **Stack:** <framework e versao> · **Biblioteca de UI:** <ex.: Angular Material 8.2.3, tema indigo-pink>
- **Fonte do CSS do kit:** <sistema rodando (URL) | repositorio | pacote publicado (URL do CDN) | reconstrucao por tokens>
- **Fidelidade:** <alta | media — motivo>
- **Prints de referencia:** <kit/assets/ref-*.png ou "sem acesso ao sistema">

## Layout-base
<menu lateral/superior, cabecalho, rodape, area de conteudo, breadcrumb; arquivo-fonte do layout>

## Componentes recorrentes
| Componente | Onde aparece (exemplo) | Como e no codigo | Peca no kit (`componentes.html#id`) |
|---|---|---|---|

## Formularios
<disposicao (colunas), rotulos, obrigatorio (*), mascaras (CPF, data, area), mensagens de validacao>

## Listagens e filtros
<grid/tabela, paginacao, acoes por linha, filtros, ordenacao, "nenhum registro">

## Botoes e acoes
<ordem e cores (primario/secundario/perigo), icones, confirmacoes>

## Mensagens
<sucesso, erro, alerta: componente e textos padrao que aparecem no sistema>

## Vocabulario da interface
<termos usados nas telas: ex. "Inventario", "Projeto", "Salvar", "Voltar">

## Observacoes
<regras e armadilhas>
```

- [ ] **Step 2: Criar `CATALOGO.md`**

```markdown
# Catalogo de telas — <projeto>

> Gerado pela skill mockup-telas no commit <hash>. Uma linha por tela (rota).

| Tela | Menu / caminho | Rota | Arquivo-fonte | Observacoes |
|---|---|---|---|---|
| <nome que o usuario ve> | <Menu > Submenu> | </rota/:id> | <src/app/.../x.component.html> | <perfil, estados, abas> |
```

- [ ] **Step 3: Criar `NOTAS.md`**

```markdown
# <tema> — notas do mockup

- **Projeto:** <projeto> · **Tipo:** <tela nova | alteracao>
- **Tela base / alterada:** <nome> — `<arquivo-fonte>` (<rota>)
- **Pedido original:** <texto do analista>
- **Destino do pacote:** <saidas/mockups/<tema>/entrega | pasta informada por quem chamou>

## Decisoes
- <pergunta → resposta do analista>

## Versoes
### v1 — AAAA-MM-DD
- <o que foi feito>

## Estados
| Ancora | O que mostra |
|---|---|
```

- [ ] **Step 4: Criar `especificacao.md`**

```markdown
# <Titulo da tela> — especificacao do mockup

- **Projeto:** <projeto> · **Tipo:** <tela nova | alteracao de tela existente>
- **Tela:** <Menu > caminho> (<rota>) — base: `<arquivo-fonte>`
- **Data:** AAAA-MM-DD · **Mockup:** `mockup.html`

## 1. Resumo da demanda
<uma ou duas frases>

## 2. O que muda (somente alteracao)
| Item | Mudanca | Detalhe |
|---|---|---|
| <campo/botao/coluna> | novo / alterado / removido | <...> |

## 3. Estados da tela
| # | Estado | Imagem | Descricao |
|---|---|---|---|
| 1 | <listagem> | `telas/01-listagem.png` | <...> |

## 4. Campos
| Rotulo | Tipo | Tamanho | Obrig. | Mascara | Padrao | Origem do dado |
|---|---|---|---|---|---|---|

## 5. Validacoes e mensagens
| Regra | Quando | Mensagem (texto exato) |
|---|---|---|

## 6. Acoes
| Botao/acao | Comportamento |
|---|---|

## 7. Perfis e permissoes
<quem ve, quem edita>

## 8. Pontos em aberto
- <...>
```

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/mockup-telas/modelos/*.md
git commit -m "Adiciona modelos de documento da skill mockup-telas"
```

---

### Task 5: `SKILL.md` — o roteiro

**Files:**
- Create: `.claude/skills/mockup-telas/SKILL.md`

**Interfaces:**
- Consumes: `ferramentas/mockup.py empacotar|prints` (Tasks 1-2); convencoes de `mockup-base.css` (Task 3); modelos (Task 4).

- [ ] **Step 1: Criar o arquivo**

````markdown
---
name: mockup-telas
description: Gera mockups fieis as telas de um sistema ja existente em .projetos/ (tela nova ou alteracao de tela), itera ajustes com o analista e entrega um pacote com mockup.html autocontido, PNG por estado e especificacao.md. Use quando o analista pedir para levantar/avaliar o padrao de telas de um sistema, criar mockup/prototipo/tela nova, alterar uma tela existente num mockup, ajustar um mockup ou finalizar/aprovar um mockup.
---

# Mockup de telas

Voce ajuda um analista a produzir mockups fieis ao sistema do cliente. Linguagem simples, **uma pergunta
por vez**. A skill so **produz** o pacote; quem decide o destino (OS, e-mail, Redmine, SVN) e o analista
ou o fluxo que chamou a skill.

## Regras (sempre)
- `.projetos/` e **somente leitura**: nunca edite, nunca crie branch ou commit la.
- Login em sistema: o analista faz no navegador. Nunca peca, digite ou guarde senha.
- Dados ficticios. Dado real so via `uv run ferramentas/db.py`, com CPF/nome/endereco mascarados.
- Nao faca `svn add`/commit, nao envie e-mail, nao crie atividade.
- Modelos desta skill: `.claude/skills/mockup-telas/modelos/`.

## Qual modo?
| Pedido do analista | Modo |
|---|---|
| "levantar / avaliar / mapear as telas do <projeto>" | 1. Levantar |
| "tela nova", "mockup de uma tela para ..." | 2. Nova |
| "alterar a tela X", "incluir campo Y na tela Z" | 3. Alterar |
| pedido de mudanca num mockup em andamento | 4. Ajustar |
| "aprovado", "pode finalizar", "gerar o pacote" | 5. Finalizar |

Em andamento = existe `saidas/mockups/*/NOTAS.md` recente; na duvida, pergunte qual.

## Antes de Nova/Alterar: o levantamento existe e esta em dia?
1. Sem `contexto/telas/<projeto>/PADROES.md` → explique e sugira o modo Levantar.
2. Leia `Commit analisado` e `Pastas de tela e estilo` do PADROES.md e rode
   `git -C .projetos/<projeto> diff --stat <hash> HEAD -- <pastas>`. Saida nao vazia → avise
   ("o sistema mudou nestes arquivos desde o levantamento") e ofereca atualizar; o analista pode seguir.

## 1. Levantar
1. Leia a ficha do projeto em `contexto/PROJETOS.md` e o README/CLAUDE.md do projeto.
2. Detecte stack e biblioteca de UI (`package.json`, `angular.json`, `vite.config.*`...).
3. Rotas e menus → `contexto/telas/<projeto>/CATALOGO.md` (modelo `CATALOGO.md`). Use rotas e
   componentes de menu; o nome da tela e o que o usuario ve (titulo/breadcrumb), nao o nome da classe.
4. Padroes → `contexto/telas/<projeto>/PADROES.md` (modelo `PADROES.md`). Leia ao menos: layout-base,
   uma listagem, um formulario de cadastro, um modal/dialogo e o CSS global.
5. Pergunte: "Voce tem acesso ao sistema rodando (homologacao)? Se sim, me passe a URL; voce faz o
   login no navegador." Monte `kit/kit.css` pela primeira fonte que funcionar e registre qual foi:
   1. **Sistema rodando:** abra a URL no navegador embutido, espere o analista logar, extraia o CSS
      compilado (`[...document.styleSheets].map(s=>[...s.cssRules].map(r=>r.cssText).join('\n'))`
      via javascript_tool; folhas externas: baixe pelo href). Tire prints de 3-5 telas do catalogo e
      salve em `kit/assets/ref-<tela>.png`.
   2. **Repositorio:** CSS/SCSS global e temas do proprio projeto (SCSS: copie so o que for CSS valido
      ou converta variaveis em valores).
   3. **Pacote publicado:** tema em `node_modules` (ausente no clone) → versao exata em
      `package-lock.json` (ou `package.json`) e baixe de `https://cdn.jsdelivr.net/npm/<pacote>@<versao>/<caminho>`
      (ex.: `@angular/material@8.2.3/prebuilt-themes/indigo-pink.css`). Fontes e icones da mesma forma
      para `kit/assets/`.
   4. **Tokens:** cores, fontes e espacamentos lidos no codigo → CSS escrito por voce. Avise que a
      fidelidade e menor.
   Concatene em `kit.css`: tema → estilos globais do projeto → estilos proprios dos componentes usados.
6. Copie `modelos/mockup-base.css` para `kit/mockup-base.css`. Escreva `kit/componentes.html`: cada peca
   recorrente (layout com menu e cabecalho, listagem com filtros e paginacao, formulario, modal, botoes,
   mensagens) num `<section id="...">`, com o **mesmo HTML/classes que o framework gera no navegador**
   (ex.: Angular Material renderiza `mat-form-field` como `div.mat-form-field...`; reproduza o HTML
   renderizado, nao o template). Escreva `kit/amostra.html` mostrando todas as pecas, com links para
   `kit.css` e `mockup-base.css`.
7. Abra a amostra para o analista (navegador embutido, `file:///...`) e pergunte: "Parece o sistema?
   O que esta diferente?" Corrija ate ele confirmar. **Sem confirmacao o levantamento nao termina.**
8. Grave no PADROES.md o commit (`git -C .projetos/<projeto> rev-parse --short HEAD`) e a data, e
   acrescente na ficha do projeto em `contexto/PROJETOS.md`:
   `- **Mockups:** contexto/telas/<projeto>/ (levantado no commit <hash>, AAAA-MM-DD)`.

## 2. Nova
1. Pergunte, uma por vez, o que faltar: objetivo, onde fica no menu, campos, acoes, perfis.
2. Escolha no CATALOGO a tela existente mais parecida como base; diga qual e por que.
3. Crie `saidas/mockups/AAAA-MM-DD-<tema>/` com `NOTAS.md` (modelo) e `v1.html` a partir de
   `modelos/rascunho.html` + pecas de `kit/componentes.html`. Um `<section class="estado">` por estado
   (lista, edicao, modal, erro de validacao, vazio...) e a barra `mk-revisao` com um link por estado.
4. Abra `v1.html` para o analista e pergunte o que ajustar.

## 3. Alterar
1. Localize a tela: CATALOGO (nome, menu, rota) e busca no codigo pelo texto que aparece na tela.
2. **Confirme antes de seguir**: "E esta? <Menu > caminho>, rota <rota>, arquivo `<arquivo>`" + print
   de referencia, se houver. Varias candidatas → ate 3; nunca escolha sozinho.
3. Gere `atual.html` (como a tela e hoje, lida do template e do kit) e `v1.html` com a mudanca, marcando
   cada diferenca com `class="mk-novo|mk-alterado|mk-removido" data-mk="<texto curto>"`.
4. Registre no NOTAS.md e abra os dois para o analista comparar.

## 4. Ajustar
Copie o ultimo `vN.html` para `vN+1.html`, aplique o pedido, registre em `NOTAS.md > Versoes` o que mudou
e por que, e mostre. Nunca sobrescreva versoes anteriores.

## 5. Finalizar
1. Confirme a versao aprovada e se a entrega vai **com ou sem** marcacoes (padrao: sem).
2. Prepare `vFINAL.html` = versao aprovada com `<body class="mk-sem-marcas">` (ou sem a classe, se pediram
   marcacoes).
3. Destino: `saidas/mockups/<tema>/entrega/` ou a pasta informada por quem chamou a skill.
4. Rode:
   ```bash
   uv run ferramentas/mockup.py empacotar saidas/mockups/<tema>/vFINAL.html <destino>/mockup.html
   uv run ferramentas/mockup.py prints <destino>/mockup.html <destino>/telas <estado1> <estado2> ...
   ```
   (estados na ordem da barra de revisao). `AVISO` de referencia nao encontrada → corrija e rode de novo.
5. Abra 1-2 PNGs (Read) e confira que estao certos e sem a barra de revisao.
6. Escreva `<destino>/especificacao.md`: use `contexto/telas/<projeto>/especificacao.*` se existir,
   senao `modelos/especificacao.md`. Fonte: NOTAS.md + mockup aprovado; textos de mensagens exatos;
   origem dos dados com `contexto/BANCOS.md` quando souber.
7. Liste os arquivos do pacote com o caminho completo. Nao envie nem copie para outro lugar.
````

- [ ] **Step 2: Conferir referencias cruzadas**

Run (na raiz do seed):
```bash
grep -o 'modelos/[A-Za-z.-]*' .claude/skills/mockup-telas/SKILL.md | sort -u | while read f; do test -f ".claude/skills/mockup-telas/$f" && echo "ok $f" || echo "FALTA $f"; done
```
Expected: so linhas `ok` (`modelos/CATALOGO.md`, `modelos/NOTAS.md`... `modelos/mockup-base.css`, `modelos/rascunho.html`, `modelos/especificacao.md`).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/mockup-telas/SKILL.md
git commit -m "Adiciona skill mockup-telas: roteiro de levantamento, mockup e pacote"
```

---

### Task 6: Documentacao do seed

**Files:**
- Modify: `contexto/SKILLS.md` (tabela)
- Modify: `CLAUDE.md` (tabela "Estrutura")
- Modify: `contexto/PROJETOS.md` (modelo da ficha)

- [ ] **Step 1: `contexto/SKILLS.md`** — acrescentar no fim da tabela:

```markdown
| **mockup-telas** | Levanta o padrao de telas de um sistema em `.projetos/` e gera mockups fieis (tela nova ou alteracao), com pacote HTML + PNG + especificacao | Ja vem no repositorio (`.claude/skills/mockup-telas/`) |
```

- [ ] **Step 2: `CLAUDE.md`** — na tabela "Estrutura", depois da linha de `ferramentas/db.py`:

```markdown
| `ferramentas/mockup.py` | Empacota mockup autocontido e gera PNGs (skill mockup-telas) | Sim |
| `contexto/telas/<projeto>/` | Padroes, catalogo e kit visual de cada sistema — **mantidos pela skill mockup-telas** | Sim |
```

- [ ] **Step 3: `contexto/PROJETOS.md`** — no bloco MODELO, antes de `- **Atualizado em:** AAAA-MM-DD`:

```markdown
- **Mockups:** <contexto/telas/<nome>/ (levantado no commit <hash>, AAAA-MM-DD) ou "nao levantado">
```

- [ ] **Step 4: Commit**

```bash
git add contexto/SKILLS.md CLAUDE.md contexto/PROJETOS.md
git commit -m "Documenta a skill mockup-telas no seed"
```

---

### Task 7: Validacao ponta a ponta no `analistas-sugf`

**Files:** nenhum no seed (salvo correcoes que a validacao revelar). Gera `contexto/telas/inventario-florestal-web/` no `analistas-sugf` e `saidas/mockups/...` la.

**Pre-requisito (pedir OK ao analista):** levar o seed para o repo da equipe:
```bash
git -C D:/Projetos_Claude/para_analistas push origin main
git -C D:/Projetos_Claude/analistas-sugf pull seed main
```

- [ ] **Step 1: Levantar** — numa sessao aberta em `D:/Projetos_Claude/analistas-sugf`: "levantar as telas do inventario-florestal-web".
Conferir: `CATALOGO.md` lista as rotas de `src/app/components/inventario` com arquivo-fonte correto; `PADROES.md` registra fonte do CSS = pacote publicado (`@angular/material@8.2.3`) ou sistema rodando; `amostra.html` aprovada pelo analista.

- [ ] **Step 2: Nova tela** — pedido real ou de exemplo do analista; conferir que a skill escolheu tela base e gerou `v1.html` com estados navegaveis.

- [ ] **Step 3: Alterar tela** — ex.: "incluir um campo na tela de cadastro de inventario"; conferir que pediu confirmacao da tela, gerou `atual.html` e `v1.html` com marcacoes.

- [ ] **Step 4: Dois ajustes** — conferir `v2.html`, `v3.html` e o NOTAS.md com as versoes.

- [ ] **Step 5: Finalizar** — conferir o contrato:
```bash
ls saidas/mockups/*/entrega saidas/mockups/*/entrega/telas
cp saidas/mockups/<tema>/entrega/mockup.html "$TEMP/mockup-isolado.html"
```
Abrir `$TEMP/mockup-isolado.html` no navegador: tem que renderizar igual (prova de autocontido). PNGs um por estado; `especificacao.md` cobre o NOTAS.md.

- [ ] **Step 6: Corrigir o que a validacao revelar** no seed (SKILL.md/modelos/script), rodar `uv run ferramentas/mockup.py --autoteste` de novo, commitar no seed com mensagem descrevendo a correcao, e commitar no `analistas-sugf` o `contexto/telas/inventario-florestal-web/` (com OK do analista).
