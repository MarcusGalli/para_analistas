# Skill `mockup-telas` — design

**Data:** 2026-11-04 · **Status:** aguardando revisao do analista · **Escopo v1:** somente telas (relatorios e geracao de tarefas ficam para depois)

## Objetivo

Permitir que o analista gere mockups **fieis as telas de um sistema ja existente** (tela nova ou alteracao
de tela existente), itere sobre eles e, ao aprovar, receba um **pacote autocontido** (HTML + PNG +
especificacao) pronto para ser anexado a uma OS, e-mail, atividade no Redmine ou outro destino.

A skill e **produtora**: ela gera o pacote e nao decide para onde ele vai. O fluxo de OS (outra frente de
trabalho) consome o pacote e decide o destino.

## Decisoes

| Tema | Decisao |
|---|---|
| Stack alvo | Web SPA (Angular, React, Vue...), stack detectada pela skill; desktop fora da v1 |
| Fidelidade | **Kit visual** extraido do sistema + mockup em HTML estatico que usa o kit |
| Formato | HTML navegavel (estados por ancora) + PNG por estado |
| Especificacao | Modelo padrao em Markdown; o projeto pode ter modelo proprio do cliente |
| Sistema rodando | Opcional: com URL de homologacao e login feito pelo analista, completa com CSS compilado e prints |
| Alteracao | Muda **so o mockup**; a skill nunca altera `.projetos/` |
| Destino final | Pasta `entrega/` padrao, ou pasta informada por quem chama a skill; sem SVN/e-mail/Redmine |

## Estrutura de arquivos

**No seed** (`para_analistas`, chega a todo analista):

```
.claude/skills/mockup-telas/
  SKILL.md              roteiro unico; identifica o modo pelo pedido
  modelos/
    PADROES.md          modelo do guia visual do projeto
    CATALOGO.md         modelo do catalogo de telas
    especificacao.md    modelo padrao da especificacao
```

**Por projeto** (gerado no levantamento, versionado no repositorio da equipe, ex.: `analistas-sugf`):

```
contexto/telas/<projeto>/
  PADROES.md       stack, layout-base, componentes, regras de UI, fonte do CSS, commit analisado
  CATALOGO.md      tela | menu/caminho | rota | arquivo-fonte | observacoes
  kit/
    kit.css            CSS do sistema (tema + estilos proprios)
    componentes.html   pecas prontas: layout com menu/cabecalho, grid, formulario, filtros, modal, botoes, mensagens
    amostra.html       pagina de conferencia com todos os componentes
    assets/            logo, icones, fontes
  especificacao.*  opcional: modelo do cliente; substitui o padrao
```

A ficha do projeto em `contexto/PROJETOS.md` ganha a linha
`- **Mockups:** contexto/telas/<projeto>/ (levantado no commit <hash>, AAAA-MM-DD)`.

**Trabalho em andamento** (em `saidas/`, fora do git):

```
saidas/mockups/AAAA-MM-DD-<tema>/
  atual.html            so em alteracao: reproducao da tela como e hoje
  v1.html, v2.html...   rascunhos; usam ../../../contexto/telas/<projeto>/kit/
  NOTAS.md              pedido, projeto, tela base, decisoes e ajustes por versao (fonte da verdade)
  entrega/              o pacote final (contrato fixo abaixo)
```

### Contrato do pacote (`entrega/`)

Nomes sempre iguais, para que outro fluxo consuma sem precisar interpretar:

```
entrega/
  mockup.html              AUTOCONTIDO: CSS, icones, fontes e logo embutidos (base64); abre fora da pasta
  telas/NN-<estado>.png    um PNG por estado (01-listagem.png, 02-edicao.png, 03-modal-excluir.png...)
  especificacao.md         documento de apoio
```

`especificacao.md` (modelo padrao) traz:
1. Resumo da demanda (o pedido, em uma ou duas frases) e projeto/tela.
2. Tipo: tela nova ou alteracao; **em alteracao, lista do que muda em relacao a tela atual** (novo / alterado / removido).
3. Estados da tela, cada um com referencia ao PNG (`telas/NN-<estado>.png`).
4. Campos: rotulo, tipo, tamanho, obrigatorio, mascara, valor padrao, origem do dado (tabela.coluna quando conhecida via `contexto/BANCOS.md`).
5. Validacoes e mensagens (texto exato).
6. Acoes/botoes e o comportamento de cada um.
7. Perfis/permissoes.
8. Pontos em aberto.

Quando o projeto tem `contexto/telas/<projeto>/especificacao.*`, a skill segue esse modelo.

## Fluxos

### 1. Levantar — `levantar <projeto>`

1. Le a ficha em `contexto/PROJETOS.md` e o README/CLAUDE.md do projeto.
2. Detecta stack e biblioteca de UI (`package.json`, `angular.json` ou equivalente).
3. Mapeia as telas a partir das rotas e menus e gera `CATALOGO.md`.
4. Extrai padroes (layout-base, componentes recorrentes, formularios, grids, botoes, mensagens, mascaras,
   vocabulario da interface) para `PADROES.md`.
