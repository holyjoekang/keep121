"""Keep121 소개 사이트를 동적으로 바꾼다(한 번만).

- 공통 메뉴·바닥글·페이지 순서 → data/site.json
- 페이지마다 본문(<main> 안, 이전/다음 단추 제외) → content/pages/<id>.html
- 각 *.html 은 머리말(head·SEO)과 빈 자리만 남고, assets/js/render.js 가 site.json 과 본문을 받아 그린 뒤
  assets/js/main.js(영상·점호 체험·견적 계산기)를 붙인다.
다시 돌리면 아무 일도 하지 않는다.
"""
import html as H, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["index", "solution", "product", "family", "usecases", "business", "evidence", "company"]
pages = {p: (ROOT / f"{p}.html").read_text(encoding="utf-8") for p in ORDER}
if 'assets/js/render.js' in pages["index"]:
    raise SystemExit("이미 동적입니다")
txt = lambda s: H.unescape(re.sub(r"<[^>]+>", "", s)).strip()  # noqa: E731

idx = pages["index"]
header = re.search(r'<header class="nav" id="nav">.*?</header>', idx, re.S).group(0)
footer = re.search(r'<footer class="footer">.*?</footer>', idx, re.S).group(0)
site = {
    "nav": [{"href": h, "label": txt(l)} for h, l in re.findall(r'<a href="([^"]+)">(.*?)</a>', re.search(r'<nav class="nav-links".*?</nav>', header, re.S).group(0))],
    "cta": dict(zip(["href", "label"], re.search(r'<a class="btn btn-primary" href="([^"]+)">(.*?)</a>', header).groups())),
    "footer": {
        "tagHtml": re.search(r'<div class="footer-tag">(.*?)</div>', footer).group(1),
        "columns": [{"title": t, "links": [{"href": h, "label": txt(l)} for h, l in re.findall(r'<a href="([^"]+)">(.*?)</a>', body)]}
                    for t, body in re.findall(r"<div><h4>(.*?)</h4>(.*?)</div>", footer)],
        "disclaimer": txt(re.search(r'<p class="disclaimer">(.*?)</p>', footer, re.S).group(1)),
        "copy": txt(re.search(r'<p class="copy">(.*?)</p>', footer).group(1)),
        "creditHtml": re.search(r'<p class="photo-credit">(.*?)</p>', footer).group(1),
    },
    "pages": [],
}
out_dir = ROOT / "content/pages"; out_dir.mkdir(parents=True, exist_ok=True)
for p in ORDER:
    src = pages[p]
    m = re.search(r'<main id="top">\n?(.*?)</main>', src, re.S)
    body = re.sub(r'\n*<nav class="pager".*?</nav>\n*', "\n", m.group(1), flags=re.S)
    crumb = re.search(r'<nav class="crumb".*?<b>(.*?)</b>', body)
    site["pages"].append({"id": p, "file": f"{p}.html", "name": txt(crumb.group(1)) if crumb else "홈"})
    (out_dir / f"{p}.html").write_text(body.strip() + "\n", encoding="utf-8")
    # 껍데기: head·Joyhouse 띠·아이콘 묶음은 그대로, 메뉴·본문·바닥글은 빈 자리로
    shell = src.replace(re.search(r'<header class="nav" id="nav">.*?</header>', src, re.S).group(0),
                        '<header class="nav" id="nav" data-mount="nav"></header>')
    shell = shell.replace(m.group(0), f'<main id="top" data-page="{p}"></main>')
    shell = shell.replace(re.search(r'<footer class="footer">.*?</footer>', shell, re.S).group(0),
                          '<footer class="footer" data-mount="footer"></footer>')
    shell = shell.replace('<script src="assets/js/main.js" defer></script>', '<script src="assets/js/render.js" defer></script>')
    assert 'render.js' in shell, p
    (ROOT / f"{p}.html").write_text(shell, encoding="utf-8")
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data/site.json").write_text(json.dumps(site, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("동적 전환:", ", ".join(f"{p['id']}({p['name']})" for p in site["pages"]))
