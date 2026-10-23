# .SVN/

Working copies (checkout) dos repositorios SVN do cliente, onde ficam as documentacoes.
**Conteudo ignorado pelo git** deste repositorio.

```bash
svn checkout <url-do-repositorio-svn> .SVN/<nome>
```

Entregaveis de OS (gerados pelo Claude ou por voce) sao salvos dentro da working copy e enviados
com `svn add` + `svn commit` — o Claude so faz commit depois que voce confirmar.
Relatorios de consulta e analises ficam em `saidas/`, nao no SVN.

Depois do checkout peca ao Claude: *"registre o SVN <nome> no contexto"* — ele preenche
[`contexto/SVN.md`](../contexto/SVN.md).
