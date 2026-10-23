# .SVN/

Working copies (checkout) dos repositorios SVN do cliente, onde ficam as documentacoes.
**Conteudo ignorado pelo git** deste repositorio.

```bash
svn checkout <url-do-repositorio-svn> .SVN/<nome>
```

Documentos gerados (pelo Claude ou por voce) sao salvos dentro da working copy e enviados
com `svn add` + `svn commit` — o Claude so faz commit depois que voce confirmar.

Depois do checkout peca ao Claude: *"registre o SVN <nome> no contexto"* — ele preenche
[`contexto/SVN.md`](../contexto/SVN.md).