5. Monta o CSS do kit nesta ordem de preferencia, registrando no `PADROES.md` qual fonte foi usada:
   1. **Sistema rodando** (opcional): o analista informa a URL de homologacao e faz o login no navegador;
      a skill copia o CSS compilado da pagina e tira prints de 3-5 telas representativas.
   2. **Estilos do repositorio** (`src/styles.*`, estilos de componentes, temas proprios).
   3. **Pacote publicado na versao exata** quando o tema esta em `node_modules` (ausente no clone):
      arquivo do CDN publico com a versao do `package-lock.json`/`package.json`
      (ex.: `@angular/material@8.2.3/prebuilt-themes/indigo-pink.css`).
   4. **Reconstrucao por tokens** (cores, fontes, espacamentos) — fidelidade menor, avisada na amostra.
6. Gera `componentes.html` e `amostra.html`; o analista abre a amostra e confirma se "parece o sistema".
   Sem confirmacao, o levantamento nao e dado como concluido.
7. Grava no `PADROES.md` o commit analisado (`git rev-parse HEAD`) e a data; atualiza a ficha em `PROJETOS.md`.

**Verificacao no inicio de todo pedido (nova/alterar):** sem levantamento → sugere `levantar`. Commit atual
diferente do analisado **e** mudancas em arquivos de tela/estilo (`git diff --stat <hash> -- <pastas de tela e estilo>`)
→ avisa e oferece atualizar; o analista pode seguir assim mesmo.

### 2. Nova tela — `nova tela: <descricao>`

1. Pergunta o que faltar, **uma pergunta por vez**: objetivo, onde fica no menu, campos, acoes, perfis.
2. Escolhe no catalogo a tela existente **mais parecida** como base e informa qual.
3. Gera `v1.html` com o kit, com todos os estados navegaveis por ancora (`#listagem`, `#edicao`, `#modal-excluir`...),
   e cria `NOTAS.md`.

### 3. Alterar tela — `alterar <tela>: <descricao>`

1. Localiza a tela pelo catalogo e pelo codigo (nome, menu, rota, texto que aparece na tela).
2. **Confirma com o analista** antes de seguir: menu/caminho, rota, arquivo-fonte e o print (se houver acesso)
   ou a reproducao. Varias candidatas → mostra ate 3; nunca escolhe sozinha.
3. Gera `atual.html` (tela como e hoje) e `v1.html` (com a mudanca), com as alteracoes **marcadas**
   (contorno + etiqueta "novo" / "alterado" / "removido"), que podem ser ligadas e desligadas por um botao.

### 4. Ajustar — qualquer pedido de mudanca no rascunho

Gera `vN+1.html`, registra no `NOTAS.md` o que mudou e por que, e mostra o resultado. Versoes anteriores
sao mantidas para comparacao.

### 5. Finalizar — quando o analista disser "aprovado"

1. Gera `entrega/mockup.html` autocontido (sem marcacoes de revisao, a menos que o analista peca).
2. Gera os PNGs de cada estado com o Edge headless, que ja vem no Windows:
   `msedge --headless --disable-gpu --window-size=1366,768 --screenshot=<png> "file:///.../mockup.html#<estado>"`.
3. Escreve `especificacao.md` a partir do `NOTAS.md` e do mockup aprovado.
4. Lista os arquivos do pacote e o caminho onde foram gravados. Se quem chamou a skill informou uma pasta de
   destino, o pacote e gravado la em vez de `entrega/`.

## Regras e limites

- Somente leitura em `.projetos/`; nenhum commit/branch nos projetos.
- Login no sistema sempre feito pelo analista no navegador; a skill nunca pede, digita ou guarda senha.
- Dados nos mockups sao ficticios. Exemplo real, quando ajudar, vem do `db.py` e com dados pessoais mascarados.
- Nao faz `svn add`/commit, nao envia e-mail, nao cria atividade no Redmine.
- `NOTAS.md` e a fonte da verdade: a sessao pode cair ou outro analista assumir e continuar do ultimo `vN`.

## Tratamento de falhas

| Situacao | Comportamento |
|---|---|
| Stack nao reconhecida | Pergunta onde ficam telas e estilos; segue com reconstrucao por tokens |
| Tema fora do repo, sem CDN e sem homologacao | Reconstrucao por tokens; aviso no `PADROES.md` e na amostra |
| Tela nao encontrada / ambigua | Ate 3 candidatas com menu e rota; analista escolhe |
| Edge nao encontrado | Entrega so o HTML e informa o comando para gerar os PNGs depois |
| Levantamento desatualizado | Avisa e oferece atualizar; analista pode seguir |

## Validacao

Projeto de teste: `analistas-sugf` → `.projetos/inventario-florestal-web` (Angular 8.3 + Angular Material 8.2.3;
tema `indigo-pink.css` em `node_modules`, ausente no clone, que testa a fonte "pacote publicado").

Roteiro ponta a ponta: levantar → conferir amostra → nova tela → alterar tela existente (ex.: uma tela de
`src/app/components/inventario`) → 2 ajustes → finalizar.

Criterios de aceite:
- O analista reconhece o sistema na `amostra.html`.
- `CATALOGO.md` lista as telas das rotas do projeto com arquivo-fonte correto.
- Em alteracao, a skill encontra a tela certa e pede confirmacao antes de gerar.
- `entrega/mockup.html` abre corretamente depois de copiado sozinho para outra pasta (autocontido).
- Os PNGs saem um por estado, com os nomes do contrato.
- `especificacao.md` cobre tudo o que foi pedido e ajustado no `NOTAS.md`.

## Fora da v1

- Relatorios (mesmo esqueleto, depois de validado o fluxo de telas).
- Geracao de tarefas/historias para desenvolvedores.
- Sistemas desktop.
- Prototipo dentro do proprio app (abordagem B), se o kit nao bastar para algum sistema.
