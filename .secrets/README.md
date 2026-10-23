# .secrets/

Logins, senhas, tokens e qualquer dado sensivel. **Tudo aqui e ignorado pelo git**, exceto este
README e os arquivos `*.exemplo`.

| Arquivo | Para que serve |
|---|---|
| `bancos.toml` | Conexoes de banco usadas por `ferramentas/db.py`. Copie de `bancos.toml.exemplo`. |
| outros | Tokens (Redmine, APIs...) — um arquivo por servico, nome livre. |

```bash
cp .secrets/bancos.toml.exemplo .secrets/bancos.toml
```

Regras:
- O Claude **nao le** esta pasta (bloqueado em `.claude/settings.json`). Quem le `bancos.toml`
  e o script `ferramentas/db.py`, que nunca imprime a senha.
- Prefira usuarios de banco **somente leitura**.
- Nunca copie senhas para `.md`, SQL, scripts ou mensagens de commit.
