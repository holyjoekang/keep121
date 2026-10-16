# SafeFlock Lite BLE 소싱 후보 재조사

**1차 샘플은 Minew B7, KKM W1, MOKOSmart W6R/W6BR의 3개 제품을 우선 비교할 것을 권합니다.** 착용 형태, 설정·개발 지원, 샘플 구매 경로를 함께 고려한 선정입니다.

이번 조사에서는 기존 목록을 다음과 같이 수정했습니다.

- **Minew B7 추가:** 공식 스토어의 가격과 착용 중량을 확인해 최우선 후보로 선정했습니다.
- **MOKOSmart 제품 변경:** 자산 부착용 M1P 대신 손목밴드용 W6R/W6BR을 선정했습니다.
- **Meshtrac·BeaconTrax 제외:** 원제조사와 공급구조 확인이 부족해 이번 제조사 중심 목록에서 제외했습니다.

**조사 기준일: 2026년 10월 16일.** 아래 사양은 제조사 공개자료이며, 재고·한국 배송·인증서·실제 성능은 공급사 답변과 샘플로 확인해야 합니다.

## 1. Top 10 후보 — 샘플 검토 우선순위

| 순위 | 업체·검토 제품 | 공식 자료에서 확인한 내용 | SafeFlock 적합성·남은 확인사항 |
|---:|---|---|---|
| **1** | **Minew — B7 Button Wristband** | BLE 5.0, IP67, 교체형 코인전지 220mAh, SOS 버튼. 본체 9.5g＋밴드 2.5g. 공식 스토어 표시가격 **US$12**. [Minewstore](https://www.minewstore.com/product/b7-button-wristband?utm_source=chatgpt.com) | **첫 구매 후보.** 착용형 완제품과 가격 확인 근거가 가장 명확합니다. 일반 BLE 버전·재사용 스트랩으로 지정하고 광고 주기, SDK, 버튼 이벤트 문서를 요청합니다. |
| **2** | **KKM — W1 Wearable Tag** | BLE 5.0, 배터리 포함 본체 8g, 교체형 CR2032 210mAh, IP63. 광고 간격 100ms~40초, KBeaconPro 설정 앱, OTA 지원. AirTag용 손목밴드·키링 액세서리를 활용하는 구조입니다. [Compatible with Wide Range of Accessories](https://www.kkmcn.com/wearable-tag-w1?utm_source=chatgpt.com) | **경량 비교 후보.** 본체는 목표에 가깝지만 IP67에는 미달합니다. 스트랩 포함 총중량, 액세서리 실제 호환성, 1초 광고 시 배터리 수명을 확인합니다. |
| **3** | **MOKOSmart — W6R/W6BR Wrist Strap Tag** | BLE 5.0, IP66, 교체형 CR2032 220mAh, 버튼·LED·가속도 센서, 손목밴드·키링 착용. 본체 약 38.6×38.6×10.5~10.8mm. 제조사 표기 수명은 기본 설정에서 1.5년입니다. [Attendance Tracking & SOS Alerts](https://store.mokosmart.com/product/w6-wrist-strap-tag/?utm_source=chatgpt.com) | **제품 조정·OEM 협의 후보.** 기존 M1P보다 용도에 맞습니다. W6R와 W6BR의 차이, 총중량, 샘플가, 버튼·광고 데이터 형식을 확인합니다. |
| **4** | **Global Tag — Wristband Beacony** | BLE 4.2, 교체형 CR2032, IP67, 광고 간격 100ms~10초. 공개 중량 8.2g, 1초 광고에서 약 1년 수명을 안내합니다. [Global Tag](https://www.global-tag.com/portfolio/wristband-beacon-bluetooth-le/?utm_source=chatgpt.com) | **경량·방수 비교 후보.** 8.2g에 스트랩이 포함되는지 불명확합니다. 구성품별 중량, 현재 판매 버전, 개발 문서, 한국 배송비를 확인합니다. |
| **5** | **HoneyComm — HCBB16** | 직경 40×10mm, IP67, 광고 간격 100ms~10초, 앱 설정 지원. 걸거나 착용하는 용도도 안내합니다. [HoneyComm](https://www.honeycomm.net/product/waterproof-ultrasonic-welding-100meters-ble-5-0-wearable-low-power-bluetooth-beacon-tag-for-personnel-management/?utm_source=chatgpt.com) | **견적 조건부 후보.** 무게가 없고 BLE 버전이 본문·표에서 다르게 기재돼 있습니다. 배터리 모델·교체 가능 여부·착용 액세서리까지 서면 확인 후 샘플을 결정합니다. |
| **6** | **Feasycom — FSC-BP107D** | BLE 5.1, IP67, 손목밴드형, CR3032, 광고 간격 100ms~10초, OTA·FeasyBeacon SDK 지원. 공개 중량 36g입니다. [IBeacon, Eddystone, AltBeacon Support](https://www.feasycom.com/product/fsc-bp107d/?utm_source=chatgpt.com) | **기능·착용감 비교 후보.** Lite 경량 목표에는 무겁습니다. 버튼 알림과 운영 편의성을 비교할 가치가 있으며, SOS가 기성 펌웨어에 포함되는지 확인해야 합니다. |
| **7** | **BlueUp — SafeX Watch BLE** | 교체형 CR2477, 버튼·가속도 센서·LED, 선택형 부저·진동, IP65, 공개 중량 27.5g. 공식 스토어 표시가격 **€33**, 스트랩 별도이며 품절 표시가 있습니다. [docs.blueupbeacons.com](https://docs.blueupbeacons.com/Devices/BLE/Datasheets/BLE_SafeXWatch_DS_v2025_2.pdf?utm_source=chatgpt.com) | **알림 기능 비교 기준.** 가격·무게가 Lite에는 부담입니다. 재입고·한국 배송·BLE 모델 펌웨어를 확인하고, 후속 고기능 제품 검토에 활용합니다. |
| **8** | **Dusun — DSBC-100** | nRF52820, 손목밴드·목걸이 옵션, CR2032 180mAh, 본체 약 41mm·30g. 모델에 따라 NFC·가속도·비퍼 기능이 다릅니다. [dusuniot.com](https://www.dusuniot.com/product-specification/bluetooth-keyfob-wristband-beacon/?utm_source=chatgpt.com) | **착용형 예비 후보.** Lite에는 크고 무겁습니다. 재고형 모델과 주문 제작형을 구분해 문의하고, 정확한 모델별 IP 등급·기능을 받아야 합니다. |
| **9** | **BNCOM — MIDASCON Beacon Tag** | 공식 사이트 검색 노출자료에 BLE 4.1, 32×66×7.9mm·18g, CR2450, 비상 알림 버튼, KC 인증이 기재돼 있습니다. [www.bncomm.co.kr](https://www.bncomm.co.kr/products/odm/pro-beacon?utm_source=chatgpt.com) | **국내 기술상담 후보.** 이번 재조사에서 제품 페이지 직접 접속은 실패했습니다. 현재 공급 여부·최신 대체 모델·KC 인증번호부터 확인해야 합니다. |
| **10** | **ELA Innovation — Blue LITE ID** | 배지·목걸이형, 교체형 배터리, 설정 도구·SDK 제공. 공식 제품 페이지 표시가격 **€29.15**, 주문 일시 불가 표시가 있습니다. [ELA Innovation](https://elainnovation.com/en/product/blue-lite-id-en/?utm_source=chatgpt.com) | **개발 문서·산업용 제품 비교 후보.** 손목밴드 완제품이 아닙니다. 판매 모델과 연결된 구형 데이터시트의 모델번호가 달라 최신 사양·재고를 받아야 합니다. |

**판단:** 1~3위는 지금 샘플 견적을 받을 대상입니다. 4~6위는 사양·견적 확인 후 추가할 후보이고, 7~10위는 공급 대안과 기능 비교용으로 두는 것이 적절합니다.

## 2. 상위 3개를 선정한 이유

### ① Minew B7 — 가장 빠른 착용형 MVP

B7은 공식 스토어에서 가격·구성·구매 경로를 확인할 수 있고, 제조사 페이지에서 SDK와 재사용 가능한 분리형 스트랩을 안내합니다. [Minew](https://www.minew.com/product/b7-button-wristband/?utm_source=chatgpt.com)

**요청할 구성**

- 일반 BLE/iBeacon·Eddystone 버전
- 재사용 가능한 스트랩
- 코인전지 포함
- Android SDK와 버튼 이벤트 해석 문서

스토어에는 Cisco Spaces·Quuppa 관련 버전도 표시돼 있으므로, **가이드 휴대폰으로 광고 패킷을 직접 읽는 일반 BLE 구성**을 명시해야 합니다.

### ② KKM W1 — 경량 단말과 액세서리 비용 검증

본체 8g은 최초 경량 목표에 가깝습니다. 별도 손목밴드 케이스를 활용할 수 있어, **태그 가격＋액세서리 가격＋배부·회수 편의성**을 검증하기 좋습니다.

KKM은 자체 앱 개발을 위한 SDK와 OEM/ODM·펌웨어 조정 서비스를 공개하고 있습니다. 다만 W1에 필요한 기능과 문서가 실제로 제공되는지는 모델별로 확인해야 합니다. [Simple your development](https://www.kkmcn.com/kbeacon_sdk?utm_source=chatgpt.com)

### ③ MOKOSmart W6R/W6BR — 착용형 운영과 후속 변경 협의

W6R/W6BR은 처음부터 손목 착용·버튼·배터리 교환을 고려한 제품입니다. 기존 M1P에 홀더를 추가하는 방식보다 초기 운영 구성이 명확합니다.

단, **기존 충전형 W6와 교체형 W6R/W6BR을 혼동하면 안 됩니다.** 견적서에 정확한 모델명, 펌웨어 버전, 액세서리를 기재하도록 요청하세요.

## 3. 실제 샘플 구매 계획

### 1단계 — 3개 모델 × 각 3대

| 제품 | 수량 | 검증 목적 |
|---|---:|---|
| Minew B7 | 3대 | 착용형 완제품, 버튼 이벤트, 앱 연동 |
| KKM W1 | 3대＋착용 액세서리 | 경량성, 액세서리 원가, 설정 편의성 |
| MOKO W6R 또는 W6BR | 3대 | 착용·배터리 교환·운영 편의성 |
| **합계** | **9대** | 모델 간 기본 기능 비교 |

Minew B7의 공개가격 기준 **3대 단말값은 US$36**입니다. 다른 두 제품의 가격과 배송·세금·액세서리는 견적을 받아야 합니다. 현재 공개가격으로 대량 양산 단가를 추정하지 않겠습니다.

### 2단계 — 선정 모델 30대

기본 시험에서 우승 모델을 고른 뒤 **운영 25대＋예비 5대**로 확대합니다.

**9대 샘플 시험으로 25명 동시 운영 성능까지 입증할 수는 없습니다.** 30대 단계에서 실제 투어 인원 규모의 탐지·배부·회수와 경보 품질을 검증합니다.

## 4. RFQ를 이렇게 수정하면 비교가 쉬워집니다

공급사에는 아래 항목을 **가능 / 불가 / 추가개발 필요**로 답하도록 요청하세요.

| 필수 확인사항 | 받아야 할 답변·증빙 |
|---|---|
| **자체 앱에서 직접 수신** | 광고 패킷 형식, Android 예제, 제조사 클라우드 이용 의무 유무 |
| **1초 광고 설정** | 설정 범위, 앱·SDK, 설정값 유지 여부 |
| **25개 태그 탐지** | 다수 태그의 광고 패킷 수신 예제·시험 로그 |
| **버튼·배터리 데이터** | 이벤트 패킷과 배터리 정보 해석 문서 |
| **착용 구성** | 본체·배터리·스트랩 각각의 무게와 구성품 사진 |
| **보안** | 설정 접근제어, ID 회전, 인증·암호화 지원을 각각 구분 |
| **조달 조건** | 3대·30대·100대·500대 가격, MOQ, 납기, 한국 배송비 |
| **품질·인증** | 해당 모델의 인증번호·시험자료·보증·초기 불량 처리 |

여기서 **25개 태그의 광고 신호 수신과 25개 기기의 지속 연결은 다른 요구**입니다. SafeFlock의 인원 확인은 광고 수신을 기본으로 하고, 개별 설정이나 찾기 기능에서 필요한 연결 방식을 별도로 확인하면 됩니다.

또한 **ID 변경 기능이나 설정 비밀번호만으로 복제 방지·추적 방지가 구현되는 것은 아닙니다.** 회전 ID와 암호학적 인증은 별도의 지원 여부·개발비 항목으로 견적을 받아야 합니다.

## 5. 권장 판정 기준

샘플은 같은 휴대폰·같은 설정으로 비교합니다.

- **탐지:** 태그별 마지막 수신 시각, 신호 공백, 누락 빈도
- **경보:** 정상 집단 이동 중 오경보와 실제 이탈 시 감지 지연
- **휴대폰:** 화면이 켜진 상태·꺼진 상태에서 수신 지속 여부
- **착용:** 손목·목걸이 착용감, 분실 가능성, 배터리 교환 편의성
- **개발:** 패킷 문서로 자체 앱에서 ID·배터리·버튼 이벤트를 읽을 수 있는지

**최종 추천은 Minew B7을 기준 제품으로 삼고, KKM W1과 MOKO W6R/W6BR을 같은 조건에서 비교하는 것입니다.** 현재 단계에서는 10개 업체 전체에 샘플 비용을 쓰기보다, 상위 3개 제품의 실제 동작과 공급사 대응을 확인한 뒤 30대 파일럿으로 넘어가는 편이 효율적입니다.
