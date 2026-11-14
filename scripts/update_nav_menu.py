"""상단 메뉴를 바닥글 구조(서비스·비즈니스·회사)에 '맞춤 제안'을 더한 4개 대메뉴로 단순화한다. 다시 돌려도 안전.

    python scripts/update_nav_menu.py

- data/site.json   menu(대메뉴→서브메뉴) 추가, 바닥글에 Proposals 칸 분리
- assets/js/render.js   menu 로 드롭다운 메뉴를 그린다 (PC: 마우스·키보드 포커스 시 펼침, 모바일: 펼친 목록)
- assets/css/style.css  /* nav-menu */ 블록 (이 스크립트가 교체)

맞춤 제안은 앞으로 10개 안팎으로 늘어난다: PROPOSALS 목록에 한 줄씩 추가하고 다시 돌리면 된다.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

L = lambda h, t: {"href": h, "label": t}  # noqa: E731
PROPOSALS = [L("proposals.html", "전체 제안 보기"), L("wyd2027.html", "WYD 서울 2027 제안"), L("wyd2027-3d.html", "WYD 서울 2027 · 1분 3D"), L("jeju2027.html", "제주 이동안전 제안"), L("jeju2027-3d.html", "제주 이동안전 · 1분 3D"), L("ilsandong.html", "일산동중학교 체험학습 제안"), L("galilee.html", "갈릴리여행사 성지순례 제안"),
             L("saga2027.html", "사랑글로벌아카데미 2027 통합 제안"), L("saga-visiontrip.html", "SaGA 일터선교 비전트립 제안"), L("saga-legacy.html", "레거시아카데미 1일 제안")]
MENU = [
 {"label": "서비스", "en": "Service", "items": [L("solution.html", "솔루션"), L("product.html", "제품"), L("operations.html", "운영 설계"),
                                                L("guide/", "Keep121 Guide 앱 (MVP)"), L("keeptrip.html", "KeepTrip (자매 앱)")]},
 {"label": "비즈니스", "en": "Business", "items": [L("usecases.html", "국내 시장"), L("b2b.html", "B2B 확장 전략"), L("business.html", "비즈니스 모델"),
                                                  L("evidence.html", "파일럿·로드맵"), L("modoo.html", "모두의 창업")]},
 {"label": "맞춤 제안", "en": "Proposals", "items": PROPOSALS},
 {"label": "회사", "en": "Company", "items": [L("company.html#vision", "비전"), L("company.html#team", "팀"), L("company.html#contact", "파일럿 문의")]},
]

# 1) site.json
s = json.loads(rd("data/site.json"))
s["menu"] = MENU
cols = [{"title": m["en"], "links": list(m["items"])} for m in MENU]
cols[-1]["links"].append(L("mailto:joekang@naver.com", "joekang@naver.com"))
s["footer"]["columns"] = cols
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")

# 2) render.js: nav() 를 드롭다운 메뉴로
js = rd("assets/js/render.js")
NEW = """  // 대메뉴(site.json menu) → 서브메뉴. PC는 마우스를 올리거나 키보드로 들어가면 펼치고, 모바일은 펼친 목록으로 보인다.
  const page = h => h.split('#')[0];
  const nav = s => `<div class="wrap">
    <a class="brand" href="index.html" aria-label="Keep121 홈">${brand}</a>
    <nav class="nav-links nav-menu" id="navLinks" aria-label="주요 메뉴">
      ${(s.menu || []).map(m => { const on = m.items.some(i => page(i.href) === here); return `<div class="nm${on ? ' on' : ''}">
        <a class="nm-top${on ? ' active' : ''}" href="${E(m.items[0].href)}" aria-haspopup="true">${E(m.label)}<svg class="nm-caret" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3"/></svg></a>
        <div class="nm-sub"><span class="nm-en">${E(m.en)}</span>${m.items.map(i => `<a href="${E(i.href)}"${page(i.href) === here && !i.href.includes('#') ? ' aria-current="page"' : ''}>${E(i.label)}</a>`).join('')}</div>
      </div>`; }).join('\\n      ')}
    </nav>
    <a class="btn btn-primary" href="${E(s.cta.href)}">${E(s.cta.label)}</a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기" aria-expanded="false"><svg class="icon"><use href="#i-menu"/></svg></button>
  </div>`;
