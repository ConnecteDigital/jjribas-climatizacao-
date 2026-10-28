#!/usr/bin/env python3
"""Monta as páginas do site a partir de _src/.

Cada arquivo em _src/pages/ começa com um bloco de metadados:

    <!--
    title: Título da página
    description: Descrição para o Google
    nav: servicos
    -->

e o restante é o conteúdo do <main>. O cabeçalho, o rodapé e os botões
flutuantes vêm de _src/partials/. O resultado é gravado na raiz do projeto,
mantendo as subpastas (ex.: _src/pages/blog/x.html -> blog/x.html), e o
sitemap.xml é atualizado com todas as páginas.

Marcadores disponíveis no HTML:
    {{root}}          caminho relativo até a raiz ("" ou "../")
    {{tel}}           link de ligação
    {{phone}}         telefone formatado
    {{wa:mensagem}}   link do WhatsApp com a mensagem já codificada
    {{icon:nome}}     ícone SVG (whats, phone, pin, check, arrow)
    {{active:chave}}  marca o item de menu da página atual
    {{partial:nome}}  insere _src/partials/nome.html (ex.: {{partial:cta}})

Uso: python3 build.py
"""
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SRC = ROOT / "_src"
PHONE_DIGITS = "5551980515585"
PHONE_DISPLAY = "(51) 98051-5585"
PHONE_TEL = "051980515585"  # link dos botões de ligação (tel:051 98051-5585)
SITE_URL = "https://www.jjribasclimatizacao.com.br/"

ICONS = {
    "whats": '<svg class="icon" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3Zm0 23.7c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.2-.4A10.7 10.7 0 1 1 16 26.7Zm5.9-8c-.3-.2-1.9-1-2.2-1-.3-.2-.5-.2-.7.1l-1 1.3c-.2.2-.4.2-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6 0-.9.4-.3.3-1.1 1.1-1.1 2.7s1.2 3.2 1.3 3.4c.2.2 2.3 3.5 5.6 5 2.1.9 2.9 1 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5l-.6-.4Z"/></svg>',
    "phone": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>',
    "pin": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z"/></svg>',
    "check": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 16.2 5.3 12l-1.4 1.4 5.6 5.6 11-11-1.4-1.4z"/></svg>',
    "arrow": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 5.3 11.8 6.7l4.3 4.3H4v2h12.1l-4.3 4.3 1.4 1.4L20 12z"/></svg>',
}

META_RE = re.compile(r"\A\s*<!--(.*?)-->\s*", re.S)


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = META_RE.match(text)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        text = text[m.end():]
    return meta, text


def render(html, meta, rel):
    depth = len(rel.parts) - 1
    root = "../" * depth
    nav = meta.get("nav", "")
    page_path = rel.as_posix()
    canonical = SITE_URL + ("" if page_path == "index.html" else page_path.removesuffix(".html"))

    html = html.replace("{{title}}", meta.get("title", "JJ Ribas Climatização"))
    html = html.replace("{{description}}", meta.get("description", ""))
    html = html.replace("{{og_image}}", meta.get("og_image", "img/fotos/hero.jpg"))
    html = html.replace("{{canonical}}", canonical)
    html = html.replace("{{root}}", root)
    html = html.replace("{{tel}}", "tel:" + PHONE_TEL)
    html = html.replace("{{phone}}", PHONE_DISPLAY)
    html = re.sub(
        r"\{\{wa:(.*?)\}\}",
        lambda m: f"https://wa.me/{PHONE_DIGITS}?text=" + quote(m.group(1), safe=""),
        html,
    )
    html = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], html)
    html = re.sub(
        r"\{\{active:(\w+)\}\}",
        lambda m: ' class="is-active" aria-current="page"' if m.group(1) == nav else "",
        html,
    )
    return html


def main():
    partials = {p.stem: p.read_text(encoding="utf-8") for p in (SRC / "partials").glob("*.html")}
    pages = sorted((SRC / "pages").rglob("*.html"))
    for page in pages:
        meta, body = parse(page)
        rel = page.relative_to(SRC / "pages")
        body = re.sub(r"\{\{partial:(\w+)\}\}", lambda m: partials[m.group(1)], body)
        html = partials["head"] + partials["header"] + "<main>\n" + body + "</main>\n" + partials["footer"]
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(html, meta, rel), encoding="utf-8")
        print("ok", rel)

    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{'' if r == 'index.html' else r.removesuffix('.html')}</loc></url>"
        for r in (p.relative_to(SRC / "pages").as_posix() for p in pages)
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8",
    )

    unresolved = [p for p in pages if "{{" in (ROOT / p.relative_to(SRC / "pages")).read_text(encoding="utf-8")]
    if unresolved:
        raise SystemExit(f"marcadores não resolvidos em: {unresolved}")


if __name__ == "__main__":
    main()
