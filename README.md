# JJ Ribas Climatização

Site institucional (HTML, CSS e JS puros) com foco em atendimento empresarial:
instalação, manutenção, higienização e contratos de PMOC em Porto Alegre, Canoas,
Sapucaia do Sul e São Leopoldo.

## Páginas

| Página           | Arquivo               |
| ---------------- | --------------------- |
| Início           | `index.html`          |
| Serviços         | `servicos.html`       |
| PMOC             | `pmoc.html`           |
| Para empresas    | `para-empresas.html`  |
| Onde atendemos   | `onde-atendemos.html` |
| Dúvidas          | `duvidas.html`        |
| Blog (6 artigos) | `blog.html`, `blog/`  |
| Contato          | `contato.html`        |

## Como editar

As páginas na raiz são **geradas**. Edite sempre os arquivos em `_src/` e depois rode:

```
python3 build.py
```

- `_src/partials/` – topo, menu, rodapé, faixa de orçamento e botões flutuantes (comuns a todas as páginas)
- `_src/pages/` – conteúdo de cada página e dos artigos do blog

Dentro do HTML, `{{wa:mensagem}}` vira o link do WhatsApp com a mensagem pronta,
`{{tel}}` o link de ligação e `{{phone}}` o telefone formatado. O número fica em `build.py`.

## Contato configurado

- Telefone e WhatsApp: (51) 98051-5585
- Botão flutuante de ligação (vermelho) à esquerda e de WhatsApp (verde) à direita
- O formulário de contato monta a mensagem e abre o WhatsApp

## Imagens

Fotos em `img/fotos/` (geradas por IA). Para trocar, substitua o arquivo mantendo o nome.
Tamanho recomendado: 1264 x 848 px (a do início, 1152 x 928 px).

## Publicação

Site estático, pronto para Vercel (`vercel.json` com URLs limpas). Antes de publicar
no domínio final, troque `www.jjribasclimatizacao.com.br` em `build.py`, `sitemap.xml`,
`robots.txt` e nos dados estruturados das páginas.

## Logo

- `img/logo-marca.png` – símbolo usado no topo, ao lado do nome
- `img/logo-branca.png` – logo completa para fundo escuro (rodapé)
- `img/logo.png` – logo completa para fundo claro
- `img/favicon.png` e `img/apple-touch-icon.png` – ícones do navegador e do celular
