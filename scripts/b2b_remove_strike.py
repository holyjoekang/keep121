"""B2B 확장 전략 '핵심 관점'에서 취소선 문구('Galaxy SmartTag3를 판매한다')를 지운다. 다시 돌려도 안전.

    python scripts/b2b_remove_strike.py

- data/b2b.json, scripts/add_b2b_page.py: view.no 를 빈 문자열로
- scripts/b2b.js → assets/js/b2b.js: view.no 가 비어 있으면 취소선 줄을 그리지 않음
- b2b.html: b2b.js 캐시 버전 갱신
"""
import datetime as dt, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

d = json.loads(rd("data/b2b.json"))
d["view"]["no"] = ""
wr("data/b2b.json", json.dumps(d, ensure_ascii=False, indent=1) + "\n")
wr("scripts/add_b2b_page.py", rd("scripts/add_b2b_page.py").replace('"no": "Galaxy SmartTag3를 판매한다"', '"no": ""'))

js = rd("scripts/b2b.js").replace("<p class=\"b2-statement\"><s>${E(v.no)}</s><br>${E(v.yes)}</p>",
                                  "<p class=\"b2-statement\">${v.no ? `<s>${E(v.no)}</s><br>` : ''}${E(v.yes)}</p>")
wr("scripts/b2b.js", js)
wr("assets/js/b2b.js", js)

s = json.loads(rd("data/site.json"))
for p in s["pages"]:
    if p["id"] == "b2b":
        p["script"] = re.sub(r"\?v=\d+", "", p["script"]) + f"?v={V}"
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")
print("  b2b 핵심 관점 취소선 제거")
