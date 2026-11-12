"""시장조사 기반 TAM·SAM·SOM과 연도별 목표(2026~2031)를 반영한다. 다시 돌려도 안전.

    python scripts/update_market_targets.py

- data/market.json         계산된 시장 규모·연도별 목표·출처 (이 스크립트가 숫자를 계산)
- assets/js/market.js      [data-market="size|targets|stages"] 자리를 그린다 (render.js 가 자리 있을 때 불러옴)
- content/pages/usecases   #size 본문 → 자리, 확장 경로 단계 → 자리, 머리 수치·안내 문구
- content/pages/evidence   #growth 본문 → 자리, 기존 재무 섹션에 '이전 계획' 안내
- content/pages/index      Explore 시장 카드 수치
"""
import datetime as dt, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")
EOK = 1e8  # 억 원

# ---- 확인된 수치 ----
students = 2_345_488 + 1_370_356 + 1_299_466      # 2025 초·중·고 (교육기본통계)
buses = 86_416                                     # 어린이 통학버스 신고 (2024.8)
outbound_pkg = 5_500_000                           # 해외 패키지 송출 연 500~600만 명 (기존 추정 중간값)
dom_trips, agency_rate = 309_000_000, 0.028        # 2025 국내여행 3.09억 회 · 여행사 상품 2.8%
elder_fac = 6_211                                  # 2025 노인의료복지시설
at_lo, at_hi, kr_share, fx = 18.4e9, 27.8e9, 0.017, 1400   # 글로벌 자산추적 2025 · 한국 비중 가정 · 환율

# ---- 단가 가정 (원) ----
P = dict(trip=2000, bus_m=20000, pkg=9000, elder_m=50000, asset_m=2000, bag=1000)

people = [
 ["초중고 현장체험학습·수학여행", f"학생 {students/1e4:,.0f}만 명 × 연 2회 × {P['trip']:,}원", students * 2 * P['trip'], "Guide", True],
 ["해외 단체 패키지 (시니어 포함)", f"연 약 550만 명 × {P['pkg']:,}원", outbound_pkg * P['pkg'], "Guide", False],
 ["어린이집·유치원 통학", f"통학버스 {buses/1e4:.1f}만 대 × 월 {P['bus_m']:,}원 × 12", buses * P['bus_m'] * 12, "Guide", False],
 ["국내 여행사 상품 여행", f"국내여행 3.09억 회 × 여행사 상품 2.8% × {P['trip']:,}원", dom_trips * agency_rate * P['trip'], "Guide", False],
 ["돌봄기관 외부활동·송영", f"노인의료복지시설 {elder_fac:,}곳 × 월 {P['elder_m']:,}원 × 12", elder_fac * P['elder_m'] * 12, "Guide", True],
]
asset_lo, asset_hi = at_lo * kr_share * fx, at_hi * kr_share * fx
asset_mid = (asset_lo + asset_hi) / 2
people_tam = sum(r[2] for r in people)
tam = people_tam + asset_mid

senior_sam = 90 * EOK  # 시니어 중심 중소 여행사 (기존 추정 70~110억 중간값)
rental_assets = 1_500_000
sam_rows = [
 ["Guide · 학교 체험학습·수학여행", "교육청·학교 결제, 2026학년도 운영 매뉴얼로 수요 근거", people[0][2]],
 ["Guide · 시니어 중심 중소 여행사", "기존 추정 70~110억 원의 중간값", senior_sam],
 ["Guide · 돌봄기관", "노인의료복지시설 외부활동·송영", people[4][2]],
 ["Track · 이동형 렌털 자산", f"IT·AV·전시·계측·의료기기 약 {rental_assets/1e4:.0f}만 점(가정) × 월 {P['asset_m']:,}원 × 12", rental_assets * P['asset_m'] * 12],
 ["Track · 공항·호텔 수하물", f"배송 연 약 100만 건(가정) × {P['bag']:,}원", 1_000_000 * P['bag']],
]
sam = sum(r[2] for r in sam_rows)

