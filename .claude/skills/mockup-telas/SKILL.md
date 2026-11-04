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
   - Os `<section class="estado">` devem ser irmaos diretos, sem outro `<section>` antes deles no mesmo pai (o primeiro estado aparece por `:first-of-type`).
   - Marcacao `mk-*` nao aparece em `input`/`img`: marque o elemento que envolve o campo.
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
