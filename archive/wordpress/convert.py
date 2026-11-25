#!/usr/bin/env python3
"""Einmalige Übernahme der WordPress-Beiträge von loydl.ch als statische Seiten.

Eingabe:  archive/wordpress/posts.json (REST-Export vom 25.11.2026)
Ausgabe:  blog/<slug>.html, blog/index.html, assets/blog/<jahr>/<monat>/<datei>

Aufruf aus dem Projekt-Root:  python3 archive/wordpress/convert.py [--download]
--download lädt die Bilder von loydl.ch/wp-content/uploads herunter (nur solange WordPress erreichbar ist).
"""
import html
import json
import pathlib
import re
import sys
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
POSTS = json.loads((ROOT / 'archive/wordpress/posts.json').read_text())
DOWNLOAD = '--download' in sys.argv

UPLOAD_RE = re.compile(r'https?://(?:www\.)?loydl\.ch/wp-content/uploads/(\d{4})/(\d{2})/([^"?#\s]+)(?:\?[^"\s]*)?')
SITE_RE = re.compile(r'https?://(?:www\.)?loydl\.ch(/[^"\s]*)?')

ALLOWED = {
    'p': (), 'br': (), 'hr': (), 'h2': (), 'h3': (), 'h4': (), 'strong': (), 'b': (), 'em': (), 'i': (),
    'ul': (), 'ol': (), 'li': (), 'blockquote': (), 'pre': (), 'code': (), 'dl': ('class',), 'dt': ('class',), 'dd': (),
    'a': ('href', 'title'), 'img': ('src', 'alt', 'width', 'height'), 'figure': (), 'figcaption': (),
    'table': (), 'thead': (), 'tbody': (), 'tr': (), 'th': (), 'td': (),
}
RENAME = {'h1': 'h2'}
DROP_WITH_CONTENT = {'style', 'script', 'iframe', 'noscript'}
VOID = {'br', 'hr', 'img'}

downloaded = []


def local_upload(url):
    m = UPLOAD_RE.match(url)
    if not m:
        return None
    year, month, name = m.groups()
    rel = f'assets/blog/{year}/{month}/{name}'
    target = ROOT / rel
    if DOWNLOAD and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        src = f'https://loydl.ch/wp-content/uploads/{year}/{month}/{name}'
        with urllib.request.urlopen(src, timeout=30) as r:
            target.write_bytes(r.read())
        downloaded.append(rel)
    return '/' + rel


def rewrite_url(url):
    url = html.unescape(url)
    local = local_upload(url)
    if local:
        return local
    m = SITE_RE.fullmatch(url)
    if m:
        return m.group(1) or '/'
    return url


class Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
            return
        if self.skip:
            return
        tag = RENAME.get(tag, tag)
        if tag not in ALLOWED:
            return
        keep = []
        for k, v in attrs:
            if k not in ALLOWED[tag] or v is None:
                continue
            if k in ('href', 'src'):
                v = rewrite_url(v)
            if k == 'class':
                v = ' '.join(c for c in v.split() if c.startswith('gallery-'))
                if not v:
                    continue
            keep.append(f'{k}="{html.escape(v, quote=True)}"')
        if tag == 'a' and any(a.startswith('href="http') for a in keep):
            keep += ['target="_blank"', 'rel="noopener"']
        if tag == 'img':
            keep.append('loading="lazy"')
        self.out.append(f'<{tag}{"" if not keep else " " + " ".join(keep)}>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        tag = RENAME.get(tag, tag)
        if tag in ALLOWED and tag not in VOID:
            self.out.append(f'</{tag}>')

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append(f'&{name};')

    def handle_charref(self, name):
        if not self.skip:
            self.out.append(f'&#{name};')


def clean(content):
    c = Cleaner()
    c.feed(content)
    out = ''.join(c.out)
    out = re.sub(r'<p>\s*(?:&nbsp;|\s|<br>)*\s*</p>', '', out)
    out = re.sub(r'\n{3,}', '\n\n', out)
    return out.strip()


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def excerpt(p, body):
    e = text(p['excerpt']['rendered'])
    if not e or e.startswith('['):
        e = text(body)
    e = re.sub(r'\s+', ' ', e)
    return e if len(e) <= 155 else e[:152].rsplit(' ', 1)[0] + ' …'


MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']


def date_de(iso):
    y, m, d = iso[:10].split('-')
    return f'{int(d)}. {MONTHS[int(m) - 1]} {y}'


# --- Seitenrahmen: Navigation und Footer wie auf den übrigen Seiten, aber mit absoluten Pfaden ---
INACT = 'text-gray-600 hover:text-purple-600 transition-colors'
ACT = 'text-purple-600 font-semibold transition-colors'
CTA = 'bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors'
ITEMS = [('/index.html', 'Home'), ('/services.html', 'Services'), ('/ai-solutions.html', 'AI Solutions'), ('/about.html', 'Über mich')]


def nav():
    d = [f'                    <a href="{h}" class="{INACT}">{l}</a>' for h, l in ITEMS]
    d.append(f'                    <a href="/contact.html" class="{CTA}">Kontakt</a>')
    m = [f'                <a href="{h}" class="block py-3 text-gray-700 hover:text-purple-600">{l}</a>' for h, l in ITEMS]
    m.append(f'                <a href="/contact.html" class="block mt-2 mb-3 text-center {CTA}">Kontakt</a>')
    src = (ROOT / 'impressum.html').read_text()
    block = re.search(r'<nav\b.*?</nav>', src, re.S).group(0)
    block = re.sub(r'<div class="hidden md:flex items-center gap-6">.*?\n                </div>',
                   '<div class="hidden md:flex items-center gap-6">\n' + '\n'.join(d) + '\n                </div>', block, flags=re.S)
    block = re.sub(r'(<div id="mobile-menu"[^>]*>).*?\n            </div>',
                   lambda x: x.group(1) + '\n' + '\n'.join(m) + '\n            </div>', block, flags=re.S)
    return block.replace('href="index.html"', 'href="/index.html"')


def footer():
    src = (ROOT / 'impressum.html').read_text()
    block = re.search(r'<footer\b.*?</footer>', src, re.S).group(0)
    block = block.replace('class="text-white font-semibold">Impressum', 'class="hover:text-white">Impressum')
    return re.sub(r'href="(?!https?:|mailto:|/)([^"]+)"', r'href="/\1"', block)


HEAD_STYLE = re.search(r'<style>.*?</style>', (ROOT / 'impressum.html').read_text(), re.S).group(0)


def page(lang, title, description, body):
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description, quote=True)}">
    <link rel="stylesheet" href="/styles.css">
    {HEAD_STYLE}
