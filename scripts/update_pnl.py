"""새 매출 목표(data/market.json)에 맞춘 손익표·시나리오·자금 조달을 계산해 실증 페이지 #finance 에 반영한다.

    python scripts/update_market_targets.py && python scripts/update_pnl.py

- data/pnl.json              가정·연도별 손익·시나리오·자금 조달 (이 스크립트가 계산)
- content/pages/evidence     #finance 본문 → [data-market="pnl"] 자리 (assets/js/market.js 가 그림)
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
M = json.loads(rd("data/market.json"))
yrs = [r for r in M["years"] if r["y"].isdigit()]          # 2027~2031
Y = [r["y"] for r in yrs]

A = {  # 가정
 "cm": {"g": [.55, .65, .70, .72, .75], "t": [.45, .58, .65, .68, .70], "e": [.40, .40, .45, .50, .55]},
 "pay": [.30, .45, .50, .52, .55],          # 1인 연 인건비 (억 원, 4대보험 포함)
 "other": [.30, .45, .60, .75, .90],        # 기타 고정비: 임차·클라우드·보험·인증·마케팅
 "tag": 2.5e4, "replace": .15,              # 태그 1점 원가(원) · 연 교체율
 "kit": .02,                                # Guide 신규 고객당 공용 키트 (억 원)
 "nre": [.1, .3, .3, .1, .1],               # 개발·인증 NRE (억 원)
 "life": 3, "ar_days": 45,
}
FREEZE = [2, 3, 4, 5, 6]

def run(k=1.0, freeze=False):
    rows, caps, cash, mn, pa, pc, pr = [], [], 0.0, 0.0, 0, 0, 0.0
    for i, r in enumerate(yrs):
        R = {p: r[p] * k for p in "gte"}
        tot = sum(R.values())
        C = sum(R[p] * A["cm"][p][i] for p in R)
        a, c = r["assets"] * k, int(re.sub(r"\D", "", r["gc"]) or 0) * k
        team = min(r["team"], FREEZE[i]) if freeze else r["team"]
        fixed = team * A["pay"][i] + A["other"][i]
        capex = max(a - pa, 0) * A["tag"] / 1e8 + pa * A["replace"] * A["tag"] / 1e8 + max(c - pc, 0) * A["kit"] + A["nre"][i]
        caps.append(capex)
        dep = sum(caps[max(0, i - A["life"] + 1):i + 1]) / A["life"]
        ebitda = C - fixed
        cash += ebitda - capex - (tot - pr) * A["ar_days"] / 365
        mn = min(mn, cash)
        rows.append(dict(y=r["y"], g=R["g"], t=R["t"], e=R["e"], rev=tot, var=tot - C, cm=C, cmr=C / tot if tot else 0, fixed=fixed,
                         ebitda=ebitda, dep=dep, op=ebitda - dep, capex=capex, cash=cash, team=team, assets=a))
        pa, pc, pr = a, c, tot
    return rows, mn

base, trough = run()
first = lambda rows, key: next((r["y"] for r in rows if r[key] > 0), "5년 안 안 됨")  # noqa: E731
scen = []
for name, k, fz in [("보수", .6, False), ("보수 + 고정비 동결", .6, True), ("기본", 1.0, False), ("공격", 1.5, False)]:
    rows, mn = run(k, fz)
    last = rows[-1]
    scen.append([name, f"{k:g}배", f"{last['rev']:.2f}억", first(rows, "ebitda"), first(rows, "op") + (f" ({last['op']:+.2f}억)" if last["op"] > 0 else ""), f"{mn:.2f}억"])

funding = [["2026 Q4", "모두의 창업 활동자금", .02, "파일럿·인터뷰"], ["2027 Q1", "창업자 자본금", .3, "법인 설립"],
           ["2027 상반기", "예비·초기창업패키지 (자격 확인 필요)", .7, "Guide·콘솔, 동의 UX, 배상보험"], ["2027 하반기", "기보 기술보증 + 중진공 창업기반자금", 1.0, "태그·키트 초도분, 운전자본"],
           ["2028", "엔젤·TIPS 운영사 투자 (Gate 1 통과 시)", 2.5, "인건비·영업"], ["2028~2029", "TIPS R&D (한도 확인 필요)", 5.0, "Track·RFID 게이트·Sensing Fusion"],
           ["2030~2031", "태그 리스 · 기보 추가 보증", 3.5, "Track 자산 증설 (자산 담보)"]]
inflow = {2026: .02, 2027: 2.0, 2028: 5.0, 2029: 2.5, 2030: 2.0, 2031: 1.5}
cum, low, buf = inflow[2026], 1e9, 0
for r in base:
    cum += inflow[int(r["y"])]
    buf = cum + r["cash"]
    low = min(low, buf)
assert low > 0, "자금 조달이 현금 최저점을 메우지 못함"
grant_eq = sum(f[2] for f in funding if "리스" not in f[1] and "기보" not in f[1])
debt = sum(f[2] for f in funding) - grant_eq

R2 = lambda v: round(v, 2)  # noqa: E731
P = {
 "updated": M["updated"],
 "lead": f"새 매출 목표(2027년 {base[0]['rev']:g}억 → 2031년 {base[-1]['rev']:g}억 원)에 맞춘 기본 시나리오입니다. 공헌이익률은 상품별 가정, 고정비는 인원 계획, 감가는 Track 태그·Guide 키트 투자({A['life']}년 정액)에서 계산했습니다. 모든 수치는 가정입니다.",
 "years": Y,
 "rows": [
  ["Guide 매출", [R2(r["g"]) for r in base], ""], ["Track 매출", [R2(r["t"]) for r in base], ""], ["Enterprise 매출", [R2(r["e"]) for r in base], ""],
  ["매출 합계", [R2(r["rev"]) for r in base], "total"],
  ["변동원가 (통신·서버·CS·구축)", [R2(r["var"]) for r in base], ""], ["공헌이익률", [f"{r['cmr']:.0%}" for r in base], ""],
  ["고정비 (인건비 + 기타)", [R2(r["fixed"]) for r in base], ""], ["EBITDA", [R2(r["ebitda"]) for r in base], "total"],
  ["감가상각", [R2(r["dep"]) for r in base], ""], ["영업이익", [R2(r["op"]) for r in base], "total"],
  ["capex (태그·키트·NRE)", [R2(r["capex"]) for r in base], ""], ["누적 현금흐름 (조달 전)", [R2(r["cash"]) for r in base], ""],
  ["인원 (명)", [r["team"] for r in base], ""], ["Track 관리 자산 (점)", [int(r["assets"]) for r in base], ""],
 ],
 "chart": [[r["y"], R2(r["g"]), R2(r["t"]), R2(r["e"]), R2(r["op"])] for r in base],
 "assumptions": [
  ["공헌이익률", "Guide 55%→75%, Track 45%→70%, Enterprise 40%→55% (규모에 따라 개선)"],
  ["인건비", f"1인 연 {A['pay'][0]}억(2027) → {A['pay'][-1]}억 원(2031), 인원 2 → 10명"],
  ["기타 고정비", f"연 {A['other'][0]}억 → {A['other'][-1]}억 원 (임차·클라우드·보험·인증·마케팅)"],
  ["Track 태그", f"1점 {A['tag']/1e4:g}만 원, 연 교체율 {A['replace']:.0%}, 구독 월 2,000원 → 회수 약 1.5년"],
  ["Guide 키트·NRE", f"신규 고객당 공용 키트 {A['kit']*1e4:,.0f}만 원, 개발·인증 NRE 연 0.1~0.3억 원"],
  ["운전자본", f"매출채권 {A['ar_days']}일"],
 ],
 "breakeven": {"ebitda": first(base, "ebitda"), "op": first(base, "op"), "trough": R2(trough)},
 "scenarios": scen,
 "scenarioNote": "보수는 매출·자산 목표의 60%, 공격은 150%입니다. 보수 시나리오에서 인원을 계획대로 늘리면 자금 소요가 가장 커지므로, 관문 미달 시 인원을 2→6명으로 묶는 '고정비 동결'을 규칙으로 둡니다.",
 "funding": [[a, b, c, d] for a, b, c, d in funding],
 "fundingTotal": R2(sum(f[2] for f in funding)), "grantEquity": R2(grant_eq), "debt": R2(debt), "buffer": R2(buf), "low": R2(low),
 "fundingNote": f"누적 현금 최저점 {trough:.2f}억 원 가운데 보조금·R&D·지분으로 {grant_eq:.2f}억 원, 자산이 남는 Track 태그 투자분은 기보 보증·리스 {debt:.2f}억 원으로 메웁니다. 2031년 말 잔액 약 {buf:.2f}억 원. Gate 1 미달 또는 2027년 9월까지 CTO 미확보 시 시드 투자를 시도하지 않고 '보수 + 동결' 경로로 갑니다. 지원사업 한도와 금리는 공고문으로 확인할 추정치입니다.",
 "previous": "이전 여행사 단일 시장 계획(2031년 매출 12.85억, 영업이익 +0.73억, 조달 11.52억 원)을 대체합니다.",
}
wr("data/pnl.json", json.dumps(P, ensure_ascii=False, indent=1) + "\n")

e = rd("content/pages/evidence.html")
m = re.search(r'<section class="soft" id="finance">\s*<div class="wrap">\s*<div class="head reveal">.*?</div>', e, flags=re.S)
end = e.index("</div>\n</section>", m.end())
head = ('<section class="soft" id="finance">\n  <div class="wrap">\n    <div class="head reveal">\n'
        '      <span class="eyebrow">Financial Plan · 2027~2031</span>\n'
        '      <h2>새 매출 목표에 맞춘<br><span class="hl">손익과 자금 계획.</span></h2>\n'
        '      <p>Guide·Track·Enterprise 매출 목표에서 출발해 공헌이익, 고정비, 태그 투자와 감가, 현금 최저점까지 계산합니다. 모든 수치는 가정이며 실적이 아닙니다.</p>\n    </div>')
e = e[:m.start()] + head + '\n    <div data-market="pnl"></div>\n  ' + e[end:]
e = re.sub(r'<p class="notice mt-s" data-market-note>.*?</p>\n', "", e, flags=re.S)
e = re.sub(r"(아래 재무표는 여행사 단일 시장 기준의 이전 가정입니다\.|손익분기 목표는 [^.]*입니다\.) ?", "", e)
e = e.replace("합계, 목표). ", f"합계, 목표). 손익분기 목표는 EBITDA {P['breakeven']['ebitda']}년, 영업이익 {P['breakeven']['op']}년입니다. ", 1)
e = re.sub(r'<div><b>2031</b><span>영업이익 흑자 목표</span></div>', f'<div><b>{P["breakeven"]["op"]}</b><span>영업이익 흑자 목표</span></div>', e)
wr("content/pages/evidence.html", e)
print(f"  EBITDA 흑자 {P['breakeven']['ebitda']} · 영업이익 흑자 {P['breakeven']['op']} · 현금 최저 {trough:.2f}억 · 조달 {P['fundingTotal']}억 (보조금·지분 {grant_eq:.2f} / 부채 {debt:.2f}) · 잔액 {buf:.2f}억 · 최저 잔액 {low:.2f}억")