# ---- 연도별 목표 (억 원 · 기관 수 · 관리 자산) ----
years = [
 dict(y="2026 Q4", stage="검증", g=0, t=0, e=0, gc="인터뷰 8곳", tc="PoC 제안 2곳", assets=0, team=1,
      items=["렌털 5곳 · 단체여행·교육 3곳 인터뷰", "SmartTag3 + QR 수동 실증", "유료 PoC 의향 1~2곳 선정"], gate="Gate 0 · 문제 비용·지불 의사 확인"),
 dict(y="2027", stage="유료 PoC", g=0.15, t=0.10, e=0, gc="유료 기관 10곳", tc="렌털사 2곳", assets=300, team=2,
      items=["법인 설립 · 위치기반서비스 신고", "Guide 학교·여행사 유료 전환", "렌털 장비 30~50대 회수관리 PoC", "GPS 선택 적용"], gate="Gate 1 · 유료 고객 10곳 + Track 재계약"),
 dict(y="2028", stage="Track 상용화", g=0.8, t=0.7, e=0, gc="30곳", tc="5곳", assets=2000, team=4,
      items=["Track 자산 구독 정식 출시", "능동형 RFID 게이트 (전시·행사)", "수하물 배송 운영사 연동 PoC", "TIPS · 시드"], gate="Gate 2 · 자산 2,000점, 월 이탈률 3% 이하"),
 dict(y="2029", stage="Enterprise", g=2.0, t=2.2, e=0.5, gc="60곳", tc="12곳", assets=8000, team=6,
      items=["Enterprise 관제·API 첫 구축", "교육청 단위 체험학습 실증", "Sensing Fusion 엔진 v1"], gate="Gate 3 · 반복매출 비중 50%"),
 dict(y="2030", stage="확장", g=3.5, t=4.5, e=1.0, gc="100곳", tc="25곳", assets=18000, team=8,
      items=["의료기기·IT 렌털로 확대", "EBITDA 손익분기 목표", "개인위치정보사업 등록"], gate=""),
 dict(y="2031", stage="규모화", g=5.5, t=7.5, e=2.0, gc="150곳", tc="40곳", assets=30000, team=10,
      items=["SAM 점유 약 2%", "영업이익 흑자 전환 목표", "해외 라이선스는 국내 관문 통과 후 검토"], gate=""),
]
for r in years:
    r["rev"] = round(r["g"] + r["t"] + r["e"], 2)
som29 = next(r for r in years if r["y"] == "2029")["rev"]
som31 = years[-1]["rev"]

