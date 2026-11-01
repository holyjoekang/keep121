"""멘토링 회차 상세 페이지(modoo-mN.html)를 만든다. 다시 돌려도 안전.

    python scripts/add_session_page.py 1

- modoo-mN.html                 modoo.html 껍데기 복사 (제목·SEO·data-page)
- content/pages/modoo-mN.html   [data-session="0N"] 자리만 둔다 — 본문은 assets/js/modoo-session.js 가
                                content/modoo/sessions/0N.json 으로 그린다
- data/site.json                페이지 순서에 추가 (모두의 창업 다음), 페이지 스크립트에 캐시 버전
- assets/js/modoo.js            회차 카드에 '상세 페이지' 버튼
- assets/css/style.css          scripts/modoo_session_page.css 덧붙임
"""
import datetime as dt, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
pid, nn = f"modoo-m{n}", f"{n:02d}"
s = json.loads(rd(f"content/modoo/sessions/{nn}.json"))
V = dt.datetime.now().strftime("%Y%m%d%H%M")

title = f"멘토링 {n}회차 · {s['title']} · 모두의 창업 · Keep121"
desc = s["summary"]
shell = rd("modoo.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, shell)
shell = shell.replace("keep121/modoo.html", f"keep121/{pid}.html").replace('data-page="modoo"', f'data-page="{pid}"')
shell = re.sub(r'assets/css/style\.css(\?v=\d+)?', f"assets/css/style.css?v={V}", shell)
wr(f"{pid}.html", shell)
m = rd("modoo.html")
wr("modoo.html", re.sub(r'assets/css/style\.css(\?v=\d+)?', f"assets/css/style.css?v={V}", m))
wr(f"content/pages/{pid}.html", f'<!-- 멘토링 {n}회차 상세: assets/js/modoo-session.js 가 content/modoo/sessions/{nn}.json 으로 이 자리를 채운다. -->\n<div data-session="{nn}"></div>\n')
print(f"  {pid}.html · content/pages/{pid}.html")

site = json.loads(rd("data/site.json"))
pages = [p for p in site["pages"] if p["id"] != pid]
i = next(i for i, p in enumerate(pages) if p["id"] == "modoo") + n
pages.insert(i, {"id": pid, "file": f"{pid}.html", "name": f"멘토링 {n}회차", "script": f"assets/js/modoo-session.js?v={V}"})
for p in pages:
    if p.get("script"):
        p["script"] = p["script"].split("?")[0] + f"?v={V}"
site["pages"] = pages
wr("data/site.json", json.dumps(site, ensure_ascii=False, indent=1) + "\n")
print("  data/site.json")

js = rd("assets/js/modoo.js")
if "ses-more" not in js:
    js = js.replace("</details>` : ''}\n</article>`).join(''),", "</details>` : ''}\n${s.page ? `<p class=\"ses-more\"><a class=\"btn btn-primary\" href=\"${E(s.page)}\">${s.n}회차 상세 페이지 보기 →</a></p>` : ''}\n</article>`).join(''),", 1)
    assert "ses-more" in js
    wr("assets/js/modoo.js", js)
    print("  assets/js/modoo.js")

css = rd("assets/css/style.css")
if "/* 모두의 창업 멘토링 회차 상세 페이지 */" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n" + rd("scripts/modoo_session_page.css"))
    print("  assets/css/style.css")
