"""확장 사업계획 페이지(expansion.html)를 붙인다. 다시 돌려도 안전.

    python scripts/add_expansion_page.py

- expansion.html               modoo.html 껍데기 복사 (제목·SEO·data-page)
- content/pages/expansion.html [data-expansion] 자리 — 본문은 assets/js/expansion.js 가 data/expansion.json 으로 그린다
- data/site.json               메뉴(시장 다음)·페이지 순서·바닥글
- content/pages/usecases.html  확장 경로 섹션에 새 페이지 안내 한 줄
- assets/css/style.css         scripts/expansion.css 덧붙임
"""
import datetime as dt, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")
d = json.loads(rd("data/expansion.json"))

title = "확장 사업계획 · Keep121"
desc = "시니어 단체여행에서 초중고 체험학습·수학여행, 유치원·어린이집 통학, 치매 어르신까지 — 국내 확장 TAM·SAM·SOM과 진입 로드맵."
shell = rd("modoo.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, shell)
shell = shell.replace("keep121/modoo.html", "keep121/expansion.html").replace('data-page="modoo"', 'data-page="expansion"')
shell = re.sub(r'assets/css/style\.css(\?v=\d+)?', f"assets/css/style.css?v={V}", shell)
wr("expansion.html", shell)
wr("content/pages/expansion.html", "<!-- 확장 사업계획: assets/js/expansion.js 가 data/expansion.json 으로 이 자리를 채운다. -->\n<div data-expansion></div>\n")
for f in ROOT.glob("*.html"):
    t = f.read_text(encoding="utf-8")
    n = re.sub(r'assets/css/style\.css(\?v=\d+)?"', f'assets/css/style.css?v={V}"', t)
    if n != t:
        f.write_text(n, encoding="utf-8")

s = json.loads(rd("data/site.json"))
if not any(n["href"] == "expansion.html" for n in s["nav"]):
    i = next(i for i, n in enumerate(s["nav"]) if n["href"] == "usecases.html") + 1
    s["nav"].insert(i, {"href": "expansion.html", "label": "확장"})
pages = [p for p in s["pages"] if p["id"] != "expansion"]
i = next(i for i, p in enumerate(pages) if p["id"] == "usecases") + 1
pages.insert(i, {"id": "expansion", "file": "expansion.html", "name": "확장 사업계획", "script": "assets/js/expansion.js"})
for p in pages:
    if p.get("script"):
        p["script"] = p["script"].split("?")[0] + f"?v={V}"
s["pages"] = pages
for c in s["footer"]["columns"]:
    if any(l["href"] == "usecases.html" for l in c["links"]) and not any(l["href"] == "expansion.html" for l in c["links"]):
        j = next(j for j, l in enumerate(c["links"]) if l["href"] == "usecases.html") + 1
        c["links"].insert(j, {"href": "expansion.html", "label": "확장 사업계획"})
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=1) + "\n")

u = rd("content/pages/usecases.html")
if "expansion.html" not in u:
    a = u.index('<section class="soft" id="expansion">')
    b = u.index('<div class="stages">', a)
    note = ('<p class="notice reveal mt-s"><svg class="icon"><use href="#i-route"/></svg><span><b>2026.11 확장 사업계획</b> · 국내 시장을 초중고 체험학습·수학여행, 유치원·어린이집 통학, 치매 어르신으로 넓힌 새 계획(SAM 약 890억 원)을 '
            '<a href="expansion.html">확장 사업계획</a>에 정리했습니다. 아래 단계는 기존 계획입니다.</span></p>\n')
    wr("content/pages/usecases.html", u[:b] + note + u[b:])

css = rd("assets/css/style.css")
if "/* 확장 사업계획 페이지 */" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n" + rd("scripts/expansion.css"))
print("  expansion.html · content/pages/expansion.html · data/site.json · usecases.html · style.css")