</head>
<body class="bg-gray-50">
    {nav()}

{body}

    {footer()}
</body>
</html>
'''


def post_page(p, body):
    title = text(p['title']['rendered'])
    article = f'''    <main class="container mx-auto px-4 pt-28 pb-16">
        <article class="max-w-3xl mx-auto bg-white rounded-xl shadow-sm p-6 md:p-10">
            <p class="text-sm text-gray-500 mb-2" lang="de"><a href="/blog/" class="text-purple-600 hover:underline">Blog-Archiv</a> · {date_de(p['date'])}</p>
            <h1 class="text-2xl md:text-4xl font-bold text-gray-800 mb-4">{html.escape(title)}</h1>
            <p class="text-sm bg-gray-100 text-gray-600 rounded-lg px-4 py-3 mb-8" lang="de">Archivbeitrag aus dem früheren Blog auf loydl.ch. Der Inhalt entspricht dem Stand vom {date_de(p['date'])}.</p>
            <div class="article">
{body}
            </div>
        </article>
    </main>'''
    return page('en', f'{title} | Blog-Archiv | LOYDL', excerpt(p, body), article)


def index_page(posts):
    items = []
    for p, body in posts:
        items.append(f'''            <li class="py-6">
                <p class="text-sm text-gray-500">{date_de(p['date'])}</p>
                <h2 class="text-xl font-bold text-gray-800 mt-1"><a href="/{p['slug']}/" class="hover:text-purple-600">{html.escape(text(p['title']['rendered']))}</a></h2>
                <p class="text-gray-600 mt-2" lang="en">{html.escape(excerpt(p, body))}</p>
            </li>''')
    main = f'''    <main class="container mx-auto px-4 pt-28 pb-16">
        <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-sm p-6 md:p-10">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-4">Blog-Archiv</h1>
            <p class="text-gray-600 mb-4">Beiträge aus dem früheren Blog auf loydl.ch, {posts[-1][0]['date'][:4]}–{posts[0][0]['date'][:4]}. Die Texte sind auf Englisch und entsprechen dem Stand ihres Erscheinungsdatums.</p>
            <ul class="divide-y divide-gray-200">
{chr(10).join(items)}
            </ul>
        </div>
    </main>'''
    return page('de', 'Blog-Archiv | LOYDL Unternehmensberatung', 'Beiträge 2013–2018 über GraphQL, Avaloq, Camunda und Process Mining aus dem früheren Blog von LOYDL.', main)


def main():
    out = ROOT / 'blog'
    out.mkdir(exist_ok=True)
    posts = []
    for p in sorted(POSTS, key=lambda x: x['date'], reverse=True):
        body = clean(p['content']['rendered'])
        posts.append((p, body))
        (out / f"{p['slug']}.html").write_text(post_page(p, body))
    (out / 'index.html').write_text(index_page(posts))
    print(f'{len(posts)} Beiträge, {len(downloaded)} Bilder geladen')
    for p, _ in posts:
        print(p['slug'])


if __name__ == '__main__':
    main()
