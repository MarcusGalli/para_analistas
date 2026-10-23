# /// script
# requires-python = ">=3.11"
# dependencies = ["oracledb"]
# ///
"""Consulta SOMENTE LEITURA nos bancos cadastrados em .secrets/bancos.toml.

  uv run ferramentas/db.py --listar
  uv run ferramentas/db.py <apelido> "SELECT ..."
  uv run ferramentas/db.py <apelido> -f consulta.sql [-p ano=2026] [--max 50] [--csv saidas/x.csv]
  uv run ferramentas/db.py --autoteste

So aceita SELECT/WITH, roda em transacao READ ONLY e nunca faz commit.
Scripts de alteracao (UPDATE/DDL) sao gerados pelo Claude e executados pelo analista na ferramenta dele.
"""
import argparse
import csv
import re
import sys
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SEGREDOS = RAIZ / ".secrets" / "bancos.toml"


def carregar():
    if not SEGREDOS.exists():
        sys.exit(f"{SEGREDOS} nao existe. Copie de .secrets/bancos.toml.exemplo e preencha.")
    with open(SEGREDOS, "rb") as f:
        return tomllib.load(f)


def comandos(sql):
    """Separa por ';' e bloqueia qualquer comando que nao seja SELECT/WITH."""
    # ponytail: ';' dentro de string literal quebra o split; trocar por parser SQL se isso acontecer
    saida = []
    for c in sql.split(";"):
        limpo = re.sub(r"--[^\n]*", " ", re.sub(r"/\*.*?\*/", " ", c, flags=re.S)).strip()
        if not limpo:
            continue
        if not re.match(r"(select|with)\b", limpo, re.I):
            sys.exit(f"Bloqueado (somente leitura): {limpo[:80]}")
        saida.append(c.strip())
    return saida


def conectar(cfg, apelido):
    banco = cfg.get("bancos", {}).get(apelido)
    if not banco:
        sys.exit(f"Apelido '{apelido}' nao existe em bancos.toml. Use --listar.")
    # ponytail: so Oracle (banco do cliente); outro tipo = um elif com o driver dele
    if banco.get("tipo", "oracle") != "oracle":
        sys.exit(f"Tipo '{banco['tipo']}' ainda nao suportado por db.py.")
    import oracledb
    oracledb.defaults.fetch_lobs = False  # CLOB -> str
    lib = cfg.get("oracle", {}).get("instant_client")
    if lib and oracledb.is_thin_mode():
        oracledb.init_oracle_client(lib_dir=lib)
    conn = oracledb.connect(user=banco["usuario"], password=banco["senha"], dsn=banco["dsn"])
    conn.cursor().execute("SET TRANSACTION READ ONLY")
    return conn


def celula(v, n=60):
    s = "" if v is None else " ".join(str(v).split())
    return (s[:n] + "...") if len(s) > n else s


def executar(conn, cmd, params, maximo, arq_csv):
    cur = conn.cursor()
    usados = {k: v for k, v in params.items() if re.search(rf":{k}\b", cmd, re.I)}
    cur.execute(cmd, usados)
    cols = [d[0] for d in cur.description]
    if arq_csv:
        linhas = cur.fetchall()
        Path(arq_csv).parent.mkdir(parents=True, exist_ok=True)
        with open(arq_csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(cols)
            w.writerows(linhas)
        print(f"{len(linhas)} linhas gravadas em {arq_csv}")
        linhas = linhas[:maximo]
        mais = False
    else:
        linhas = cur.fetchmany(maximo + 1)
        mais = len(linhas) > maximo
        linhas = linhas[:maximo]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in linhas:
        print("| " + " | ".join(celula(v).replace("|", "/") for v in r) + " |")
    print(f"\n{len(linhas)} linha(s)" + (f" — ha mais; use --max ou --csv" if mais else ""))


def autoteste():
    assert comandos("select 1 from dual; -- fim") == ["select 1 from dual"]
    assert comandos("/* x */ WITH a AS (select 1 from dual) select * from a;") != []
    assert len(comandos("select 1 from dual;\nselect 2 from dual;")) == 2
    for perigoso in ["update t set x=1", "select 1 from dual; delete from t", "drop table t", "begin null; end"]:
        try:
            comandos(perigoso)
            raise AssertionError(f"deveria bloquear: {perigoso}")
        except SystemExit:
            pass
    print("autoteste ok")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("apelido", nargs="?")
    ap.add_argument("sql", nargs="?")
    ap.add_argument("-f", "--arquivo", help="arquivo .sql (um ou mais SELECT separados por ;)")
    ap.add_argument("-p", "--param", action="append", default=[], help="bind :nome -> nome=valor")
    ap.add_argument("--max", type=int, default=100, help="linhas exibidas (padrao 100)")
    ap.add_argument("--csv", help="grava TODAS as linhas neste CSV (use a pasta saidas/)")
    ap.add_argument("--listar", action="store_true", help="lista apelidos cadastrados")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()

    if a.autoteste:
        return autoteste()
    cfg = carregar()
    if a.listar:
        for nome, b in cfg.get("bancos", {}).items():
            print(f"{nome:25} {b.get('tipo', 'oracle'):8} {b.get('usuario', ''):25} {b.get('dsn', '')}")
        return
    if not a.apelido or not (a.sql or a.arquivo):
        ap.error("informe <apelido> e o SQL (texto ou -f arquivo)")

    sql = Path(a.arquivo).read_text(encoding="utf-8") if a.arquivo else a.sql
    params = dict(p.split("=", 1) for p in a.param)
    cmds = comandos(sql)
    conn = conectar(cfg, a.apelido)
    try:
        for i, cmd in enumerate(cmds, 1):
            if len(cmds) > 1:
                print(f"\n### Consulta {i}/{len(cmds)}")
            csv_i = a.csv if len(cmds) == 1 or not a.csv else re.sub(r"(\.csv)?$", f"_{i}.csv", a.csv, count=1)
            executar(conn, cmd, params, a.max, csv_i)
    finally:
        conn.rollback()
        conn.close()


if __name__ == "__main__":
    main()
