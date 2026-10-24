"""모두의 창업 진행 페이지(modoo.html)를 사이트에 붙인다(한 번만, 다시 돌려도 안전).

- data/site.json: 상단 메뉴 · 바닥글 Business 열 · 페이지 순서에 modoo 추가 (페이지 전용 스크립트 assets/js/modoo.js)
- assets/js/render.js: site.json 페이지 항목에 "script"가 있으면 본문을 그린 뒤 붙인다
- modoo.html: evidence.html 껍데기를 복사해 제목·SEO·data-page 만 바꾼다
- assets/css/style.css: 모두의 창업 페이지 스타일 추가
- README.md: 구성 목록에 한 줄
본문은 content/pages/modoo.html, 진행 상태는 data/modoo.json(갱신은 scripts/modoo.py).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

# site.json
site = json.loads(rd("data/site.json"))
if not any(n["href"] == "modoo.html" for n in site["nav"]):
    site["nav"].append({"href": "modoo.html", "label": "모두의 창업"})
biz = next(c for c in site["footer"]["columns"] if c["title"] == "Business")
if not any(l["href"] == "modoo.html" for l in biz["links"]):
    biz["links"].append({"href": "modoo.html", "label": "모두의 창업"})
if not any(p["id"] == "modoo" for p in site["pages"]):
    site["pages"].append({"id": "modoo", "file": "modoo.html", "name": "모두의 창업", "script": "assets/js/modoo.js"})
wr("data/site.json", json.dumps(site, ensure_ascii=False, indent=1) + "\n")

# render.js: 페이지 전용 스크립트
js = rd("assets/js/render.js")
if "pg.script" not in js:
    anchor = "    document.body.appendChild(js);\n"
    assert anchor in js
    js = js.replace(anchor, anchor + "    const pg = s.pages.find(p => p.id === id);\n"
                    "    if (pg && pg.script) { const x = document.createElement('script'); x.src = pg.script; document.body.appendChild(x); }\n", 1)
    wr("assets/js/render.js", js)

# modoo.html 껍데기
title = "모두의 창업 2기 · Keep121"
desc = "Keep121의 모두의 창업 2기 1라운드 진행 기록: 일정, 1:1 책임멘토링, 창업활동자금 200만 원 집행, AI 솔루션 100만 원, 12월 1일 사업계획서 제출까지."
shell = rd("evidence.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', rf"\g<1>{desc}", shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', rf"\g<1>{title}", shell)
shell = shell.replace("keep121/evidence.html", "keep121/modoo.html").replace('data-page="evidence"', 'data-page="modoo"')
assert 'data-page="modoo"' in shell
wr("modoo.html", shell)

# CSS
css = rd("assets/css/style.css")
if "/* 모두의 창업 진행 페이지 */" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n" + (ROOT / "scripts/modoo.css").read_text(encoding="utf-8"))

# README
md = rd("README.md")
if "modoo.html" not in md:
    line = "- `company.html` — 비전·가치 · 브랜드 · 창업자·자문 · 팀 구성 계획 · 파일럿 문의\n"
    assert line in md
    md = md.replace(line, line + "- `modoo.html` — 모두의 창업 2기 1라운드 진행: 지금 할 일 · 일정 · 책임멘토링 · 창업활동자금 · AI 솔루션 · 사업계획서 · 진행 로그. "
                    "상태는 `data/modoo.json`, 갱신은 `scripts/modoo.py`, 메일 요약·받은 자료는 `모두의창업/`\n", 1)
    wr("README.md", md)
print("modoo 페이지 연결 완료", file=sys.stderr)
