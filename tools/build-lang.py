#!/usr/bin/env python3
"""Baut die Sprachseiten de/, it/, nl/, fr/ aus index.html (Englisch ist die Quelle).

Aufruf im Repo-Ordner:
    python3 tools/build-lang.py          baut alle Sprachen
    python3 tools/build-lang.py --keys   schreibt nur i18n/_en.json (alle Texte)

Texte stehen in i18n/<sprache>.json als {"englischer Text": "Übersetzung"}.
Namen und Ausdrücke, die in jeder Sprache gleich bleiben, stehen in i18n/_keep.json.
Fehlt ein Text (z. B. weil Sarah einen englischen Satz geändert hat), meldet das
Skript ihn und lässt auf der Sprachseite vorerst das Englisch stehen.
Kundenbewertungen (blockquote) werden nie übersetzt.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
I18N = ROOT / 'i18n'
SITE = 'https://www.garden-park.co.uk/'
LANGS = {  # code: (html lang, Name in der eigenen Sprache, og:locale)
    'en': ('en-GB', 'English', 'en_GB'),
    'de': ('de-CH', 'Deutsch', 'de_CH'),
    'it': ('it', 'Italiano', 'it_IT'),
    'nl': ('nl', 'Nederlands', 'nl_NL'),
    'fr': ('fr', 'Français', 'fr_FR'),
}
ATTRS = ('alt', 'aria-label', 'title', 'data-label-open', 'data-label-close', 'data-title')
META_CONTENT = re.compile(r'<meta (?:name="description"|property="og:(?:title|description)")')
SKIP_OPEN = re.compile(r'<(script|style|svg|blockquote|address)\b', re.I)
SKIP_CLOSE = re.compile(r'</(script|style|svg|blockquote|address)>', re.I)


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def translatable(s):
    s = norm(s)
    return bool(s) and re.search(r'[A-Za-zÀ-ÿ]', s) is not None


FLAGS = {  # kleine SVG-Fahnen (Emoji-Fahnen zeigt Windows nicht an)
    'en': '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true"><path d="M0 0h60v30H0z" fill="#012169"/><path d="M0 0l60 30M60 0L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30M60 0L0 30" stroke="#C8102E" stroke-width="2"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>',
    'de': '<svg class="flag" viewBox="0 0 5 3" aria-hidden="true"><path d="M0 0h5v1H0z" fill="#000"/><path d="M0 1h5v1H0z" fill="#D00"/><path d="M0 2h5v1H0z" fill="#FFCE00"/></svg>',
    'it': '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true"><path d="M0 0h1v2H0z" fill="#009246"/><path d="M1 0h1v2H1z" fill="#fff"/><path d="M2 0h1v2H2z" fill="#CE2B37"/></svg>',
    'nl': '<svg class="flag" viewBox="0 0 9 6" aria-hidden="true"><path d="M0 0h9v2H0z" fill="#AE1C28"/><path d="M0 2h9v2H0z" fill="#fff"/><path d="M0 4h9v2H0z" fill="#21468B"/></svg>',
    'fr': '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true"><path d="M0 0h1v2H0z" fill="#002395"/><path d="M1 0h1v2H1z" fill="#fff"/><path d="M2 0h1v2H2z" fill="#ED2939"/></svg>',
}


def lang_block(cur):
    out = []
    for code, (_, name, _) in LANGS.items():
        if cur == 'en':
            href = '' if code == 'en' else f'{code}/'
        else:
            href = '../' if code == 'en' else f'../{code}/'
        href = href or './'
        attr = ' aria-current="true"' if code == cur else ''
        out.append(f'<a href="{href}" hreflang="{code}" lang="{code}"{attr}>{FLAGS[code]}<span>{name}</span></a>')
    label = {'en': 'Language', 'de': 'Sprache', 'it': 'Lingua', 'nl': 'Taal', 'fr': 'Langue'}[cur]
    return ('<!--lang-start--><details class="nav-lang"><summary aria-label="' + label + ': ' + LANGS[cur][1] + '">'
            + FLAGS[cur] + '<span>' + cur.upper() + '</span><svg class="chev" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5l5 5 5-5"/></svg></summary>'
            + '<div class="lang-menu">' + ''.join(out) + '</div></details><!--lang-end-->')


def head_links(cur):
    url = SITE if cur == 'en' else f'{SITE}{cur}/'
    alt = ''.join(f'<link rel="alternate" hreflang="{c}" href="{SITE if c == "en" else SITE + c + "/"}">\n'
                  for c in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}">\n'
    return (f'<!--head-start-->\n<link rel="canonical" href="{url}">\n{alt}'
            f'<meta property="og:locale" content="{LANGS[cur][2]}">\n<!--head-end-->')


def walk(html, fn_text, fn_attr):
    """Geht durch alle Texte und übersetzbaren Attribute; fn_* geben Ersatz zurück."""
    parts = re.split(r'(<[^>]+>)', html)
    depth = 0
    in_body = False
    for i, p in enumerate(parts):
        if p.startswith('<'):
            if p.startswith('<!--'):
                continue
            if SKIP_OPEN.match(p) and not p.endswith('/>'):
                depth += 1
            elif SKIP_CLOSE.match(p):
                depth = max(0, depth - 1)
            if p.lower().startswith('<body'):
                in_body = True
            if p.lower().startswith('<title'):
                parts[i + 1] = fn_text(parts[i + 1])
            def rep(m):
                return f'{m.group(1)}="{fn_attr(m.group(2))}"'
            p2 = re.sub(r'\b(' + '|'.join(ATTRS) + r')="([^"]*)"', rep, p)
            if META_CONTENT.match(p):
                p2 = re.sub(r'content="([^"]*)"', lambda m: f'content="{fn_attr(m.group(1))}"', p2)
            parts[i] = p2
        elif in_body and depth == 0 and translatable(p) and not parts[i - 1].lower().startswith('<title'):
            parts[i] = fn_text(p)
    return ''.join(parts)


def jsonld_desc(html, fn):
    html = re.sub(r'("description": ")([^"]*)(")', lambda m: m.group(1) + fn(m.group(2)) + m.group(3), html)
    # FAQ-Daten für Google: Fragen und Antworten mitübersetzen
    def faq(m):
        return re.sub(r'("(?:name|text)": ")((?:[^"\\]|\\.)*)(")',
                      lambda n: n.group(1) + json.dumps(fn(json.loads('"' + n.group(2) + '"')), ensure_ascii=False)[1:-1] + n.group(3), m.group(0))
    return re.sub(r'<script type="application/ld\+json" id="faq-ld">.*?</script>', faq, html, flags=re.S)


def collect(html):
    keys = []
    def add(s):
        k = norm(s)
        if translatable(k) and k not in keys:
            keys.append(k)
        return s
    walk(html, add, add)
    jsonld_desc(html, add)
    return keys


def fix_paths(html):
    html = re.sub(r'(["\s,])(img|assets|grantown-map)/', r'\1../\2/', html)
    return html


def main():
    src = SRC.read_text(encoding='utf-8')
    # Sprachwahl und Kopf-Links auch in der englischen Quelle aktuell halten
    src = re.sub(r'<!--lang-start-->.*?<!--lang-end-->', lambda m: lang_block('en'), src, flags=re.S)
    src = re.sub(r'<!--head-start-->.*?<!--head-end-->', lambda m: head_links('en'), src, flags=re.S)
    SRC.write_text(src, encoding='utf-8')

    keys = collect(re.sub(r'<!--lang-start-->.*?<!--lang-end-->', '', src, flags=re.S))  # Sprachwahl baut lang_block selber
    I18N.mkdir(exist_ok=True)
    (I18N / '_en.json').write_text(json.dumps(keys, ensure_ascii=False, indent=1), encoding='utf-8')
    if '--keys' in sys.argv:
        print(len(keys), 'Texte in i18n/_en.json')
        return
    keep = set(json.loads((I18N / '_keep.json').read_text(encoding='utf-8')))
    keep |= {norm(k) for k in collect(lang_block('en'))} | {v[1] for v in LANGS.values()}  # wird pro Sprache neu gebaut

    for code in LANGS:
        if code == 'en':
            continue
        f = I18N / f'{code}.json'
        if not f.exists():
            continue
        tr = json.loads(f.read_text(encoding='utf-8'))
        missing = []
        def t(s):
            k = norm(s)
            if not translatable(k) or k in keep:
                return s
            if k in tr:
                lead = s[:len(s) - len(s.lstrip())]
                trail = s[len(s.rstrip()):]
                return lead + tr[k] + trail
            missing.append(k)
            return s
        out = walk(src, t, t)
        out = jsonld_desc(out, t)
        out = out.replace('<html lang="en-GB">', f'<html lang="{LANGS[code][0]}">', 1)
        out = re.sub(r'<!--lang-start-->.*?<!--lang-end-->', lambda m: lang_block(code), out, flags=re.S)
        out = re.sub(r'<!--head-start-->.*?<!--head-end-->', lambda m: head_links(code), out, flags=re.S)
        out = out.replace('"url": "https://www.garden-park.co.uk/"', f'"url": "{SITE}{code}/"', 1)
        out = fix_paths(out)
        d = ROOT / code
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(out, encoding='utf-8')
        unused = [k for k in tr if k not in keys]
        print(f'{code}: gebaut, {len(missing)} fehlend, {len(unused)} nicht mehr gebraucht')
        for k in missing:
            print('   FEHLT  ', k[:90])
        for k in unused:
            print('   ALT    ', k[:90])


if __name__ == '__main__':
    main()
