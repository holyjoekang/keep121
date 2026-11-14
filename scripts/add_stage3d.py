"""포토 스테이지형 1분 3D 제안(제주 · 일산동중 · 사랑글로벌아카데미)을 만든다. 다시 돌려도 안전.

    python scripts/add_stage3d.py

- 엔진: assets/js/stage3d.js (원본 scripts/stage3d.js) + 소리 assets/js/sound3d.js (원본 scripts/sound3d.js)
  각 제안서의 배경 사진 위에 장면별 3D 오브젝트를 올리고
  끌어서 돌리기 · 마우스 설명 · '길 잃은 사람 눌러 찾기' 같은 상호작용과 내레이션 · 배경음을 넣는다.
- WYD(wyd2027-3d.html)도 2026.11 같은 방식으로 바꿨다 (이전 입자형 wyd3d.js · add_wyd3d.py 는 삭제)
- 장면 데이터: data/<id>_stage.json (배경 사진은 각 제안서 data/<deck>.json 의 img 를 그대로 쓴다)
- 페이지: jeju2027-3d.html · ilsandong-3d.html · saga2027-3d.html
- 각 제안서(add_*_proposal.py)에 link3d, 맞춤 제안 카드(add_proposals_page.py)에 '▶ 1분 3D' 링크
"""
import datetime as dt, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")


def sc(bg, k, title, sub, say, obj, dur=7.5, stats=None, hint=None, cta=None):
    s = {"bg": bg, "dur": dur, "k": k, "title": title, "sub": sub, "say": say, "obj": obj}
    if stats: s["stats"] = stats
    if hint: s["hint"] = hint
    if cta: s["cta"] = cta
    return s


