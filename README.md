# Keep121 — Every one, kept. 한 사람도 빠짐없이, 지키다

단체 안전 플랫폼 Keep121(구 SafeFlock) 소개 홈페이지 (GitHub Pages). 디자인은 Keep121 브랜드 가이드 v1.0(색상·글꼴·로고·명칭 체계)을 따릅니다.

**https://holyjoekang.github.io/keep121/**

## 구성

- `index.html` — 홈 (히어로 · 문제/해결/근거 요약 · 페이지 안내 · 파일럿 CTA)
- 주제별 페이지 (상단 고정 탭으로 페이지 안 이동, 하단에 이전/다음 페이지)
  - `solution.html` — 문제 · 솔루션 구조 · 작동 방식 · 라이브 지도 데모
  - `evidence.html` — 시뮬레이션 결과
  - `product.html` — 디자인 · 단말·모드·프리셋 · 경보 체계
  - `family.html` — 가족 안심 링크·알림 정책 · 여행 기록
  - `usecases.html` — 설산 시나리오 · 활용 분야 · 제주
  - `business.html` — 가격·구매자 · 소싱·운영 · 로드맵
  - `company.html` — 브랜드 스토리 · 팀 · 파일럿 문의
- `Keep121_솔루션_재설계.html` — 13,312회 시뮬레이션 결과로 솔루션을 재설계한 문서 (2026-10-16). 홈페이지 내용의 근거
- `assets/css/style.css`, `assets/js/main.js` — 스타일과 인터랙션 (원탭 출석 체크, Leaflet 줌인 지도, 시뮬레이션 차트, 프리셋 선택기, 배터리·경보 임계값 계산, 프리셋 가격 계산기)
- `story/` — 이전 버전 상세 페이지

## 다국어 (English · 简体中文)

- 한국어 페이지(루트의 `*.html`)가 원본입니다. `en/`, `zh/` 페이지는 직접 고치지 말고 스크립트로 생성합니다.
- 번역 사전: `i18n/en.json`, `i18n/zh.json` (한국어 문구 → 번역), 인터랙션 문구는 `assets/js/i18n.en.js`, `assets/js/i18n.zh.js`
- 한국어 페이지를 고친 뒤:

```bash
python tools/i18n_build.py extract   # 새로 번역할 문구 목록 → i18n/segments.json
python tools/i18n_build.py build     # en/, zh/ 페이지 생성 (번역이 빠진 문구는 목록으로 표시)
```

## 로컬 실행

```bash
python -m http.server 5173
```

모든 화면과 수치는 콘셉트 시안·목표치이며 검증된 실적이 아닙니다. 시뮬레이션 수치는 가정값으로 돌린 결과로, 실측 샘플로 보정할 대상입니다.
