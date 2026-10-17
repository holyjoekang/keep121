"""Build English / Chinese pages from the Korean source pages.

The Korean pages at the repo root stay the single source of truth. This script
cuts every Korean text block (and Korean attribute values) out of each page,
looks up its translation in i18n/<lang>.json, and writes en/*.html, zh/*.html.

  python tools/i18n_build.py extract   # refresh i18n/segments.json (Korean strings to translate)
  python tools/i18n_build.py build     # write en/ and zh/ pages; lists anything untranslated
"""
import html.parser
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'solution.html', 'evidence.html', 'product.html', 'family.html',
         'usecases.html', 'business.html', 'company.html']
LANGS = {'en': 'en', 'zh': 'zh-CN'}
HANGUL = re.compile('[가-힣]')
# Elements that break a text block; anything else (b, span, small, br, em, a, q...) stays inside one segment.
BLOCK = set('''html head body header footer nav main section article aside div p ul ol li dl dt dd table thead tbody
tr td th h1 h2 h3 h4 h5 h6 figure figcaption form label button select option details summary blockquote
svg g text symbol defs title meta link script style output input textarea fieldset'''.split())
VOID = set('area base br col embed hr img input link meta source track wbr'.split())
SKIP = {'script', 'style'}
ATTR = re.compile(r'(\s(?:aria-label|title|alt|placeholder|content|data-n|data-label)=")([^"]*)(")')


class Node:
    def __init__(self, tag, start, inner):
        self.tag, self.start, self.inner, self.end, self.children, self.texts = tag, start, inner, None, [], []