DECKS = {
 # ───────────────────────────── WYD 서울 2027 ─────────────────────────────
 "wyd2027": dict(page="wyd2027-3d.html", deck="wyd2027", pages="15장", kicker="WYD Seoul 2027 · Keep121 × Galaxy SmartTag3",
  gate="40만 순례자,<br>한 사람도 놓치지 않는 대회", desc="Keep121 × Galaxy SmartTag3 — 2027 서울 세계청년대회 40만 순례자 안전 · 안내 제안을 60초 인터랙티브 3D로.",
  scenes=[
   sc("hanbok", "WYD Seoul 2027 · 천주교 서울대교구 제안", "전 세계 40만 순례자가<br><em>서울로 옵니다.</em>", "2027년 8월 3일 ~ 8일, 서울 곳곳에서 열리는 세계청년대회.",
      "전 세계 40만 순례자가 서울로 옵니다. 한 사람도 놓치지 않는 대회를 제안합니다.",
      {"type": "pins", "items": [[-3.9, -0.4, "인천공항", "#F2A541", "입국 · 태그 수령"], [-1.4, 0.9, "개막미사", "#5b6fd6", "8.3 · 집결 · 등록"], [0.6, -0.8, "광화문 일대", "#3fbf8f", "젊은이 축제"], [2.4, 1.4, "교황 환영", "#ff5a5a", "8.5"], [4.0, -0.2, "폐막미사", "#F2A541", "8.7 밤샘 기도 · 8.8"]]},
      stats=[["40만", "해외 순례자 (추정)"], ["6일", "8.3 ~ 8.8"], ["수십", "개 언어"]], hint="핀에 마우스를 올리거나 끌어서 돌려 보세요"),
   sc("jp2crowd", "The Problem", "인파 속 한 사람,<br><em>누가 먼저 알 수 있을까?</em>", "말이 다르고 길이 낯선 도시에서, 집결 시간이 지나서야 알게 된다면 이미 늦습니다.",
      "인파 속에서 한 사람이 일행을 놓치면, 누가 가장 먼저 알 수 있을까요?",
      {"type": "crowd", "groups": 6, "per": 9, "lostLabel": "Maria · 미확인 · 눌러서 찾기", "foundToast": "✓ 광화문 남측 반경 50m · 봉사자가 9분 만에 찾았습니다"}, hint="빨간 사람을 눌러 찾아보세요"),
   sc("checkin", "Galaxy SmartTag3 · 9.5g", "명찰에 단 태그 하나가<br><em>안전 끈이 됩니다.</em>", "공항 · 등록처에서 QR로 본인 · 그룹과 연결. 삼성 스폰서 시 순례자 부담 0원.",
      "명찰에 단 구 점 오 그램 태그 하나가, 순례자의 안전 끈이 됩니다.",
      {"type": "tag", "note": "9.5g · Android · iPhone · 대여 2~3천원(안)", "chips": [["공항 수령"], ["QR 연결"], ["마지막 위치"], ["대회 후 반납"]]},
      stats=[["9.5g", "SmartTag3"], ["0원", "삼성 스폰서 시"]]),
   sc("group", "Demo · KeepTrip", "내 일정을<br><em>내 언어로.</em>", "늦을 것 같으면 먼저 알리고, ‘Traducir’ 한 번으로 실시간 통역 앱에 연결합니다.",
      "모국어 일정이 열리고, 집결에 늦을 것 같으면 먼저 알려 줍니다.",
      {"type": "phone", "app": "KeepTrip · Día 3 · 5 de agosto", "title": "Mi itinerario de hoy", "color": "#4A5BB0",
       "rows": [["08:00", "Catequesis · Myeongdong", "ok"], ["11:30", "Festival · Gwanghwamun", "ok"], ["14:30", "Reunión · City Hall salida 3 · 25 min", "now"], ["16:00", "Bienvenida al Papa", ""]],
       "callouts": [["⏰ 집결 25분 전 알림", "l"], ["🗣 실시간 통역", "r"], ["🆘 SOS", "r"]], "tip": "스페인어 일정 예시"}),
   sc("procession", "Demo · KeepGuide", "누가 없는지,<br><em>집결 1분 만에.</em>", "인솔자는 그룹 점호를 1분 안에. 미확인자는 마지막 확인 위치 · 반경 · 경과 시간과 함께.",
      "인솔자는 일 분 만에 그룹을 확인하고, 미확인자는 마지막 위치와 함께 알립니다.",
      {"type": "phone", "app": "KeepGuide · 인솔자", "title": "Manila-07 그룹 · 14:31", "color": "#3E8E6E",
       "rows": [["30/32", "2명 미확인 · 집결 City Hall 3번", "now"], ["Maria", "미확인 12분 · 광화문 남측 50m", "no"], ["Juan", "이동 중 · 도착 4분", "now"], ["상황실", "신고 · 통역 · 전화", ""]],
       "callouts": [["⏱ 1분 점호", "l"], ["📍 마지막 위치 · 반경", "r"], ["📞 상황실 신고", "r"]]}),
   sc("street", "Scenario · 한 순례자의 7일", "출국 전부터 귀국까지,<br><em>한 사람의 7일.</em>", "등록 → 태그 수령 → 모국어 일정 → 통역 → 점호 · 이탈 경보 → 상황실 대응 → 반납",
      "출국 전 등록부터 귀국 반납까지, 한 순례자의 7일을 지킵니다.",
      {"type": "route", "stops": [["출국 전", "등록 · 동의"], ["8.1~3", "태그 수령"], ["매일 아침", "모국어 일정"], ["행사 중", "실시간 통역"], ["집결", "점호 · 경보"], ["귀국", "반납 · 파기"]]}),
   sc("stage", "KeepEnterprise · 조직위 상황실", "40만 명을<br><em>한 화면에.</em>", "구역 밀집도 · 미확인 경보 · SOS를 보고 가까운 봉사자 · 의료팀을 연결합니다. (시연용)",
      "조직위 상황실은 사십만 명의 현황을 한 화면에서 보고 바로 대응합니다.",
      {"type": "bars", "items": [["주 행사장", 3.2, "#ff5a5a", "밀집 92%"], ["광화문 일대", 2.3, "#F2A541", "71%"], ["교구 행사장", 1.3, "#3fbf8f", "38%"], ["환승역 주변", 2.0, "#F2A541", "64%"]]},
      stats=[["11분", "평균 발견 (목표)"], ["0건", "미해결 실종 (목표)"]]),
   sc("hands", "Samsung × 서울대교구 × Keep121", "Every one, kept.<br><em>모두가 함께 돌아가는 대회.</em>", "삼성전자 단말 스폰서 · 공동 캠페인, 2027 상반기 교구 청년 행사 파일럿부터 함께합니다.",
      "모두가 함께 돌아가는 대회. 서울대교구, 삼성전자와 함께 킵원투원이 만들겠습니다.",
      {"type": "arch"}, cta=[["15장 제안서 보기", "wyd2027.html"], ["맞춤 제안 모음", "proposals.html"]]),
  ]),
 # ───────────────────────────── 제주 ─────────────────────────────
 "jeju2027": dict(page="jeju2027-3d.html", deck="jeju2027", pages="17장", kicker="제주 이동안전 · 제주대학교 × Keep121",
  gate="제주를 찾은 모든 이가,<br>함께 돌아가도록", desc="중국인 방문객 · 수학여행단을 위한 제주 이동 안전 서비스 제안(안)을 60초 인터랙티브 3D로.",
  scenes=[
   sc("hill", "제주 · 산학 제안 (안)", "제주를 찾은 모든 이가<br><em>함께 돌아가도록.</em>", "2025년 제주 방문객 1,386만 명 — 외국인은 1년 새 17.7% 늘었습니다.",
      "지난해 제주를 찾은 천삼백팔십육만 명. 모두가 함께 돌아가도록 제안합니다.",
      {"type": "pins", "items": [[-3.8, -0.6, "제주공항", "#F2A541", "도착 · 태그 수령"], [-1.2, 1.2, "동문시장", "#ff5a5a", "자유시간 · 통역"], [3.9, -0.4, "성산일출봉", "#3fbf8f", "하산 집결"], [0.6, 2.0, "중문관광단지", "#8fa0ff", "숙소 · 야간 점호"]]},
      stats=[["1,386만", "2025 방문객"], ["224만", "외국인"], ["70.2%", "외국인 중 중국인"]], hint="핀에 마우스를 올리거나 끌어서 돌려 보세요"),
   sc("market", "Two customers", "대규모 행사가 아닌,<br><em>제주의 두 고객부터.</em>", "말이 통하지 않는 중국인 단체의 자유시간, 교사 한 명이 책임지는 수학여행 학생 수십 명.",
      "대규모 행사가 아닌, 중국인 단체와 수학여행 학생, 제주의 두 고객부터 시작합니다.",
      {"type": "cards", "items": [["중국인 단체", "158.8만 명 (2025). 중국어 일정 · 시장 통역 · 가이드 점호", "#ff5a5a"], ["수학여행", "2026 상반기 8.7만 명 · 535개교. 1분 점호 · 야간 점호", "#3fbf8f"], ["가족 · 시니어", "2단계 확장 대상", "#8fa0ff"], ["크루즈 단체", "2027 하반기 시험 운영", "#F2A541"]]}),
   sc("night", "The Problem", "시장 자유시간 뒤,<br><em>한 명이 돌아오지 않았다.</em>", "안내와 사전 점검은 있지만, ‘지금 누가 없는지’ 아는 일은 비어 있습니다.",
      "시장 자유시간 뒤 한 명이 돌아오지 않았다면, 지금 누가 없는지 바로 알아야 합니다.",
      {"type": "crowd", "groups": 6, "per": 8, "lostLabel": "미확인 1명 · 눌러서 찾기", "foundToast": "✓ 동문시장 8번 출구 반경 50m에서 찾았습니다"}, hint="빨간 사람을 눌러 찾아보세요"),
   sc("airport", "Galaxy SmartTag3 · 일정 단위 대여", "9.5g 태그를<br><em>여행 일정만큼만.</em>", "제주공항 · 크루즈항 데스크에서 받고, 출국할 때 반납합니다.",
      "구 점 오 그램 태그 하나를 여행 일정만큼만 빌려, 공항에서 받고 출국할 때 반납합니다.",
      {"type": "tag", "note": "9.5g · Android · iPhone · 1인 2~3천원(안)", "chips": [["공항 수령"], ["QR 연결"], ["마지막 위치"], ["출국 반납"]]}, stats=[["9.5g", "SmartTag3"], ["2~3천원", "일정당 대여 (안)"]]),
   sc("market", "KeepTrip 中文 · 실시간 통역", "중국어 일정이<br><em>위챗 안에서 바로.</em>", "늦을 것 같으면 먼저 알리고, ‘翻译’ 한 번으로 통역 앱 · 1330에 연결합니다.",
      "중국어 일정이 위챗 링크로 열리고, 늦을 것 같으면 먼저 알려 줍니다.",
      {"type": "phone", "app": "KeepTrip · 第2天", "title": "今日行程 · 上海 32人团", "color": "#4A5BB0",
       "rows": [["09:00", "城山日出峰 · 登山约60分钟", "ok"], ["12:00", "午餐 · 海鲜料理", "ok"], ["15:30", "东门市场 8号门 集合 · 还有20分钟", "now"], ["17:30", "返回酒店", ""]],
       "callouts": [["⏰ 집결 20분 전 알림", "l"], ["🗣 시장 · 택시 통역", "r"], ["📞 1330 사람 통역", "r"]], "tip": "중국어 일정 · 위챗 링크"}),
   sc("seongsan", "Scenario · 2박 3일", "공항에서 공항까지,<br><em>한 명도 빠짐없이.</em>", "공항 태그 수령 → 성산일출봉 → 동문시장 → 숙소 야간 점호 → 반납 · 안전 리포트",
      "공항에서 공항까지, 2박 3일 동안 한 명도 빠짐없이 함께합니다.",
      {"type": "route", "stops": [["제주공항", "태그 수령"], ["성산일출봉", "집결 알림"], ["동문시장", "통역 · 점호"], ["숙소", "22:00 야간 점호"], ["제주공항", "반납 · 리포트"]]}),
   sc("welcome", "KeepEnterprise · 제주관광공사", "관광공사는 오늘의<br><em>제주 안전을 한 화면에.</em>", "참여 여행사 · 학교의 운영 현황과 경보를 보고 1330 · 경찰 · 의료로 연결합니다. (시연용)",
      "제주관광공사는 오늘의 제주 안전을 한 화면에서 보고 바로 연결합니다.",
      {"type": "bars", "items": [["제주공항", 2.0, "#3fbf8f", "18개 그룹"], ["동문시장", 1.3, "#F2A541", "미확인 1"], ["성산일출봉", 3.0, "#ff5a5a", "혼잡"], ["중문관광단지", 2.4, "#3fbf8f", "22개 그룹"]]},
      stats=[["2억 원", "1년 차 시범 (안)"], ["8,000명", "시범 규모"]]),
   sc("coastwide", "제주관광공사 × 제주대학교 × Keep121", "Every one, kept.<br><em>모두 함께 돌아가는 제주.</em>", "2027 봄 수학여행 10개교, 여름 중국 단체 20팀부터 시범 운영을 제안합니다.",
      "모두 함께 돌아가는 제주. 내년 봄 수학여행 시범 운영부터 함께하겠습니다.",
      {"type": "arch"}, cta=[["17장 제안서 보기", "jeju2027.html"], ["맞춤 제안 모음", "proposals.html"]]),
  ]),
 # ─────────────────────────── 일산동중학교 ───────────────────────────
 "ilsandong": dict(page="ilsandong-3d.html", deck="ilsandong", pages="14장", kicker="일산동중학교 · 현장체험학습 · 수학여행",
  gate="바뀐 안전 지침,<br>지켰다는 기록까지", desc="일산동중학교 맞춤 제안: 2026 현장체험학습 안전 강화 지침에 맞춘 1분 점호 · 보조인력 · 이행 기록을 60초 인터랙티브 3D로.",
  scenes=[
   sc("uniform", "What changed · 2026", "현장체험학습<br><em>안전 지침이 바뀌었습니다.</em>", "교원 면책 강화 추진 · 보조인력 학급당 1명 · 업체 안전요원과 차량 점검 · 경기도 지침 간소화 (보도 기준)",
      "올해 현장체험학습 안전 지침이 바뀌었습니다. 이제는 지침을 지켰다는 기록이 중요합니다.",
      {"type": "cards", "items": [["교원 면책 강화", "고의 · 중과실이 없으면 민 · 형사 면책 추진", "#5b6fd6"], ["보조인력 학급당 1명", "학생 50명당 1명에서 학급당 1명으로", "#3fbf8f"], ["업체 의무 명시", "위탁업체 입찰에 안전요원 · 차량 점검", "#F2A541"], ["경기도 지침 개정", "교원 협의 · 학운위 심의 · 사전답사 간소화", "#ff5a5a"]]},
      hint="카드에 마우스를 올려 보세요"),
   sc("soccer", "2027학년도 연간 운영 (안)", "22학급 564명,<br><em>한 해 12번 학교 밖으로.</em>", "새학년 셋업 → 리더십 캠프 → 현장체험학습 → 진로체험 → 수학여행 → 별밤캠프 → 연간 보고",
      "이십이 학급 오백육십사 명이, 한 해 열두 번 학교 밖 활동에 나섭니다.",
      {"type": "route", "stops": [["3월", "명단 · 동의"], ["4월", "리더십 캠프"], ["5월", "현장체험학습"], ["7월", "진로체험"], ["10월", "경주 수학여행"], ["11월", "별밤캠프"], ["12월", "연간 보고"]]},
      stats=[["564명", "22학급"], ["12회", "체험 · 캠프 (2026)"]]),
   sc("gwanghwamun", "In the field", "체험처 집결,<br><em>한 명이 보이지 않는다.</em>", "처음 온 보조인력은 학생 얼굴을 모릅니다. 미확인 학생만, 마지막 확인 장소와 함께 알립니다.",
      "체험처 집결 때 한 명이 보이지 않으면, 마지막 확인 장소와 함께 바로 알립니다.",
      {"type": "crowd", "groups": 6, "per": 9, "lostLabel": "3반 B조 미확인 · 눌러서 찾기", "foundToast": "✓ 체험관 2층 · 5분 만에 합류"}, hint="빨간 학생을 눌러 찾아보세요"),
   sc("teacher", "Demo · KeepGuide", "담임은 반 전체,<br><em>보조인력은 맡은 조만.</em>", "같은 반 명단을 나눠 들고 명찰 QR로 1분 점호. 보조인력에게는 담당 학생만 보입니다.",
      "담임은 반 전체를, 보조인력은 맡은 조만 확인합니다. 점호는 일 분이면 충분합니다.",
      {"type": "phone", "app": "KeepGuide · 2학년 3반 담임", "title": "현장체험학습 · 버스 3호차", "color": "#3E8E6E",
       "rows": [["A조", "담임 · 14명 확인", "ok"], ["B조", "보조인력 · 13/14 확인 중", "now"], ["미확인", "1명 · 체험관 2층 · 4분 전", "no"], ["13:30", "버스 3호차 앞 집결", ""]],
       "callouts": [["👩‍🏫 담임 · 반 전체", "l"], ["🧑‍🤝‍🧑 보조인력 · 담당 조만", "r"], ["⏱ 1분 점호", "r"]]}),
   sc("campus", "Demo · 안전조치 이행 기록", "점호가 끝나면<br><em>이행 기록이 남습니다.</em>", "사전교육 · 동의 · 보조인력 배치 · 차량 점검 · 점호 · 귀교 — 따로 서류를 만들 필요가 없습니다.",
      "점호가 끝나는 순간, 안전조치 이행 기록이 자동으로 정리됩니다.",
      {"type": "phone", "style": "doc", "app": "2027.5.14 · 일산동중학교 · 자동 생성", "title": "현장체험학습 안전조치 이행 기록",
       "rows": [["사전교육", "5.13 6교시 · 8개 반", "ok"], ["학부모 동의", "201명 중 199명 · 2명 대체", "ok"], ["보조인력", "학급당 1명 · 8명 배정", "ok"], ["차량 점검", "버스 8대 점검표", "ok"], ["점호", "9회 · 평균 58초", "ok"], ["귀교", "16:42 · 201/201", "ok"]],
       "foot": "예시 · 가상 데이터. 학교 서식에 맞춰 조정합니다.", "tip": "학교 서식으로 PDF 내려받기"}),
   sc("hanok", "Demo · 학년부 화면", "교감 · 학년부는<br><em>학년 전체를 한 화면에.</em>", "반별 점호 · 보조인력 배치 · 미확인 경보를 실시간으로 봅니다. (시연용)",
      "교감과 학년부는 여덟 개 반의 점호 현황을 한 화면에서 봅니다.",
      {"type": "bars", "items": [["1반", 2.6, "#3fbf8f", "28/28"], ["2반", 2.6, "#3fbf8f", "28/28"], ["3반", 2.0, "#ff5a5a", "27/28"], ["4반", 2.6, "#3fbf8f", "25/25"], ["5반", 2.5, "#3fbf8f", "24/24"], ["6반", 2.5, "#3fbf8f", "24/24"], ["7반", 2.2, "#F2A541", "점호 중"], ["8반", 2.6, "#3fbf8f", "22/22"]]}),
   sc("bulguksa", "숙박형 · 수학여행", "수학여행엔<br><em>태그와 야간 점호를.</em>", "넓은 유적지와 숙소에는 SmartTag3를 더하고, 22시 층별 점호 뒤 미확인 학생만 교사가 확인합니다.",
      "경주 수학여행처럼 숙박형에는 태그를 더하고, 밤 열 시 숙소 점호까지 지킵니다.",
      {"type": "tag", "note": "수학여행 · 캠프에만 선택 · 반납 후 재사용", "chips": [["반별 키트"], ["유적지 자유관람"], ["22:00 야간 점호"], ["학부모 알림"]]}),
   sc("hanok", "일산동중학교 × Keep121", "모두 함께 돌아오는<br><em>체험학습.</em>", "2027학년도 1학기 5월 현장체험학습 무상 시범부터 함께하겠습니다.",
      "존중과 참여로 아끼고 키우고 나누는 배움터, 모두 함께 돌아오는 체험학습을 만들겠습니다.",
      {"type": "arch"}, cta=[["14장 제안서 보기", "ilsandong.html"], ["맞춤 제안 모음", "proposals.html"]]),
  ]),
 # ───────────────────────── 사랑글로벌아카데미 ─────────────────────────
 "saga2027": dict(page="saga2027-3d.html", deck="saga2027", pages="16장", kicker="사랑글로벌아카데미 2027 · Keep121",
  gate="레거시부터 비전트립까지,<br>한 분도 빠짐없이", desc="사랑글로벌아카데미 2027 통합 맞춤 제안 — 레거시아카데미 · 일터선교 비전트립 · 포에버 · 복지관 연계를 60초 인터랙티브 3D로.",
  scenes=[
   sc("saga_group", "SaGA 2027", "레거시부터 비전트립까지,<br><em>한 분도 빠짐없이.</em>", "강화 · 공주 · 양재천 · 서울대공원 · 신안 · 안동 · 나가사키, 그리고 유럽 종교개혁 비전트립.",
      "레거시 순례부터 유럽 비전트립까지, 이천이십칠 년 사랑글로벌아카데미의 모든 여정을 지킵니다.",
      {"type": "pins", "items": [[-2.4, -1.6, "강화", "#F2A541", "기독교 레거시 순례"], [-1.0, -0.9, "서울 · 양재천 · 대공원", "#3fbf8f", "워커톤 4.12 · 만보 걷기"], [-1.6, 0.4, "공주", "#F2A541", "레거시 리더십 여행"], [1.8, -0.4, "안동", "#8fa0ff", "요코하마에서 안동으로"], [-2.6, 2.0, "신안", "#5b6fd6", "섬티아고 12사도"], [3.8, 2.2, "나가사키", "#ff5a5a", "4.18~23 해외 레거시"]]},
      hint="핀에 마우스를 올려 보세요"),
   sc("grandpark2", "2027 Annual plan", "봄에 시험하고,<br><em>가을까지 실제로.</em>", "4.12 워커톤 · 5월 하루 코스 파일럿(무상) → 나가사키 · 1박 2일 · 비전트립 · 세미나 실제 운영",
      "사월 워커톤과 오월 하루 코스로 시험하고, 가을까지 실제 프로그램에서 운영합니다.",
      {"type": "route", "stops": [["4.12", "워커톤 (파일럿)"], ["4.18~23", "나가사키"], ["5월", "강화 · 공주 (파일럿)"], ["6~10월", "신안 · 안동 · 고성"], ["8월", "유럽 비전트립"], ["11.8~10", "세미나"]]}),
   sc("grandpark", "Demo · 4.12 레거시 워커톤", "1만보 걷는 날,<br><em>뒤처진 분을 먼저.</em>", "후미 봉사자와 가장 먼 분의 거리가 멀어지면 알림. 체크포인트 4곳에서 통과를 확인합니다.",
      "만 보를 걷는 날, 맨 뒤 봉사자와 거리가 멀어진 분을 먼저 알려 줍니다.",
      {"type": "crowd", "groups": 6, "per": 7, "lostLabel": "후미 350m · 눌러서 확인", "foundToast": "✓ 휴식 차량 연결 · 천천히 함께 걷는 중"}, hint="빨간 분을 눌러 확인해 보세요"),
   sc("gongju2", "Demo · 레거시 미션 (공주)", "교재의 ‘레거시 활동’이<br><em>조별 미션이 됩니다.</em>", "공주제일교회 → 영명학당 → 선교사 묘 → 늘봄정원. 질문 · 조별 사진 · 확인을 조장 휴대폰 하나로.",
      "교재의 레거시 활동이 조별 미션이 되어, 조장 휴대폰 하나로 함께 채웁니다.",
      {"type": "phone", "app": "KeepTrip · 레거시 미션 · 2조", "title": "레거시 리더십 여행 (공주)", "color": "#4A5BB0",
       "rows": [["1", "공주제일교회 · 누가 언제 개척했나?", "ok"], ["2", "영명학교 · 조별 사진", "ok"], ["3", "선교사 묘역 · 샤프 선교사 부부", "now"], ["4", "늘봄정원 · 레거시 식사 & 커피", ""]],
       "callouts": [["📖 배움의 장", "l"], ["📷 조별 사진", "r"], ["🚶 513m 후미 확인", "r"]]}),
   sc("yangjae", "생도는 명찰만", "앱도 휴대폰도 필요 없이,<br><em>명찰 태그 하나.</em>", "자녀에게는 출발 · 탑승 · 도착 세 번의 안심 알림. 건강 · 기도제목은 저장하지 않습니다.",
      "생도분들은 명찰만 거시면 됩니다. 자녀에게는 출발, 탑승, 도착 세 번 알려 드립니다.",
      {"type": "tag", "note": "앱 설치 없음 · 여정마다 대여 후 반납", "chips": [["출발 알림"], ["탑승 확인"], ["도착 알림"], ["종이 응급 카드"]]}),
   sc("hahoe", "Program portfolio", "SaGA의 다섯 가지 여정,<br><em>같은 도구로.</em>", "레거시 하루 · 1박 2일 · 해외 · 일터선교 비전트립 · 포에버와 반포종합사회복지관 연계",
      "다섯 가지 여정을 같은 도구로 운영하고, 포에버와 복지관 어르신 나들이로 넓힙니다.",
      {"type": "cards", "items": [["레거시 · 하루", "강화 · 공주 · 양재천 · 서울대공원", "#F2A541"], ["레거시 · 1박 2일", "신안 · 안동 · 고성", "#5b6fd6"], ["레거시 · 해외", "나가사키 4.18~23", "#ff5a5a"], ["일터선교 비전트립", "유럽 종교개혁 9일", "#8fa0ff"], ["연계 확장", "포에버 소풍 · 반포종합사회복지관", "#3fbf8f"]]}),
   sc("oura", "학장 · 운영위원 화면", "한 해의 모든 여정을<br><em>한 화면에서.</em>", "프로그램별 참가 확인 · 미션 완료 · 귀가 확인을 봅니다. (시연용)",
      "학장님과 운영위원은 한 해의 모든 여정을 한 화면에서 봅니다.",
      {"type": "bars", "items": [["워커톤", 2.8, "#3fbf8f", "104/104 완주"], ["나가사키", 2.4, "#3fbf8f", "40명 · 캐리어 40"], ["강화 · 공주", 2.2, "#F2A541", "미션 90%"], ["1박 2일", 2.6, "#3fbf8f", "야간 점호 완료"], ["비전트립", 2.0, "#8fa0ff", "8월 예정"], ["세미나", 1.4, "#8fa0ff", "11월 예정"]]}),
   sc("saga_night", "사랑글로벌아카데미 × Keep121", "“그는 늙어도 여전히 결실하며”<br><em>모두 함께 돌아오는 여정.</em>", "4.12 레거시 워커톤을 첫 무상 파일럿으로 제안드립니다.",
      "그는 늙어도 여전히 결실하며. 모두 함께 돌아오는 레거시 여정을 만들겠습니다.",
      {"type": "arch"}, cta=[["16장 제안서 보기", "saga2027.html"], ["맞춤 제안 모음", "proposals.html"]]),
  ]),
}

