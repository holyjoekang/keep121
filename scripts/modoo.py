"""모두의 창업 진행 상태(data/modoo.json) 갱신. 실행할 때마다 updated 날짜를 오늘로 바꾼다.

  python scripts/modoo.py log 2026-10-27 제출 "서약서 2종 제출" "부가세 미환급·청렴윤리 서약서 PDF 회신"
  python scripts/modoo.py expense 2026-11-03 "① 재료구입비" "NFC 태그 30개" 45000 "카드 승인내역"
  python scripts/modoo.py status "10/27(화) 16:00" done        # 일정 상태: done|due|check|plan (when 앞부분으로 찾음)
  python scripts/modoo.py mentoring 1 "2026-11-02 · 온라인" "목표 고객을 시니어 전문 중소 여행사로 좁힘"
  python scripts/modoo.py ai 1개월차 "솔루션 이름" 300000 "고객 인터뷰 분석"
  python scripts/modoo.py plan "양식 확인" done                 # 사업계획서 단계 상태
  python scripts/modoo.py mentor "OOO 멘토(소속) · 11/2 첫 미팅"
  python scripts/modoo.py sched "10/29(목)" "멘토링 1회차" "이광일 멘토" plan "10/27"   # 일정 추가 (마지막 인자: 이 when 뒤에 넣음)
  python scripts/modoo.py now 3 "멘토링 1회차" "일자=10/29(목);멘토=이광일" "설명"      # '지금 할 일' n번째 카드 교체
"""
import datetime as dt, json, sys
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "data/modoo.json"
m = json.loads(F.read_text(encoding="utf-8"))
cmd, *a = sys.argv[1:] or ["help"]
pick = lambda rows, k, v: next(r for r in rows if r[k].startswith(v))  # noqa: E731

if cmd == "log":
    m["log"].insert(0, dict(zip(["date", "kind", "title", "text"], a)))
    m["log"].sort(key=lambda r: r["date"], reverse=True)
elif cmd == "expense":
    date, cat, desc, amount, proof = (a + [""])[:5]
    m["expenses"].append({"date": date, "cat": cat, "desc": desc, "amount": int(amount), "proof": proof})
    m["expenses"].sort(key=lambda r: r["date"])
elif cmd == "status":
    r = pick(m["schedule"], "when", a[0]); r["status"] = a[1]; r.pop("label", None)
    if len(a) > 2: r["label"] = a[2]
elif cmd == "mentoring":
    r = next(r for r in m["mentoring"] if r["n"] == int(a[0])); r["date"] = a[1]
    if len(a) > 2: r["result"] = a[2]
elif cmd == "ai":
    pick(m["ai"], "round", a[0])["solutions"].append({"name": a[1], "amount": int(a[2]), "purpose": a[3] if len(a) > 3 else ""})
elif cmd == "plan":
    pick(m["planSteps"], "step", a[0])["status"] = a[1]
elif cmd == "sched":
    row = {"when": a[0], "task": a[1], "note": a[2], "status": a[3]}
    i = next((i + 1 for i, r in enumerate(m["schedule"]) if len(a) > 4 and r["when"].startswith(a[4])), len(m["schedule"]))
    m["schedule"].insert(i, row)
elif cmd == "now":
    card = {"title": a[1], "facts": [kv.split("=", 1) for kv in a[2].split(";")], "text": a[3]}
    n = int(a[0]) - 1
    m["now"][n:n + 1] = [card]
elif cmd == "mentor":
    m["mentor"] = a[0]
else:
    sys.exit(__doc__)
m["updated"] = dt.date.today().isoformat()
F.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("갱신:", cmd, m["updated"])
