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
import shutil
import subprocess
import time
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


def externo(ref):
    return ref.startswith(("http:", "https:", "data:", "//", "#", "mailto:"))


def remoto(ref, externos):
    if externos is not None and ref.startswith(("http:", "https:", "//")):
        externos.append(ref)
    return True


def limpo(ref):
    return ref.split("?")[0].split("#")[0]


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho.name)[0]
    if not tipo and caminho.suffix.lower() == ".woff2":
        tipo = "font/woff2"
    tipo = tipo or "application/octet-stream"
    return f"data:{tipo};base64,{base64.b64encode(caminho.read_bytes()).decode()}"


def embutir_css(css, base, faltando, raiz, externos=None, vistos=None):
    """Embute @import e url() locais; `base` e a pasta do arquivo CSS."""
    vistos = vistos or set()

    def troca_import(m):
        ref = m.group(1)
        alvo = (base / limpo(ref)).resolve()
        if externo(ref) and remoto(ref, externos):
            return m.group(0)
        if not alvo.is_file() or alvo in vistos:
            faltando.append(rel(alvo, raiz))
            return m.group(0)
        texto = alvo.read_text(encoding="utf-8", errors="replace")
        return embutir_css(texto, alvo.parent, faltando, raiz, externos, vistos | {alvo})

    def troca_url(m):
        ref = m.group(2).strip()
        if externo(ref) and remoto(ref, externos):
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


def empacotar(origem, destino, externos=None):
    """Devolve as referencias locais faltando; se `externos` for uma lista, recebe as http(s)/// nao embutidas."""
    origem = Path(origem).resolve()
    base = origem.parent
    html = origem.read_text(encoding="utf-8")
    faltando = []

    def troca_link(m):
        href = HREF.search(m.group(0))
        if not href or (externo(href.group(1)) and remoto(href.group(1), externos)):
            return m.group(0)
        alvo = (base / limpo(href.group(1))).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, base))
            return m.group(0)
        css = embutir_css(alvo.read_text(encoding="utf-8", errors="replace"), alvo.parent, faltando, base, externos)
        return f"<style>\n{css}\n</style>"

    def troca_style(m):
        return m.group(1) + embutir_css(m.group(2), base, faltando, base, externos) + m.group(3)

    def troca_script(m):
        ref = m.group(3)
        if externo(ref) and remoto(ref, externos):
            return m.group(0)
        alvo = (base / limpo(ref)).resolve()
        if not alvo.is_file():
            faltando.append(rel(alvo, base))
            return m.group(0)
        js = alvo.read_text(encoding="utf-8", errors="replace").replace("</script", "<\\/script")
        return f"<script{m.group(1)}{m.group(4)}>{js}</script>"

    def troca_src(m):
        ref = m.group(3)
        if externo(ref) and remoto(ref, externos):
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
        externos = []
        faltando = empacotar(raiz / "v1.html", saida, externos)
        html = saida.read_text(encoding="utf-8")
        assert faltando == ["kit/assets/sumiu.png"], faltando
        assert externos == ["https://exemplo.com/fundo.png"], externos
        assert "<link" not in html, "link de CSS nao foi embutido"
        assert "#123456" in html, "@import nao foi embutido"
        assert "data:font/woff2;base64," in html or "data:application/octet-stream;base64," in html, "fonte nao embutida"
        assert html.count("data:image/png;base64,") == 2, "imagens (img e url no <style>) nao embutidas"
        assert "window.ok=1;" in html and 'src="kit/app.js"' not in html, "script nao embutido"
        assert "https://exemplo.com/fundo.png" in html, "url externa deveria ficar como esta"
        assert 'href="#edicao"' in html, "ancora deveria ficar como esta"
    print("autoteste empacotar: ok")
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
        try:
            prints(pagina, raiz / "telas", ["a", "naoexiste"], 400, 300)
            raise AssertionError("estado inexistente deveria sair com SystemExit")
        except SystemExit as e:
            assert "naoexiste" in str(e), e
    print("autoteste prints: ok")


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
    texto = html.read_text(encoding="utf-8")
    sem = [e for e in estados if f'id="{e}"' not in texto and f"id='{e}'" not in texto]
    if sem:
        sys.exit(f"Estados nao encontrados em {html.name} (id=\"...\"): {', '.join(sem)}")
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    copia = html.with_name(f".print-{html.name}")
    copia.write_text(
        texto + "\n<style>.mk-revisao{display:none!important}</style>\n",
        encoding="utf-8",
    )
    gerados = []
    try:
        for n, estado in enumerate(estados, 1):
            png = (pasta / f"{n:02d}-{estado}.png").resolve()
            png.unlink(missing_ok=True)
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as perfil:
                subprocess.run(
                    [edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                     f"--user-data-dir={perfil}", f"--window-size={largura},{altura}",
                     f"--screenshot={png}", f"{copia.as_uri()}#{estado}"],
                    capture_output=True, timeout=90,
                )
                anterior = None
                for _ in range(50):  # o Edge pode sair antes de o PNG aparecer (ou ficar pela metade) no disco
                    atual = png.stat().st_size if png.is_file() else 0
                    if atual > 0 and atual == anterior:  # tamanho estavel em duas leituras seguidas
                        break
                    anterior = atual
                    time.sleep(0.2)
            if not png.is_file():
                sys.exit(f"Edge nao gerou {png}")
            gerados.append(png)
    finally:
        copia.unlink(missing_ok=True)
    return gerados


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--autoteste", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("empacotar")
    e.add_argument("origem", type=Path)
    e.add_argument("destino", type=Path)
    p = sub.add_parser("prints")
    p.add_argument("html", type=Path)
    p.add_argument("pasta", type=Path)
    p.add_argument("estados", nargs="+")
    p.add_argument("--largura", type=int, default=1366)
    p.add_argument("--altura", type=int, default=900)
    a = ap.parse_args()
    if a.autoteste:
        autoteste()
    elif a.cmd == "empacotar":
        externos = []
        faltando = empacotar(a.origem, a.destino, externos)
        print(f"gravado: {a.destino}")
        if externos:
            print("AVISO - referencias externas (nao embutidas):")
            for x in sorted(set(externos)):
                print(f"  {x}")
        if faltando:
            print("AVISO - referencias locais nao encontradas (ficaram como estao):")
            for f in faltando:
                print(f"  {f}")
            sys.exit(1)
    elif a.cmd == "prints":
        for png in prints(a.html, a.pasta, a.estados, a.largura, a.altura):
            print(f"gerado: {png}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