SHELL = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://keep121.co.kr/{page}">
  <meta property="og:image" content="{og}">
  <meta name="theme-color" content="#0b0f24">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Sans+KR:wght@400;500;600;700;800&display=swap">
  <link rel="stylesheet" href="assets/css/stage3d.css?v={v}">
  <script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}}}</script>
</head>
<body data-src="data/{id}_stage.json">
<!-- 장면: data/{id}_stage.json · 엔진: assets/js/stage3d.js · 생성: scripts/add_stage3d.py -->
<div id="bg" aria-hidden="true"><div class="bgl a"></div><div class="bgl b"></div></div>
<div class="veil" aria-hidden="true"></div>
<canvas id="scene" aria-label="인터랙티브 3D 장면 — 끌어서 돌리고, 오브젝트를 눌러 볼 수 있습니다"></canvas>
<div id="labels" aria-hidden="true"></div>
<div id="tip" role="tooltip"></div>
<header class="top">
  <a class="brand" href="index.html" aria-label="Keep121 홈"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#23306B"/><path d="M9 26V15a7 7 0 0 1 14 0v11" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><circle cx="16" cy="20.5" r="3" fill="#F2A541"/></svg>Keep121</a>
  <nav class="nav" aria-label="제안 메뉴"><a href="index.html">홈</a><a href="proposals.html">맞춤 제안</a><a href="{deck}.html">{pages} 제안서</a></nav>