"""
js = re.sub(r"(  // 대메뉴\(site\.json menu\).*?\n)?  const page = h => .*?\n(?=  const nav = s =>)", "", js, flags=re.S)
js, n = re.subn(r"  const nav = s => `<div class=\"wrap\">.*?</div>`;\n", lambda m: NEW, js, count=1, flags=re.S)
assert n == 1, "render.js nav() not found"
wr("assets/js/render.js", js)

# 3) style.css: 드롭다운 스타일
CSS = """/* nav-menu (scripts/update_nav_menu.py) */
.nav-menu { gap: 6px; align-items: center; }
.nav-menu .nm { position: relative; }
.nav-menu .nm-top { display: inline-flex; align-items: center; gap: 5px; padding: 10px 12px; border-radius: 10px; }
.nav-menu .nm-caret { width: 12px; height: 12px; fill: none; stroke: currentColor; stroke-width: 1.6; opacity: .7; transition: transform .2s; }
.nav-menu .nm-top.active::after { left: 12px; right: 12px; bottom: 2px; }
.nav-menu .nm-sub { position: absolute; top: 100%; left: 50%; min-width: 220px; padding: 12px 8px 10px; margin-top: 6px; background: #fff; border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 18px 50px rgba(14,18,38,.18); display: flex; flex-direction: column; opacity: 0; visibility: hidden; transform: translate(-50%, 6px); transition: opacity .18s, transform .18s, visibility .18s; z-index: 120; }
.nav-menu .nm-sub::before { content: ""; position: absolute; left: 0; right: 0; top: -14px; height: 14px; }
.nav-menu .nm-sub .nm-en { padding: 0 12px 6px; font: 600 11px/1 var(--display); letter-spacing: .14em; text-transform: uppercase; color: var(--soft); }
.nav-menu .nm-sub a { color: var(--text) !important; padding: 9px 12px; border-radius: 9px; font-size: 14.5px; font-weight: 500; white-space: nowrap; }
.nav-menu .nm-sub a:hover, .nav-menu .nm-sub a:focus-visible { background: var(--bg-soft); color: var(--ink) !important; }
.nav-menu .nm-sub a[aria-current="page"] { color: var(--sky) !important; font-weight: 700; }
.nav-menu .nm-sub a::after { display: none; }
@media (hover: hover) and (min-width: 961px) {
  .nav-menu .nm:hover .nm-sub, .nav-menu .nm:focus-within .nm-sub { opacity: 1; visibility: visible; transform: translate(-50%, 0); }
  .nav-menu .nm:hover .nm-caret, .nav-menu .nm:focus-within .nm-caret { transform: rotate(180deg); }
}
@media (max-width: 960px) {
  .nav .wrap:not(:has(.lang-switch)) > .nav-toggle { margin-left: auto; }
  .nav.open .nav-menu { max-height: calc(100vh - 72px); overflow-y: auto; align-items: stretch; }
  .nav.open .nav-menu .nm { width: 100%; }
  .nav.open .nav-menu .nm { border-bottom: 1px solid var(--line); padding: 6px 0 10px; }
  .nav.open .nav-menu .nm-top { padding: 10px 0 4px; font-size: 13px; color: var(--soft) !important; border: 0; pointer-events: none; }
  .nav.open .nav-menu .nm-caret, .nav.open .nav-menu .nm-sub .nm-en { display: none; }
  .nav.open .nav-menu .nm-sub { position: static; opacity: 1; visibility: visible; transform: none; box-shadow: none; border: 0; padding: 0; margin: 0; min-width: 0; display: grid; grid-template-columns: 1fr 1fr; }
  .nav.open .nav-menu .nm-sub a { padding: 9px 0; font-size: 15.5px; border: 0; }
}
/* /nav-menu */
"""
css = rd("assets/css/style.css")
css = re.sub(r"/\* nav-menu \(scripts/update_nav_menu\.py\) \*/.*?/\* /nav-menu \*/\n", "", css, flags=re.S)
wr("assets/css/style.css", css.rstrip("\n") + "\n\n" + CSS)
print("  site.json(menu·footer) · render.js(nav) · style.css(nav-menu)")

# 4) 캐시 갱신: 페이지 껍데기의 style.css·render.js 버전 올리기
import datetime as dt  # noqa: E402
V = dt.datetime.now().strftime("%Y%m%d%H%M")
for f in ROOT.glob("*.html"):
    t = f.read_text(encoding="utf-8")
    if "assets/js/render.js" not in t:
        continue
    t2 = re.sub(r'assets/css/style\.css(\?v=\d+)?"', f'assets/css/style.css?v={V}"', t)
    t2 = re.sub(r'assets/js/render\.js(\?v=\d+)?"', f'assets/js/render.js?v={V}"', t2)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