ok = lambda v: round(v / EOK)  # noqa: E731
M = {
 "updated": "2026-11-12",
 "basis": "연간 매출 잠재력(원). 공식 통계에서 시작해 단가 가정으로 환산한 추정이며, 인터뷰·PoC로 다시 검증합니다.",
 "funnel": [
  ["TAM", "국내 사람·자산 이동관리", f"약 {ok(tam):,}억 원", f"사람 {ok(people_tam):,}억 + 자산 추적 {ok(asset_lo):,}~{ok(asset_hi):,}억(중간값 {ok(asset_mid):,}억)"],
  ["사람", "Guide 대상 단체이동", f"약 {ok(people_tam):,}억 원", "학교·통학·여행·돌봄 5개 영역 합계"],
  ["SAM", "초기 3개 시장 + 인접", f"약 {ok(sam):,}억 원", "Guide 학교·시니어 여행·돌봄 + Track 렌털·수하물"],
  ["SOM", "2031 목표", f"{som31:g}억 원", f"SAM의 약 {som31 / ok(sam) * 100:.1f}% · 2029년 {som29:g}억 원({som29 / ok(sam) * 100:.1f}%)"],
 ],
 "people": [[n, f, ok(v), s, sam_in] for n, f, v, s, sam_in in people],
 "asset": {"lo": ok(asset_lo), "hi": ok(asset_hi), "mid": ok(asset_mid),
   "formula": f"글로벌 자산 추적 시장 2025년 {at_lo/1e9:.1f}~{at_hi/1e9:.1f}B 달러 × 한국 비중 {kr_share*100:.1f}%(GDP 비중 가정) × {fx:,}원"},
 "sam": [[n, b, ok(v)] for n, b, v in sam_rows], "samTotal": ok(sam), "tam": ok(tam),
 "prices": [["Guide 단체이동", f"1인 1회 {P['trip']:,}원 (해외 패키지 {P['pkg']:,}원)"], ["통학 모드", f"차량당 월 {P['bus_m']:,}원"], ["돌봄기관", f"기관당 월 {P['elder_m']:,}원"], ["Track", f"자산 1점당 월 {P['asset_m']:,}원 · 수하물 1건 {P['bag']:,}원"]],
 "years": years,
 "change": "이전 계획(2031년 매출 12.85억 원, 여행사 단일 시장)과 확장 TAM 2,600억·SAM 890억 원 추정을 이 수치로 대체합니다. SOM은 Track 자산 구독이 더해져 2031년 15억 원으로 상향하되, 점유율 가정은 3~5%에서 약 2%로 낮췄습니다.",
 "sources": [
  ["2025 유·초·중·고 학생 555만 명 (초 234.5만·중 137.0만·고 129.9만)", "교육부 2025 교육기본통계 · 아시아경제", "https://view.asiae.co.kr/article/2025082809583626415"],
  ["2025 국내여행 3.09억 회 · 지출 39.5조 원", "문체부 2025 국민여행조사 · 뉴데일리", "https://www.newdaily.co.kr/site/data/html/2026/06/30/2026063000117.html"],
  ["국내 관광여행 중 여행사 상품 구매 2.8%", "2025 국민여행조사 · 세계일보", "https://www.segye.com/newsView/20260630515634"],
  ["2025 국민 출국자 약 2,958만 명", "헤럴드경제", "https://www.heraldk.com/article/2026012722573312289"],
  ["60대 해외여행자의 패키지 이용 63.3%", "오픈서베이", "https://blog.opensurvey.co.kr/trendreport/overseas-travel-2025/"],
  ["어린이 통학버스 신고 8만 6,416대 (2024.8)", "경찰청 자료 · 국회 의원실 (원문 확인 필요)", ""],
  ["2025 노인의료복지시설 6,211개소", "e-나라지표", "https://www.index.go.kr/unify/idx-info.do?idxCd=2766"],
  ["글로벌 자산 추적 시장 2025년 18.4~27.8B 달러", "Datahorizzon · Fortune Business Insights 외", "https://www.fortunebusinessinsights.com/index.php/asset-tracking-markt-109490"],
 ],
 "gaps": "국내 B2B 장비 렌털 자산 수, 전시회 개최 건수, 공항 수하물 배송 건수는 공개 통계를 찾지 못해 가정으로 두었습니다. 렌털사·배송 운영사 인터뷰에서 먼저 확인합니다."
}
wr("data/market.json", json.dumps(M, ensure_ascii=False, indent=1) + "\n")
wr("assets/js/market.js", rd("scripts/market.js"))

def mount(t, start_re, end_marker, key):
    """start_re 섹션의 head 다음부터 end_marker 앞까지를 자리로 바꾼다."""
    m = re.search(start_re, t, flags=re.S)
    a = m.end()
    b = t.index(end_marker, a)
    return t[:a] + f'\n    <div data-market="{key}"></div>\n  ' + t[b:]

u = rd("content/pages/usecases.html")
if 'data-market="size"' not in u:
    u = mount(u, r'<section class="soft" id="size">\s*<div class="wrap">\s*<div class="head reveal">.*?</div>', "</div>\n</section>", "size")
if 'data-market="stages"' not in u:
    a = u.index('<div class="stages">', u.index('id="expansion"'))
    b = u.index("</section>", a)
    u = u[:a] + '<div data-market="stages"></div>\n  </div>\n' + u[b:]
u = re.sub(r'<h2>확인된 수치와 추정을<br><span class="hl">나눠서 봅니다.</span></h2>', '<h2>사람과 자산의 이동,<br><span class="hl">통계에서 출발해 좁힙니다.</span></h2>', u)
u = re.sub(r'<div><b>80~120<small>만 명</small></b><span>연간 SAM \(추정\)</span></div><div><b>9~13<small>%</small></b><span>2031 SAM 점유 \(기본\)</span></div>',
           f'<div><b>{M["samTotal"]:,}<small>억 원</small></b><span>연간 SAM (추정)</span></div><div><b>{som31:g}<small>억 원</small></b><span>2031 SOM 목표</span></div>', u)