</header>
<section class="cap" id="cap" aria-live="polite"></section>
<div id="toast" role="status"></div>
<div class="ctl"><button id="play" aria-label="재생 / 정지">❚❚</button><button id="mute" aria-label="소리 켜기 / 끄기">🔇</button><div id="dots"></div><div class="track"><div id="bar"></div></div><span id="time">0s</span><button id="replay">다시 보기</button></div>
<section class="gate" id="gate"><div><span class="k">{kicker}</span><h1>{gate}</h1><p>약 1분 · 내레이션과 배경음 · 끌어서 돌리고 눌러 보는 3D</p>
  <div class="btns"><button id="go-sound">▶ 소리 켜고 보기</button><button id="go-mute">소리 없이 보기</button></div>
  <small>내레이션은 기기에 설치된 한국어 음성으로 읽습니다 (시제품)</small></div></section>
<script type="module" src="assets/js/stage3d.js?v={v}"></script>
</body>
</html>
"""

CSS = """/* 포토 스테이지 1분 3D (원본: scripts/add_stage3d.py) */
:root{--dawn:#F2A541;--ink:#0b0f24}
*{box-sizing:border-box} html,body{margin:0;height:100%;background:var(--ink);color:#fff;font-family:"IBM Plex Sans KR",system-ui,sans-serif;overflow:hidden}
#bg{position:fixed;inset:-30px;z-index:0;transition:transform .2s linear}
.bgl{position:absolute;inset:0;background:center/cover no-repeat;opacity:0;transform:scale(1.04);transition:opacity 1.2s ease}
.bgl.on{opacity:1;animation:kb 9s ease-out forwards}
@keyframes kb{from{transform:scale(1.04)}to{transform:scale(1.16)}}
.veil{position:fixed;inset:0;z-index:1;pointer-events:none;background:linear-gradient(0deg,rgba(11,15,36,.95) 0%,rgba(11,15,36,.55) 38%,rgba(11,15,36,.25) 62%,rgba(11,15,36,.55) 100%)}
#scene{position:fixed;inset:0;width:100%;height:100%;display:block;z-index:2;cursor:grab;touch-action:none}
#labels{position:fixed;inset:0;z-index:3;pointer-events:none}
.lbl{position:absolute;left:0;top:0;white-space:nowrap;font-size:13px;font-weight:700;padding:5px 10px;border-radius:999px;background:rgba(11,15,36,.78);border:1px solid rgba(255,255,255,.2);backdrop-filter:blur(6px);transition:opacity .3s}
.lbl span{display:block;font-weight:500;font-size:11.5px;color:#c9d0ee}
.lbl.pin{background:rgba(255,255,255,.92);color:#141a2e}
.lbl.warn{background:#ff5a5a;border-color:#ff8a8a;animation:pulse 1.1s ease-in-out infinite}
.lbl.ok{background:#3fbf8f;border-color:#7fd1ad}
.lbl.chip{background:rgba(242,165,65,.92);color:#2a1a00;border:0}
.lbl.bar,.lbl.stop{border-radius:10px;text-align:center}
@keyframes pulse{50%{box-shadow:0 0 0 8px rgba(255,90,90,.25)}}
#tip{position:fixed;left:0;top:0;z-index:6;max-width:260px;padding:10px 14px;border-radius:12px;background:#fff;color:#141a2e;font-size:14px;line-height:1.5;box-shadow:0 12px 40px rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:opacity .2s}
#tip.on{opacity:1} #tip b{color:#23306B}
#toast{position:fixed;left:50%;top:84px;transform:translate(-50%,-10px);z-index:6;background:#3fbf8f;color:#062b1c;font-weight:800;padding:12px 20px;border-radius:14px;opacity:0;transition:.35s;pointer-events:none;box-shadow:0 12px 30px rgba(0,0,0,.3)}
#toast.on{opacity:1;transform:translate(-50%,0)}
.top{position:fixed;left:16px;right:16px;top:14px;display:flex;justify-content:space-between;align-items:center;gap:12px;z-index:5}
.top a{color:#fff;text-decoration:none}
.brand{display:flex;align-items:center;gap:8px;font:800 16px "Bricolage Grotesque",sans-serif;background:rgba(11,15,36,.6);padding:6px 12px 6px 8px;border-radius:12px;backdrop-filter:blur(8px)}
.brand svg{width:24px;height:24px}
.nav{display:flex;gap:4px;background:rgba(11,15,36,.6);padding:4px;border-radius:12px;backdrop-filter:blur(8px);font-size:14px}
.nav a{padding:6px 10px;border-radius:9px;opacity:.85} .nav a:hover{background:rgba(255,255,255,.12);opacity:1}
.cap{position:fixed;left:clamp(16px,5vw,80px);bottom:96px;z-index:4;width:min(600px,calc(100% - 32px));opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s;pointer-events:none}
.cap.on{opacity:1;transform:none}
.cap .k{font:700 13px "Bricolage Grotesque",sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--dawn);margin:0 0 10px}
.cap h2{font-size:clamp(28px,4.2vw,52px);line-height:1.16;margin:0 0 12px;letter-spacing:-.02em;text-shadow:0 4px 30px rgba(0,0,0,.7)} .cap h2 em{font-style:normal;color:var(--dawn)}
.cap .sub{font-size:clamp(15px,1.6vw,19px);line-height:1.6;color:#e1e6fa;margin:0;text-shadow:0 2px 14px rgba(0,0,0,.8)}
.cap .hint{margin:14px 0 0;display:inline-block;font-size:14px;font-weight:700;background:rgba(242,165,65,.18);border:1px solid rgba(242,165,65,.5);color:#ffd7a1;padding:6px 12px;border-radius:999px}
.stats{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.stats div{background:rgba(11,15,36,.55);border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:9px 14px;backdrop-filter:blur(6px)}
.stats b{display:block;font:800 24px "Bricolage Grotesque",sans-serif;color:var(--dawn)} .stats span{font-size:12.5px;color:#c9d0ee}
.cta{display:flex;gap:10px;margin-top:20px;pointer-events:auto} .cta a{background:var(--dawn);color:#2a1a00;font-weight:700;padding:12px 18px;border-radius:12px;text-decoration:none} .cta a.ghost{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.28)}
.ctl{position:fixed;left:16px;right:16px;bottom:22px;z-index:5;display:flex;align-items:center;gap:10px}
.ctl button{border:0;background:rgba(255,255,255,.14);color:#fff;border-radius:10px;height:36px;min-width:40px;padding:0 12px;font:inherit;cursor:pointer}
#dots{display:flex;gap:6px} #dots button{min-width:0;width:24px;height:24px;padding:0;background:transparent;display:grid;place-items:center} #dots i{width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.35)} #dots button.on i{background:var(--dawn);transform:scale(1.4)}
.track{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.18);overflow:hidden} #bar{height:100%;width:0;background:var(--dawn)}
#time{font-size:13px;color:#aab3d8;min-width:72px;text-align:right} #replay{display:none} body.ended #replay{display:inline-block}
.gate{position:fixed;inset:0;z-index:10;display:grid;place-items:center;background:radial-gradient(ellipse at center,rgba(11,15,36,.7),rgba(11,15,36,.96));text-align:center;padding:24px}
.gate[hidden]{display:none} body.gating .cap,body.gating #labels{opacity:0!important}
.gate .k{font:700 13px "Bricolage Grotesque",sans-serif;letter-spacing:.16em;color:var(--dawn);text-transform:uppercase}
.gate h1{font-size:clamp(28px,4.4vw,52px);margin:10px 0 8px;line-height:1.2} .gate p{color:#c9d0ee;margin:0 0 26px}
.gate .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.gate button{border:0;border-radius:14px;padding:16px 26px;font:700 18px "IBM Plex Sans KR",sans-serif;cursor:pointer}
#go-sound{background:var(--dawn);color:#2a1a00} #go-mute{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25)}
.gate small{display:block;margin-top:18px;color:#8a93b8;font-size:13px}
@media (max-width:640px){.nav a:not(:last-child){display:none} .cap{bottom:84px} .stats b{font-size:19px} #dots{display:none} .lbl{font-size:11.5px;padding:4px 8px} .cap h2{font-size:27px}}
"""

wr("assets/css/stage3d.css", CSS)
wr("assets/js/stage3d.js", rd("scripts/stage3d.js"))
wr("assets/js/sound3d.js", rd("scripts/sound3d.js"))

for id_, cfg in DECKS.items():
    deck = json.loads(rd(f"data/{cfg['deck']}.json"))
    used = {s["bg"] for s in cfg["scenes"]}
    img = {}
    for k in used:
        assert k in deck["img"], (id_, k)
        img[k] = deck["img"][k]
        if f"{k}@pos" in deck["img"]: img[f"{k}@pos"] = deck["img"][f"{k}@pos"]
    data = {"title": f"{cfg['kicker']} · 1분 3D 제안", "img": img, "scenes": cfg["scenes"]}
    total = sum(s["dur"] for s in cfg["scenes"])
    assert abs(total - 60) < 0.01, (id_, total)
    wr(f"data/{id_}_stage.json", json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    title = f"{cfg['kicker'].split(' · ')[0]} · 1분 3D 제안 · Keep121"
    wr(cfg["page"], SHELL.format(title=title, desc=cfg["desc"], page=cfg["page"], og=img[cfg["scenes"][0]["bg"]], v=V, id=id_,
                                 deck=cfg["deck"], pages=cfg["pages"], kicker=cfg["kicker"], gate=cfg["gate"]))

# 각 제안서 상단의 '▶ 3D 1분 제안서 보기' (link3d) · 맞춤 제안 카드의 '▶ 1분 3D 제안'
for script, page, anchor in [("scripts/add_ilsandong_proposal.py", "ilsandong-3d.html", 'wr("data/ilsandong.json"'),
                             ("scripts/add_saga2027_proposal.py", "saga2027-3d.html", 'wr("data/saga2027.json"')]:
    t = rd(script)
    if "link3d" not in t:
        t = t.replace(anchor, f'D["link3d"] = "{page}"  # 1분 3D 버전 (상단 메뉴 링크)\n' + anchor, 1); wr(script, t)
p = "scripts/add_proposals_page.py"; t = rd(p)
for marker, page in [('"stats": [["564명", "22학급"]', "ilsandong-3d.html"), ('"stats": [["10+", "2027 여정"]', "saga2027-3d.html")]:
    if page not in t:
        t = t.replace(marker, f'"extra": ["▶ 1분 3D 제안", "{page}"], ' + marker, 1)
wr(p, t)
for s in ["add_ilsandong_proposal", "add_saga2027_proposal", "add_proposals_page"]:
    subprocess.run([sys.executable, str(ROOT / f"scripts/{s}.py")], check=True, stdout=subprocess.DEVNULL)
print("  jeju2027-3d.html · ilsandong-3d.html · saga2027-3d.html · data/*_stage.json · assets/js/stage3d.js · sound3d.js")
