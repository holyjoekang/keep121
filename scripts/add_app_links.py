"""Keep121 Guide 앱(guide/) 바로가기와 KeepTrip App 연결 섹션을 사이트에 넣는다(다시 돌려도 안전).

- content/pages/product.html: Guide 섹션에 'Guide 앱 열기', KeepTrip 섹션에 'KeepTrip 앱 열기' 단추
- content/pages/index.html: 제품 구성의 Keep121 Guide 카드 → 앱 바로가기
- content/pages/keeptrip.html: 맨 아래 'KeepTrip App 연결하기' 섹션 + 이 페이지 메뉴 (기존 링크는 그대로)
- data/site.json: 바닥글 Service 열에 'Keep121 Guide 앱' 링크
- assets/css/style.css: 단추 줄 · 앱 연결 카드 스타일
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

GUIDE_URL = "guide/"
KEEPTRIP_URL = "https://keeptrip.ai.studio/"


def put(text, anchor, add, before=False, mark=None):
    if mark and mark in text:
        return text
    assert anchor in text, anchor[:60]
    return text.replace(anchor, add + anchor if before else anchor + add, 1)


# ---------- product.html: Guide 앱 열기 ----------
p = rd("content/pages/product.html")
GUIDE_BTN = f"""
      <div class="app-acts">
        <a class="btn btn-primary" href="{GUIDE_URL}" target="_blank" rel="noopener"><svg class="icon"><use href="#i-phone"/></svg>Guide 앱 열기 (MVP 데모)</a>
        <span class="fine">Android Chrome에서 명찰 NFC 탭까지 동작 · 데이터는 기기에만 저장</span>
      </div>"""
p = put(p, "<p class=\"fine mt-m\">이벤트 로그 스키마", GUIDE_BTN + "\n      ", before=True, mark='Guide 앱 열기')
KT_BTN = f"""
      <div class="app-acts">
        <a class="btn btn-dawn" href="{KEEPTRIP_URL}" target="_blank" rel="noopener"><svg class="icon"><use href="#i-pin"/></svg>KeepTrip 앱 열기</a>
        <span class="fine">keeptrip.ai.studio · 시제품(Google AI Studio) · 설치 없이 링크로</span>
      </div>"""
p = put(p, "<p class=\"fine mt-m\">위치는 여행객 본인이 동의한 경우에만", KT_BTN + "\n      ", before=True, mark='KeepTrip 앱 열기')
wr("content/pages/product.html", p)

# ---------- index.html: Guide 카드 → 앱 ----------
i = rd("content/pages/index.html")
OLD = '<a class="prod reveal" href="product.html#guide">'
if OLD in i:
    i = i.replace(OLD, f'<a class="prod reveal" href="{GUIDE_URL}" target="_blank" rel="noopener">', 1)
wr("content/pages/index.html", i)

# ---------- keeptrip.html: KeepTrip App 연결하기 ----------
k = rd("content/pages/keeptrip.html")
k = put(k, '<a href="#link">Keep121 연동</a>', '\n      <a href="#app">앱 연결</a>', mark='href="#app"')
APP = f"""

<!-- ============ KEEPTRIP APP ============ -->
<section class="soft" id="app">
  <div class="wrap">
    <div class="app-card reveal">
      <div>
        <span class="eyebrow">KeepTrip App</span>
        <h2>KeepTrip App<br><span class="hl">연결하기.</span></h2>
        <p>설치 없이 링크로 엽니다. 휴대폰에서 연 뒤 ‘홈 화면에 추가’하면 앱처럼 쓸 수 있습니다. 맞춤 준비, 오늘, 도착 해설, 보이스 기록, 여행 스토리를 지금 체험해 보세요.</p>
        <div class="app-acts">
          <a class="btn btn-dawn" href="{KEEPTRIP_URL}" target="_blank" rel="noopener"><svg class="icon"><use href="#i-pin"/></svg>KeepTrip App 열기</a>
          <span class="fine">keeptrip.ai.studio · 시제품(Google AI Studio)</span>
        </div>
      </div>
      <ul class="app-steps">
        <li><b>1</b><span>휴대폰 브라우저로 링크 열기</span></li>
        <li><b>2</b><span>내 여행 일정 선택 또는 추가</span></li>
        <li><b>3</b><span>공유 메뉴에서 ‘홈 화면에 추가’</span></li>
      </ul>
    </div>
  </div>
</section>
"""
if 'id="app"' not in k:
    k = k.rstrip("\n") + APP
wr("content/pages/keeptrip.html", k)

# ---------- site.json: footer link ----------
s = json.loads(rd("data/site.json"))
svc = next(c for c in s["footer"]["columns"] if c["title"] == "Service")
if not any(l["href"] == GUIDE_URL for l in svc["links"]):
    at = next(n for n, l in enumerate(svc["links"]) if l["href"] == "product.html") + 1
    svc["links"].insert(at, {"href": GUIDE_URL, "label": "Keep121 Guide 앱 (MVP)"})
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=1) + "\n")

# ---------- CSS ----------
css = rd("assets/css/style.css")
CSS = """
/* App shortcuts (scripts/add_app_links.py) */
.app-acts { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px; margin-top: 24px; }
.app-acts .fine { margin: 0; }
.app-card { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 32px; align-items: center; padding: 40px; border-radius: 28px; background: #fff; border: 1px solid var(--line); box-shadow: var(--shadow); }
.app-card h2 { margin: 12px 0 14px; }
.app-card p { color: var(--muted); margin: 0; }
.app-steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
.app-steps li { display: flex; align-items: center; gap: 12px; padding: 14px 16px; border-radius: 16px; background: var(--bg-soft); }
.app-steps b { width: 32px; height: 32px; border-radius: 16px; background: var(--indigo); color: #fff; display: grid; place-items: center; flex: none; font-size: 14px; }
@media (max-width: 900px) { .app-card { grid-template-columns: 1fr; padding: 24px; } }
"""
if ".app-card" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n" + CSS)

print("done")
