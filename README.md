# JJ Ribas Climatização

Site institucional (HTML, CSS e JS puros, sem build) com foco em atendimento empresarial:
instalação, manutenção, higienização e contratos de PMOC em Porto Alegre, Canoas,
Sapucaia do Sul e São Leopoldo.

## Estrutura

```
index.html          Página única com todas as seções
css/style.css       Estilos e responsividade
js/main.js          Menu mobile, animações e formulário -> WhatsApp
img/                Logo, favicon, hero, mapa e imagem de compartilhamento
img/servicos/       Imagens dos quatro serviços
```

## Contato configurado

- Telefone e WhatsApp: (51) 98051-5585
- Botão flutuante de ligação à esquerda e de WhatsApp à direita
- O formulário de contato monta a mensagem e abre o WhatsApp

## Trocar imagens

As imagens atuais são ilustrações. Para usar fotos, coloque os arquivos em
`img/servicos/` (ex.: `instalacao.jpg`) e atualize o `src` correspondente em `index.html`.
Tamanho recomendado: 1200 x 800 px (proporção 3:2).

O logo fica em `img/logo.svg`.

## Visualizar

Basta abrir `index.html` no navegador, ou publicar a pasta em qualquer hospedagem
estática (Vercel, Netlify, GitHub Pages, Hostinger etc.).
