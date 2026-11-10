"""Align operating design and solution narrative with the product page."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
(r/'assets/css/solutions.css').write_text((r/'scripts/visual_pages/solutions.css').read_text())
product=(r/'content/pages/product.html').read_text()
badge=re.search(r'<div class="badge-art.*?(<svg viewBox="0 0 380 400".*?</svg>)',product,re.S).group(1)
def sec(k,title,body,cls='',id=''):
 return f'<section class="{cls}" id="{id}"><div class="wrap"><span class="v-k">{k}</span><h2>{title}</h2>{body}</div></section>'
def cards(items):return '<div class="v-grid">'+''.join(f'<article class="v-card"><span class="v-chip">{tag}</span><h3>{title}</h3><p>{desc}</p><a class="text-link" href="{href}">{link} →</a></article>' for tag,title,desc,href,link in items)+'</div>'
def steps(items):return '<div class="v-flow">'+''.join(f'<div><b>0{i+1}</b><strong>{name}</strong><p>{text}</p></div>' for i,(name,text) in enumerate(items))+'</div>'
# The product page is the naming and scope authority, without changing its contents.
ops=(r/'content/pages/operations.html').read_text()
start=ops.index('<section class="" id="hardware">');end=ops.index('<section ',start+10)
hardware=sec('01 / PRODUCT SYSTEM','명찰과 앱, 네 가지 역할로 연결합니다.','<div class="v-split"><div class="s-badge">'+badge+'</div><div><p class="v-lead">제품 페이지의 구성을 그대로 현장에 적용합니다. Keep Check는 직접 점호, Keep Tag는 위치 확인, Guide는 판단과 기록, Keep Home은 확인된 사실의 전달을 맡습니다.</p><div class="v-status"><span>기본: Guide + Keep Check</span><span>위치 필요 시: Keep Tag</span><span>알림 연동: Keep Home</span></div><p class="v-note">BLE 전용 태그는 독립 제품으로 제공하지 않습니다. 호환 Keep Tag의 BLE 근접 후보 활용은 단말·앱 연동 검증 후 적용할 기능이며, 인솔자의 확인을 대신하지 않습니다.</p></div></div>'+cards([('현장 운영','Keep121 Guide','명단·점호·미확인자 대응·라벨·종료 기록. 현재 웹앱은 로컬 저장 방식이며 Android 네이티브 앱은 제품 계획입니다.','product.html#guide','가이드 앱 구성'),('NFC 명찰','Keep Check','배터리 없는 NFC 명찰로 한 명씩 확인합니다. 회수가 필요 없는 방식으로 배부할 수 있는 기본 점호 제품입니다.','product.html#tag','NFC 명찰 보기'),('GPS · LTE','Keep Tag','기성 인증품과 위치정보 플랫폼 연동을 전제로 최근 위치를 확인하는 명찰형 트래커입니다.','product.html#tag','트래커 도입 조건')])+'<div class="s-home"><span class="v-chip">Keep Home · 연동 계획</span><h3>가족에게는 확인된 사실만.</h3><p>인솔자가 도착을 확인한 시각과 결과를 전달합니다. 알림 전송과 보호자의 수신·확인은 구분합니다. 현재 웹앱에는 알림톡이 연결되어 있지 않습니다.</p><a href="product.html#lineup">전체 제품 체계 →</a></div>',id='hardware')
ops=ops[:start]+hardware+ops[end:]
replacements={
'BLE 중심 + 필요 인원 GPS':'Keep Check 기본 + Keep Tag 선택',
'NFC·QR / BLE + 차량 수신기 선택':'Keep Check + Guide · 인계 확인',
'NFC·QR 기본 + BLE 행사 대여':'Keep Check + Guide · Keep Tag 선택',
'BLE·GPS 혼합 + 다국어 참가자 웹':'Keep Tag / Check + KeepTrip 연계 계획',
'비정기 행사와 자원봉사 인솔에 맞춘 간단한 준비와 일괄 대여를 계획합니다.':'비정기 행사와 자원봉사 인솔에는 NFC 점호를 기본으로 합니다. 위치 확인이 필요한 경우 Keep Tag를 선택하고, 배부·충전·회수를 함께 준비합니다.',
'명찰 · BLE · GPS':'Keep Check · Keep Tag',
'직접 확인 / 주변 신호 / 최근 위치':'NFC 탭 / GPS·LTE 최근 위치',
'기관 · 보호자':'Console / HQ · Keep Home',
'운영 콘솔 · 확인된 사실의 알림':'기관 기록 · 확인된 사실의 알림',
'장비는 현장에 맞게. 확인은 사람을 중심으로.':'Guide·Check·Tag·Home을 하나의 확인 흐름으로.',
'>BLE</text>':'>NFC</text>',
'BLE·GPS 자동 수신은 미연결':'단말 자동 수신은 미연결',
'BLE/GPS 수신':'Keep Tag 위치 수신',
'최종 인계와 장비 회수를 확인한 뒤 기록을 내보냅니다.':'최종 인계를 확인하고 Keep Tag를 회수합니다. 배부형 Keep Check는 회수 없이 운영할 수 있습니다.'}
for a,b in replacements.items():ops=ops.replace(a,b)
ops=ops.replace('인바운드 이동 일러스트','인바운드 이동 일러스트')
(r/'content/pages/operations.html').write_text(ops)
# Visual solution page: issue -> product -> action -> observable result.
hero='''<div class="vp solution-v2"><section class="v-hero"><div class="wrap v-split"><div><span class="v-k">KEEP121 SOLUTIONS / EVERY ONE, KEPT.</span><h1>이동의 빈틈을 찾고,<br><em>확인의 흐름으로<br>연결합니다.</em></h1><p class="v-lead">버스를 탈 때, 흩어졌다 모일 때, 보호자에게 인계할 때.<br>서로 다른 현장의 문제를 제품과 행동으로 하나씩 풀어갑니다.</p><div class="v-cta"><a class="btn btn-primary" href="#issues">우리 현장의 문제 찾기 ↓</a><a class="btn btn-ghost" href="product.html">제품 구성 보기</a></div></div><div class="s-journey" role="img" aria-label="명단 분산, 미확인, 인계 공백을 Guide의 명단, 재확인, 기록으로 연결하는 개념도"><div class="s-journey-head">이동 중 생기는 세 가지 빈틈</div><div class="s-before"><span>흩어진 명단</span><span>놓친 확인</span><span>남지 않은 인계</span></div><div class="s-join" aria-hidden="true">↓</div><div class="s-hub"><b>Keep121 Guide</b><small>누가 · 언제 · 무엇을 확인했는가</small></div><div class="s-join" aria-hidden="true">↓</div><div class="s-after"><span>한 명단</span><span>새 집결마다 확인</span><span>대응·종료 기록</span></div><p>제품과 운영 절차를 연결한 개념도</p></div></div></section>'''
issues=[
('roll','01','반복 점호','휴게소마다 다시 세는데,<br>누가 빠졌는지 알기 어렵습니다.','여행 패키지 · 학교 현장학습 · 지역단체','호명·머릿수만으로는 같은 사람을 두 번 세거나 이전 집결의 확인을 이번 결과로 착각할 수 있습니다.','Keep Check + Guide','명단을 준비하고 집결별 점호를 시작합니다. NFC 탭 또는 직접 확인을 기록하고 미확인자부터 다시 확인합니다.','이번 집결의 확인 인원과 미확인 명단이 분리됩니다. 확인을 취소하면 사유가 남습니다.','점호 시간 · 미확인자 재확인 횟수','현재 웹앱: 명단·점호·직접 확인, 지원 브라우저 NFC','check'),
('boarding','02','탑승과 출발','버스 옆에 있었다고,<br>버스에 탄 것은 아닙니다.','패키지 다중 차량 · 수학여행 · 단체 관광','집결지 주변 감지나 위치만 보고 탑승을 완료하면 다른 버스 탑승과 미승차를 놓칠 수 있습니다.','Guide + Keep Check / Keep Tag','현재 탑승 단계에서 인원을 확인합니다. 미확인자는 현장에서 재확인하고, 담당자가 차량·인원을 최종 확인한 뒤 출발을 완료합니다.','미확인자·미해결 대응이 있는 동안 앱의 출발 완료가 차단됩니다. 위치와 근접 후보는 보조 근거입니다.','출발 전 미확인 잔여 인원 · 확인 완료까지 걸린 시간','현재: 출발 확인 조건 / 출발 후 경보는 연동·실증 필요','bus'),
('free','03','자유시간과 재집결','집합 시간이 지났는데,<br>어디부터 찾아야 할까요?','3~5일 패키지 · 어르신 관광 · 향후 인바운드','연락이 닿지 않는 참가자의 마지막 확인과 위치가 분리되어 있으면 대응 시작이 늦어집니다.','Keep Tag + Guide · KeepTrip 연계','마지막 인원 확인을 보고 연락·현장 확인 담당자를 정합니다. 연동된 Keep Tag의 최근 위치·수신 시각을 참고해 대응하고, 재합류를 직접 확인합니다.','찾는 과정과 재합류 근거가 남습니다. KeepTrip은 집합 장소·시각 안내를 돕는 여행객 앱으로 연결할 계획입니다.','미확인 인지 시간 · 대응 시작·해결 시간','현재: 대응 기록 / 위치·일정 연동은 개발 계획','pin'),
('handover','04','등하교와 인계','내린 사실과 인계한 사실은<br>서로 다른 확인입니다.','유치원 등하교 · 교육기관 · 송영 확장','차량 가까이에서 신호가 잡힌 것만으로 하차나 보호자 인계를 확정할 수 없습니다.','Keep Check + Guide · Keep Home 연계','승차·하차 단계별 직접 확인을 하고 인계 대상과 담당자를 확인합니다. 차량 내부 최종 점검 후 운행을 종료하는 절차로 설계합니다.','통학 모드의 종료 점검을 유지합니다. 수신기나 태그는 차량 내부 직접 확인을 대체하지 않습니다.','미인계 인원 · 차량 최종 점검 기록','현재: 통학 종료 확인 / 인계 대상별 구조화는 고도화 계획','school'),
('family','05','보호자 소통','“괜찮다”는 말보다,<br>누가 확인했는지가 필요합니다.','학교 현장학습 · 어르신 관광 · 가족 여행','자동 위치 신호를 안전 확인으로 전달하면 실제 확인 여부와 보호자의 이해가 달라집니다.','Guide → Keep Home','인솔자가 도착·인계를 확인한 뒤 그 사실과 시각을 전달합니다. 전송 대기·실패·완료를 구분하고, 수신 확인이 없으면 읽었다고 표시하지 않습니다.','확인한 사실을 기준으로 일관된 알림을 보냅니다. Keep Home은 현재 웹앱에 연결되지 않은 계획 기능입니다.','확인 후 전송 시간 · 실패·재전송 건수','계획: 도착 확인 알림 1종부터 검증','message'),
('record','06','운영 기록과 개선','행사는 끝났는데,<br>확인 과정은 기억에만 남습니다.','여행사 · 교육기관 · 지역단체 운영자','누가 언제 확인하고 어떤 이유로 수정했는지 없으면 다음 행사의 운영 개선도 어렵습니다.','Guide → Console / HQ','인원 확인·취소·대응·장비 회수를 시간순으로 기록합니다. 현장에서 백업·CSV를 내보내고, 기관 콘솔 연동은 다음 단계로 개발합니다.','담당자의 행동과 처리 시간이 남습니다. 현재는 기기 내 기록이며 기관 간 자동 공유는 제공하지 않습니다.','기록 누락 · 오경보 라벨 · 재이용 의향','현재: 로컬 기록·JSON/CSV / 기관 콘솔은 로드맵','file')]
nav='<nav class="s-issue-nav" aria-label="문제별 바로가기">'+''.join(f'<a href="#{id}"><b>{no}</b>{label}</a>' for id,no,label,*_ in issues)+'</nav>'
body=hero+sec('01 / FIND YOUR ISSUE','우리 현장에서 생기는 문제를 선택하세요.','<p class="v-lead">문제 → 대응 제품 → 현장 행동 → 확인 결과. 같은 구조로 여섯 가지 이슈를 살펴보세요.</p>'+nav,id='issues')
for id,no,label,title,env,problem,products,action,result,metric,status,icon in issues:
 content=f'''<div class="s-issue-heading"><div><span class="v-chip">{env}</span><h2>{title}</h2></div><div class="s-symbol" aria-hidden="true"><svg class="icon"><use href="#i-{icon}"/></svg></div></div><div class="s-resolution"><article class="s-problem"><span class="s-label">문제 / ISSUE</span><h3>{label}의 빈틈</h3><p>{problem}</p></article><div class="s-chevron" aria-hidden="true">→</div><article class="s-action"><span class="s-label">대응 / ACTION</span><h3>{products}</h3><p>{action}</p></article></div><div class="s-result"><b>확인할 결과</b><p>{result}</p></div><details class="s-evidence"><summary>제공 범위와 검증 지표</summary><p><strong>{status}</strong></p><p>실증에서 측정: {metric}</p></details>'''
 body+=f'<section id="{id}" class="{"v-soft" if int(no)%2 else ""}"><div class="wrap"><span class="v-k">ISSUE {no} / {label}</span>{content}</div></section>'
body+=sec('02 / PRODUCT CONNECTION','네 가지 제품, 하나의 확인 흐름.','<div class="s-product-map"><a href="product.html#tag"><span>확인 입력</span><b>Keep Check</b><small>NFC 명찰 · 직접 점호</small></a><span class="s-map-arrow" aria-hidden="true">→</span><a class="s-map-hub" href="product.html#guide"><span>현장 판단과 기록</span><b>Keep121 Guide</b><small>미확인 → 대응 → 직접 확인</small></a><span class="s-map-arrow" aria-hidden="true">→</span><a href="product.html#lineup"><span>확인된 사실 전달</span><b>Keep Home</b><small>도착·확인 시각 · 연동 계획</small></a></div><div class="s-support"><a href="product.html#tag"><b>Keep Tag</b><span>GPS·LTE 최근 위치 → Guide 대응 보조</span></a><a href="product.html#keeptrip"><b>KeepTrip</b><span>여행객의 일정·집합 안내 · 연계 계획</span></a><a href="product.html#roadmap"><b>Console / HQ</b><span>기관 운영·기록 · 로드맵</span></a></div><p class="v-note">독립 BLE 전용 태그, 넘어짐 감지, SOS는 현재 제품 범위에 포함하지 않습니다. 인원 확인과 사고 대응의 최종 판단은 담당자가 합니다.</p>','v-band',id='products')
body+=sec('03 / ONE WORKFLOW','서로 다른 이동도, 확인의 원칙은 같습니다.',steps([('출발 준비','참가자·담당자·명찰을 연결합니다. 수집 목적과 동의를 확인합니다.'),('이동과 재집결','새 장소마다 새 점호. 미확인자를 우선 확인합니다.'),('대응과 인계','연락·현장 확인·재합류·인계 근거를 남깁니다.'),('종료와 개선','Keep Tag 회수, 현장 점검, 기록 백업으로 마무리합니다.')])+'<p class="v-note">30초 점호·3분 인지는 제품 계획의 검증 목표입니다. 실측된 성능이나 안전 보장으로 표현하지 않습니다.</p>',id='workflow')
body+=sec('04 / TRY THE WORKFLOW','지금 가능한 확인부터 경험하세요.','<div class="v-split"><div><h3>현재 Guide 웹앱</h3><p>명단, 점호, 확인 취소, 대응 기록, 출발 조건, 장비 회수와 종료, 기기 내 저장과 내보내기를 제공합니다.</p></div><div><h3>단말·서버 연동 다음 단계</h3><p>Keep Tag 위치 수신, 자동 경보, Keep Home 알림, 다중 인솔자 동기화, 기관 콘솔을 실제 장비·운영 환경에서 검증합니다.</p></div></div><div class="v-cta"><a class="btn btn-primary" href="guide/">Guide 앱 사용하기</a><a class="btn btn-ghost" href="operations.html">사용 환경별 운영 보기</a><a class="btn btn-ghost" href="company.html#contact">현장 실증 협의</a></div>','v-soft',id='demo')+'</div>'
(r/'content/pages/solution.html').write_text(body)
for name in ['solution','operations']:
 p=r/(name+'.html');s=p.read_text().replace('<body>', '<body class="product-aligned">')
 for css in ['operations','solutions']:
  if f'assets/css/{css}.css' not in s:s=s.replace('</head>',f'<link rel="stylesheet" href="assets/css/{css}.css">\n</head>')
 p.write_text(s)