u = re.sub(r'(<b>2026\.11 확장 사업계획</b> · )확장 시장은.*?(<a href="operations\.html#scenarios">)',
           lambda m: m.group(1) + f'Guide(사람)와 Track(자산)을 합친 국내 TAM은 약 {M["tam"]:,}억 원, 초기 진입 SAM은 약 {M["samTotal"]:,}억 원으로 다시 추정했습니다. SOM 목표는 2029년 {som29:g}억 원, 2031년 {som31:g}억 원입니다. <a href="#size">시장 규모 보기</a> · ' + m.group(2), u, flags=re.S)
u = re.sub(r'새 계획\(SAM 약 [^)]*\)', f'새 계획(SAM 약 {M["samTotal"]:,}억 원)', u)
wr("content/pages/usecases.html", u)

e = rd("content/pages/evidence.html")
if 'data-market="targets"' not in e:
    e = mount(e, r'<section id="growth">\s*<div class="wrap">\s*<div class="head reveal">.*?</div>', "</div>\n</section>", "targets")
e = e.replace('<h2>관문에 미달하면<br><span class="hl">채용과 투자를 멈춥니다.</span></h2>', '<h2>연도별 목표,<br><span class="hl">관문에 미달하면 멈춥니다.</span></h2>')
e = e.replace("<p>각 단계는 앞 관문을 통과해야 채용과 단말 투자를 시작합니다.", "<p>2026.11 B2B 확장 전략(Guide·Track·Enterprise)에 맞춰 다시 세운 목표입니다. 각 단계는 앞 관문을 통과해야 채용과 단말 투자를 시작합니다.")
note = '<p class="notice mt-s" data-market-note><span><b>이전 계획</b> · 아래 재무표는 여행사 단일 시장 기준의 이전 가정입니다. 현재 연도별 매출 목표는 <a href="#growth">성장 로드맵</a>을 따릅니다.</span></p>\n'
e = re.sub(r'<p class="notice mt-s" data-market-note>.*?</p>\n', "", e, flags=re.S)
m = re.search(r'<section class="soft" id="finance">\s*<div class="wrap">\s*<div class="head reveal">.*?</div>\s*', e, flags=re.S)
e = e[:m.end()] + note + e[m.end():]
wr("content/pages/evidence.html", e)

i = rd("content/pages/index.html")
i = re.sub(r'<span class="ex-stat">[^<]*<small>연간 SAM \(추정\)</small>', f'<span class="ex-stat">{M["samTotal"]:,}억 원 <small>연간 SAM (추정)</small>', i)
wr("content/pages/index.html", i)

r = rd("assets/js/render.js")
r = re.sub(r"\n    if \(document\.querySelector\('\[data-market\]'\)\).*", "", r)
r = r.replace("    const pg = s.pages.find(p => p.id === id);",
              f"    if (document.querySelector('[data-market]')) {{ const k = document.createElement('script'); k.src = 'assets/js/market.js?v={V}'; document.body.appendChild(k); }}\n    const pg = s.pages.find(p => p.id === id);", 1)
wr("assets/js/render.js", r)
print(f"  TAM {M['tam']:,}억 · 사람 {ok(people_tam):,}억 · 자산 {ok(asset_lo):,}~{ok(asset_hi):,}억 · SAM {M['samTotal']:,}억 · SOM 2029 {som29}억 / 2031 {som31}억")

# 실증 페이지 머리 수치·안내 문구
e = rd("content/pages/evidence.html")
e = re.sub(r'<div><b>[\d.]+<small>억 원</small></b><span>2031 매출 · [^<]*</span></div>',
           f'<div><b>{som31:g}<small>억 원</small></b><span>2031 매출 목표 · Guide+Track</span></div>', e)
e = re.sub(r'(<b>2026\.11 확장 사업계획</b> · ).*?(<a href="operations\.html#scenarios">)',
           lambda m: m.group(1) + "매출 목표는 " + " → ".join(f"{r['y']}년 {r['rev']:g}억" for r in years[1:]) + " 원입니다(Guide·Track·Enterprise 합계, 목표). 아래 재무표는 여행사 단일 시장 기준의 이전 가정입니다. <a href=\"#growth\">연도별 목표 보기</a> · " + m.group(2), e, flags=re.S)
wr("content/pages/evidence.html", e)
