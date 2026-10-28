"""KeepTrip을 솔루션·제품 섹션에 '여행객 앱(패키지 모드)'으로 넣는다(다시 돌려도 안전).

단체 여행객도 KeepTrip으로 패키지 일정을 따라가면서, 스스로 필요한 정보를 얻고 기록한다.
- content/pages/solution.html: '여행객 앱' 섹션 + 이 페이지 메뉴
- content/pages/product.html: 라인업 표 한 줄, 'KeepTrip 패키지 모드' 섹션, 메뉴, 2027 로드맵
- content/pages/index.html: 제품 구성 카드에 KeepTrip 추가 (넷 → 다섯)
- assets/css/style.css: 5칸 제품 그리드
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

def put(text, anchor, add, before=False):
    assert anchor in text, anchor[:60]
    return text.replace(anchor, add + anchor if before else anchor + add, 1)

PHONE = """<div class="kt-phone reveal" aria-label="KeepTrip 패키지 모드 화면 예시">
      <div class="kt-ph-top"><span>다낭 5일 · DAY 2</span><b>가이드 확인 10:42</b></div>
      <h4>호이안 구시가지</h4><p class="kt-ph-sub">자유시간 · 14:30 내원교 앞 집합</p>
      <div class="kt-ph-play"><span class="kt-ph-btn" aria-hidden="true"><svg class="icon"><use href="#i-play"/></svg></span><div><b>3분 음성 해설</b><i><em></em></i></div></div>
      <ol class="kt-ph-list"><li>내원교(일본교)</li><li>떤끼 고가</li><li>호이안 야시장</li></ol>
      <div class="kt-ph-voice">말로 기록하기</div>
    </div>"""

SOL = f"""
<!-- ============ TRAVELER APP (KeepTrip) ============ -->
<section class="soft" id="traveler">
  <div class="wrap feature-grid">
    {PHONE}
    <div class="feature-copy reveal d1">
      <span class="eyebrow">For Travelers · KeepTrip</span>
      <h2>가이드는 Guide로,<br><span class="hl">여행객은 KeepTrip으로.</span></h2>
      <p>단체 여행객도 휴대폰 링크 하나로 패키지 일정을 따라가면서, 스스로 필요한 정보를 얻고 자기 여행을 기록합니다. 앱 설치는 없습니다. 가이드에게 몇 번이고 묻던 “몇 시까지 어디로?”가 화면에 있습니다.</p>
      <ul class="feature-list">
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>패키지를 따라가기</b> 여행사 일정이 그대로 들어오고, 가이드가 바꾼 집합 시각·장소가 바로 반영</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>스스로 알아보기</b> 도착한 곳의 해설과 꼭 볼 것, 자유시간 주변 정보</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>나만의 기록</b> 말로 남기면 정리되고, 귀국 후 여행기로 가족에게</span></li>
      </ul>
      <p class="fine">KeepTrip은 가이드 점호를 대신하지 않습니다. 인원 확인은 Keep121 Guide와 명찰이 맡고, KeepTrip은 여행객 본인의 정보와 기록을 돕습니다. 화면은 예시입니다. · <a href="keeptrip.html">KeepTrip 자세히</a></p>
    </div>
  </div>
</section>
"""

PROD = f"""
<!-- ============ KEEPTRIP (package mode) ============ -->
<section id="keeptrip">
  <div class="wrap feature-grid">
    {PHONE}
    <div class="feature-copy reveal d1">
      <span class="eyebrow">KeepTrip · Package Mode</span>
      <h2>패키지를 따라가면서도,<br><span class="hl">내 여행은 내가 챙긴다.</span></h2>
      <p class="lede">여행객용 웹앱(PWA)입니다. 투어가 시작되면 여행사가 명단과 함께 보낸 링크로 열고, 귀국 후에는 개인 여행에도 그대로 씁니다.</p>
      <ul class="checks">
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>일정 자동 연동</b> · 여행사 일정과 Guide에서 바꾼 집합 시각·장소</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>도착 해설</b> · 정차지에 도착하면 해설과 꼭 볼 것 3가지</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>자유시간 정보</b> · 집합 장소까지 거리, 주변 식당·화장실·환전</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>보이스 기록</b> · 말로 남기면 장소·음식·동행으로 정리, 사진과 묶음</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>여행 스토리</b> · 귀국 후 Keep Journey 앨범이 내 여행기로, 카카오톡 링크 공유</span></li>
      </ul>
      <p class="fine mt-m">위치는 여행객 본인이 동의한 경우에만, 투어 기간에만 씁니다. 인원 확인은 Guide와 명찰이 맡으며 KeepTrip은 그 기록을 보여줄 뿐 대신하지 않습니다.</p>
    </div>
  </div>
</section>
"""

# solution.html
s = rd("content/pages/solution.html")
if 'id="traveler"' not in s:
    s = put(s, '      <a href="#demo">점호 체험</a>', '      <a href="#traveler">여행객 앱</a>\n', before=True)
    s = put(s, "\n<!-- ============ DEMO ============ -->", SOL, before=True)
    wr("content/pages/solution.html", s)

# product.html
p = rd("content/pages/product.html")
if 'id="keeptrip"' not in p:
    p = put(p, '      <a href="#tag">명찰 · 단말</a>', '      <a href="#keeptrip">여행객 앱</a>\n', before=True)
    p = put(p, '          <tr><th scope="row">Console / HQ</th>',
            '          <tr><th scope="row">KeepTrip</th><td>여행객 웹앱(설치 없음). 패키지 일정 따라가기, 도착 해설, 보이스 기록, 여행 스토리. 귀국 후 개인 여행에도 사용</td><td><span class="lbl plan">콘셉트 · 2027 베타</span></td></tr>\n', before=True)
    p = put(p, "\n<!-- ============ TAG / CHECK ============ -->", PROD, before=True)
    p = put(p, "경보 튜닝 v2 (라벨 데이터 기반 정차지 유형별 규칙), 명단 CSV 표준", ", KeepTrip 패키지 모드 베타")
    wr("content/pages/product.html", p)

# index.html: 제품 구성 넷 → 다섯
h = rd("content/pages/index.html")
if 'href="keeptrip.html"><span class="ic">' not in h:
    h = h.replace("네 가지 구성이 하나의 흐름으로 움직입니다.", "다섯 가지 구성이 하나의 흐름으로 움직입니다.", 1)
    card = ('\n      <a class="prod reveal d4" href="keeptrip.html"><span class="ic"><svg class="icon"><use href="#i-pin"/></svg></span>'
            '<span class="role">Traveler App</span><h3>KeepTrip</h3><p>여행객용 링크 앱. 패키지 일정을 따라가며 해설을 듣고, 말로 기록하고, 귀국 후 여행기로 나눕니다.</p>'
            '<span class="lbl plan">콘셉트 · 2027</span></a>')
    h = put(h, "사람이 확인한 사실만 보냅니다.</p><span class=\"lbl goal\">MVP · 도착 확인 1종</span></a>", card)
    wr("content/pages/index.html", h)

# CSS
css = rd("assets/css/style.css")
if "/* 제품 5종 그리드 */" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n/* 제품 5종 그리드 */\n@media (min-width: 1101px) { .products:has(> .prod:nth-child(5)):not(.kt-features) { grid-template-columns: repeat(5, minmax(0, 1fr)); } }\n")
print("KeepTrip → 솔루션·제품 반영 완료", file=sys.stderr)