class Tree(html.parser.HTMLParser):
    """Records source offsets so segments can be replaced in the original text."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for m in re.finditer('\n', src):
            self.lines.append(m.end())
        self.root = Node('#root', 0, 0)
        self.stack = [self.root]
        self.starttags = []

    def off(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        o = self.off()
        text = self.get_starttag_text()
        self.starttags.append((o, o + len(text)))
        if tag in VOID or text.endswith('/>'):
            return
        n = Node(tag, o, o + len(text))
        self.stack[-1].children.append(n)
        self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        o = self.off()
        self.starttags.append((o, o + len(self.get_starttag_text())))

    def handle_endtag(self, tag):
        o = self.off()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                for n in self.stack[i:]:
                    n.end = o
                del self.stack[i:]
                return

    def handle_data(self, data):
        o = self.off()
        self.stack[-1].texts.append((o, o + len(data)))

    handle_entityref = handle_charref = lambda self, name: None


def has_block(n):
    return any(c.tag in BLOCK or has_block(c) for c in n.children)


def segments(src):
    """Return [(start, end, text)] spans of Korean text blocks and attribute values."""
    t = Tree(src)
    t.feed(src)
    t.close()
    t.root.end = len(src)
    out = []

    def walk(n):
        if n.tag in SKIP or n.end is None:
            return
        inner = src[n.inner:n.end]
        if not HANGUL.search(re.sub(r'<[^>]*>', '', inner)):
            return
        if n.tag != '#root' and n.tag != 'head' and not has_block(n):
            s, e = n.inner, n.end
            while s < e and src[s].isspace():
                s += 1
            while e > s and src[e - 1].isspace():
                e -= 1
            out.append((s, e, src[s:e]))
            return
        for a, b in n.texts:
            txt = src[a:b]
            if HANGUL.search(txt):
                s = a + len(txt) - len(txt.lstrip())
                e = b - (len(txt) - len(txt.rstrip()))
                out.append((s, e, src[s:e]))
        for c in n.children:
            walk(c)

    walk(t.root)
    for a, b in t.starttags:
        for m in ATTR.finditer(src, a, b):
            if HANGUL.search(m.group(2)):
                out.append((m.start(2), m.end(2), m.group(2)))
    out.sort()
    return out


def read(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8').read()


def extract():
    seen, order = {}, []
    for page in PAGES:
        for _, _, txt in segments(read(page)):
            if txt not in seen:
                seen[txt] = page
                order.append(txt)
    path = os.path.join(ROOT, 'i18n', 'segments.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump([{'page': seen[t], 'ko': t} for t in order], io.open(path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(len(order), 'segments ->', path)


SWITCH = ('<div class="lang-switch" aria-label="Language">'
          '<a href="{ko}" hreflang="ko" lang="ko"{a_ko}>KO</a>'
          '<a href="{en}" hreflang="en" lang="en"{a_en}>EN</a>'
          '<a href="{zh}" hreflang="zh-CN" lang="zh-CN"{a_zh}>中文</a></div>')
SITE = 'https://holyjoekang.github.io/keep121/'


def switcher(page, here):
    cur = ' aria-current="true"'
    if here == 'ko':
        hrefs = dict(ko=page, en='en/' + page, zh='zh/' + page)
    else:
        hrefs = dict(ko='../' + page, en=('' if here == 'en' else '../en/') + page,
                     zh=('' if here == 'zh' else '../zh/') + page)
    return SWITCH.format(**hrefs, a_ko=cur if here == 'ko' else '', a_en=cur if here == 'en' else '',
                         a_zh=cur if here == 'zh' else '')


NAV_ANCHOR = re.compile(r'(\s*)(<a class="btn btn-primary" href="company\.html#contact">)')


def add_switcher(src, page, here):
    src = re.sub(r'\s*<div class="lang-switch".*?</div>', '', src, count=1)
    return NAV_ANCHOR.sub(lambda m: m.group(1) + switcher(page, here) + m.group(1) + m.group(2), src, count=1)


def localize_paths(src, lang):
    src = re.sub(r'((?:href|src)=")(assets/|Keep121_|story/)', r'\1../\2', src)
    src = re.sub(r"url\('assets/", "url('../assets/", src)
    src = src.replace('<html lang="ko">', '<html lang="%s">' % LANGS[lang])
    src = re.sub(r'(<meta property="og:url" content="%s)([^"]*)"' % re.escape(SITE),
                 lambda m: m.group(1) + lang + '/' + m.group(2) + '"', src)
    # Chinese-friendly fonts; English keeps the Latin glyphs of IBM Plex Sans KR.
    if lang == 'zh':
        src = src.replace('family=IBM+Plex+Sans+KR:wght@400;500;600;700',
                          'family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700;800')
    src = src.replace('<script src="../assets/js/main.js" defer></script>',
                      '<script src="../assets/js/i18n.%s.js" defer></script>\n'
                      '<script src="../assets/js/main.js" defer></script>' % lang)
    return src


def build():
    missing = {}
    for lang in LANGS:
        if not os.path.exists(os.path.join(ROOT, 'i18n', lang + '.json')):
            print('skip', lang, '(no i18n/%s.json)' % lang)
            continue
        tr = json.load(io.open(os.path.join(ROOT, 'i18n', lang + '.json'), encoding='utf-8'))
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for page in PAGES:
            src = read(page)
            segs = segments(src)
            for s, e, txt in reversed(segs):
                if txt in tr and tr[txt]:
                    src = src[:s] + tr[txt] + src[e:]
                else:
                    missing.setdefault(lang, []).append((page, txt))
            src = add_switcher(localize_paths(src, lang), page, lang)
            io.open(os.path.join(ROOT, lang, page), 'w', encoding='utf-8', newline='').write(src)
    # Korean pages get the switcher too (idempotent).
    for page in PAGES:
        src = read(page)
        new = add_switcher(src, page, 'ko')
        if new != src:
            io.open(os.path.join(ROOT, page), 'w', encoding='utf-8', newline='').write(new)
    for lang, items in missing.items():
        print('[%s] %d untranslated' % (lang, len(items)))
        for page, txt in items[:40]:
            print('  ', page, '|', txt[:90])
    print('built', ', '.join(LANGS))


if __name__ == '__main__':
    {'extract': extract, 'build': build}[sys.argv[1] if len(sys.argv) > 1 else 'build']()
