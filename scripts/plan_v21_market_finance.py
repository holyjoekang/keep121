"""사업계획서 v2.1에 새 TAM·SAM·SOM과 손익을 반영한다. 다시 돌려도 안전.

    python scripts/update_market_targets.py && python scripts/update_pnl.py && python scripts/plan_v21_market_finance.py

- data/market.json · data/pnl.json 을 읽어
- data/modoo.json            planV21(v2.0 → v2.1 대조·장별 문안) · planSteps · log 갱신
- content/pages/modoo.html   #plan 에 [data-modoo="planV21"] 자리
- assets/js/modoo.js         planV21 렌더러 (scripts/modoo_plan_v21.js 조각을 끼움)
- docs/사업계획서_v2.1_시장·재무.md  사업계획서 본문에 붙여 넣을 장별 문안
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
M, P = json.loads(rd("data/market.json")), json.loads(rd("data/pnl.json"))
yrs = {r["y"]: r for r in M["years"]}
sam, tam = M["samTotal"], M["tam"]
pr = {r[0]: r[1] for r in P["rows"]}
Y = P["years"]
col = lambda name: dict(zip(Y, pr[name]))  # noqa: E731
rev, op, ebitda = col("매출 합계"), col("영업이익"), col("EBITDA")
s3, s5 = yrs["2029"]["rev"], yrs["2031"]["rev"]
people = next(f for f in M["funnel"] if f[0] == "사람")[2]

compare = [
 ["TAM", "450~540억 원 (해외 패키지 송출 × 8,900원)", f"약 {tam:,}억 원 (사람 {people.replace('약 ', '')} + 자산 추적 {M['asset']['lo']:,}~{M['asset']['hi']:,}억 원)"],
 ["SAM", "70~110억 원 (시니어 중심 중소 여행사)", f"약 {sam:,}억 원 (Guide 학교·시니어 여행·돌봄 + Track 렌털·수하물)"],
 ["SOM", "2031년 12.85억 원 (SAM의 9~13%)", f"3년차 2029년 {s3:g}억 원 · 5년차 2031년 {s5:g}억 원 (SAM의 {s3/sam*100:.1f}% · {s5/sam*100:.1f}%)"],
 ["수익모델", "1인 1회 렌탈 8,900원 단일", "Guide 행사·여행 이용료 + Track 자산 구독(월 2,000원/점) + Enterprise 구축·SaaS"],
 ["2027 매출", "1.8억 원", f"{rev['2027']:g}억 원 (유료 기관 10곳 · 렌털사 PoC 2곳)"],
 ["손익분기", "EBITDA 2030 · 영업이익 2031 (+0.73억)", f"EBITDA {P['breakeven']['ebitda']} · 영업이익 {P['breakeven']['op']} ({op['2031']:+g}억)"],
 ["자금", "1년차 7,500만 원 (정부지원 67%·매출 20%·자본금 13%) · 5년 기본 경로 11.52억 원", f"기본 경로 {P['fundingTotal']}억 원 (보조금·R&D·지분 {P['grantEquity']} / 보증·리스 {P['debt']}) · 2027년 2.0억 원"],
]
som_check = [
 ["멘토 기준 3년차 3%", f"{sam*.03:.1f}억 원", f"v2.1 계획 {s3:g}억 원 ({s3/sam*100:.1f}%)"],
 ["멘토 기준 5년차 5%", f"{sam*.05:.1f}억 원", f"v2.1 계획 {s5:g}억 원 ({s5/sam*100:.1f}%)"],
]
som_note = "v2.0은 SAM의 9~13%로 과대했고, v2.1은 기준(3%·5%)보다 보수적으로 잡았습니다. 초기 3개 시장(단체여행·교육, 장비 렌털, 공항 수하물)에서 단계적으로 검증한 뒤 상향합니다."

chapters = [
 ["1.2 목표 시장 분석 — TAM·SAM·SOM", [
   f"TAM 약 {tam:,}억 원: 국내 단체이동(학교 체험학습·수학여행, 통학, 해외·국내 단체여행, 돌봄기관) {people.replace('약 ', '')}과 자산 이동관리(장비·수하물 추적) {M['asset']['lo']:,}~{M['asset']['hi']:,}억 원의 합.",
   f"SAM 약 {sam:,}억 원: 기관이 결제하는 초기 진입 시장 — " + ", ".join(f"{n} {v:,}억" for n, _, v in M["sam"]) + ".",
   f"SOM: 3년차(2029) {s3:g}억 원, 5년차(2031) {s5:g}억 원 — SAM의 {s3/sam*100:.1f}%·{s5/sam*100:.1f}%로 멘토 기준(3%·5%)보다 보수적.",
   "근거: 2025 교육기본통계(초중고 501만 명), 2025 국민여행조사(국내여행 3.09억 회·여행사 상품 2.8%), 어린이 통학버스 8.6만 대, 노인의료복지시설 6,211곳, 글로벌 자산 추적 시장 184~278억 달러. 단가와 Track 자산 수는 가정이며 인터뷰로 검증."]],
 ["3.1 수익모델", [
   "Keep121 Guide: 행사·여행 단위 이용료 (1인 1회 2,000원, 해외 패키지 9,000원 수준)",
   "Keep121 Track: 자산 수량 기반 구독 (태그 1점 월 2,000원, 수하물 1건 1,000원)",
   "Keep121 Enterprise: 기업별 구축비 + SaaS (통합 관제·API)",
   "공통 기반기술 Keep121 Sensing(위치 오차 보정·센서 최적 조합) 위에서 세 상품을 운영"]],
 ["3.2 연도별 목표 (2027~2031)", [
   " → ".join(f"{y} {rev[y]:g}억" for y in Y) + " 원",
   "Guide 고객 " + " → ".join(f"{yrs[y]['gc']}" for y in Y) + ", Track 관리 자산 " + " → ".join(f"{yrs[y]['assets']:,}점" for y in Y),
   "인원 " + " → ".join(f"{yrs[y]['team']}명" for y in Y) + ", 각 단계는 Gate 0~3 통과 시에만 채용·투자 확대"]],
 ["3.3 추정 손익", [
   "영업이익 " + ", ".join(f"{y} {op[y]:+g}억" for y in Y),
   f"EBITDA 흑자 {P['breakeven']['ebitda']}년, 영업이익 흑자 {P['breakeven']['op']}년 · 누적 현금 최저 {P['breakeven']['trough']}억 원(조달 전)",
   "가정: 공헌이익률 Guide 55→75%, Track 45→70%, Enterprise 40→55% · Track 태그 1점 2.5만 원, 3년 감가"]],
 ["3.4 자금 조달", [
   f"기본 경로 {P['fundingTotal']}억 원 — 보조금·R&D·지분 {P['grantEquity']}억, 기보 보증·태그 리스 {P['debt']}억 (자산이 남는 Track 태그 투자분)",
   "2027년: 자본금 0.3억 + 창업패키지 0.7억 + 기보·중진공 1.0억 = 2.0억 원",
   f"2031년 말 잔액 약 {P['buffer']}억 원 · Gate 1 미달 시 '보수 + 고정비 동결' 경로"]],
]
v21 = {
 "title": "사업계획서 v2.1 · 시장 규모와 손익 반영",
 "lead": "웹사이트에 반영한 TAM·SAM·SOM(data/market.json)과 손익표(data/pnl.json)를 PSST 1.2장·3장에 옮깁니다. 아래 문안은 같은 데이터에서 생성합니다.",
 "compare": compare, "somCheck": som_check, "somNote": som_note, "chapters": chapters,
 "doc": "docs/사업계획서_v2.1_시장·재무.md",
 "note": "모든 수치는 추정·목표이며 실적이 아닙니다. 고객 인터뷰 등 가정값 교체는 별도 과제입니다.",
}

d = json.loads(rd("data/modoo.json"))
d["planV21"] = v21
for s in d["planSteps"]:
    if s["step"] == "아이디어 진단 반영":
        s["basis"] = "사업계획서 v2.0(10/29) + 멘토링 1회차 피드백 · TAM·SAM·SOM·손익 v2.1 반영(11/12)"
d["log"] = [l for l in d["log"] if not (l["date"] == "2026-11-12" and l["kind"] == "사업계획서")]
d["log"].insert(0, {"date": "2026-11-12", "kind": "사업계획서", "title": "v2.1 시장 규모·손익 반영",
   "text": f"피드백 ⑥(SOM 재산정) 반영. TAM 약 {tam:,}억 · SAM 약 {sam:,}억 · SOM 2029년 {s3:g}억·2031년 {s5:g}억 원, 영업이익 흑자 {P['breakeven']['op']}년, 조달 {P['fundingTotal']}억 원."})
wr("data/modoo.json", json.dumps(d, ensure_ascii=False, indent=1) + "\n")

pg = rd("content/pages/modoo.html")
if 'data-modoo="planV21"' not in pg:
    a = pg.index('<tbody data-modoo="planSteps"></tbody>')
    b = pg.index("</div>", a) + len("</div>")
    pg = pg[:b] + '\n    <div data-modoo="planV21" class="mt-l"></div>' + pg[b:]
    wr("content/pages/modoo.html", pg)

js = rd("assets/js/modoo.js")
frag = rd("scripts/modoo_plan_v21.js").rstrip() + "\n"
js = re.sub(r"    planV21: .*?\n(?=    sessions:)", "", js, flags=re.S)
js = js.replace("    sessions: m =>", frag + "    sessions: m =>", 1)
wr("assets/js/modoo.js", js)

md = [f"# {v21['title']}", "", f"> {v21['lead']} {v21['note']}", "", "## v2.0 → v2.1 대조", "", "| 항목 | v2.0 | v2.1 |", "|---|---|---|"]
md += [f"| {a} | {b} | {c} |" for a, b, c in compare]
md += ["", "## SOM 점검 (멘토 피드백 ⑥)", "", "| 기준 | SAM 기준 금액 | v2.1 |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in som_check] + ["", som_note, ""]
for t, items in chapters:
    md += [f"## {t}", ""] + [f"- {x}" for x in items] + [""]
md += ["## 추정 손익표 (억 원)", "", "| 항목 | " + " | ".join(Y) + " |", "|---|" + "---|" * len(Y)]
md += [f"| {l} | " + " | ".join(str(v) for v in vals) + " |" for l, vals, _ in P["rows"]]
md += ["", "## 출처", ""] + [f"- {a} — {b}" + (f" ({u})" if u else "") for a, b, u in M["sources"]]
md += ["", f"_생성: scripts/plan_v21_market_finance.py · 기준일 {M['updated']}_", ""]
wr(v21["doc"], "\n".join(md))
print("  modoo.json planV21 · modoo.html · modoo.js ·", v21["doc"])
