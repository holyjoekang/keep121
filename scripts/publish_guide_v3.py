"""Publish Guide v3 (Apple-style redesign) from scripts/guide_v3 into guide/."""
from pathlib import Path
import json, re
r = Path(__file__).resolve().parents[1]; src, g = r/'scripts/guide_v3', r/'guide'
for a, b in [('app.js', 'v3-app.js'), ('app.css', 'v3-app.css'), ('config.json', 'v3-config.json')]:
    (g/b).write_text((src/a).read_text())
p = g/'index.html'; s = p.read_text()
s = re.sub(r'\s*<link rel="preconnect"[^>]*>', '', s)
s = re.sub(r'\s*<link href="https://fonts.googleapis.com[^>]*>', '', s)
s = s.replace('v2-app.css', 'v3-app.css').replace('v2-app.js', 'v3-app.js')
s = s.replace('<meta name="theme-color" content="#23306B">', '<meta name="theme-color" content="#f2f2f7" media="(prefers-color-scheme: light)">\n  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">\n  <meta name="apple-mobile-web-app-capable" content="yes">\n  <meta name="apple-mobile-web-app-status-bar-style" content="default">\n  <meta name="apple-mobile-web-app-title" content="Keep Guide">')
p.write_text(s)
p = g/'sw.js'; s = p.read_text()
s = re.sub(r"'keep-guide-v\d+'", "'keep-guide-v3'", s)
s = re.sub(r"const SHELL = \[.*?\];", "const SHELL = ['./', 'index.html', 'v3-app.css', 'v3-app.js', 'v3-config.json', 'manifest.webmanifest', 'icon.svg'];", s)
dup = "if (res.ok && SHELL.some(p => new URL(p, self.registration.scope).href === url.href)) "
s = s.replace(dup*2, dup)
p.write_text(s)
p = g/'manifest.webmanifest'; m = json.loads(p.read_text())
m.update(description='단체 이동 인솔자용 점호·대응·장비 회수 앱', background_color='#F2F2F7', theme_color='#F2F2F7')
p.write_text(json.dumps(m, ensure_ascii=False, indent=2)+'\n')
for f in ['v2-app.js', 'v2-app.css']: (g/f).unlink(missing_ok=True)
print('published guide v3')
