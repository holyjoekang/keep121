"""KeepTrip 앱 링크를 GitHub Pages 배포 주소로 바꾼다. 다시 돌려도 안전.

    python scripts/update_keeptrip_link.py

KeepTrip(holyjoekang/keeptrip)은 main 푸시 때 GitHub Actions로 https://holyjoekang.github.io/keeptrip/ 에 배포된다.
- content/pages/keeptrip.html · product.html 의 'KeepTrip 앱 열기' 버튼과 안내 문구
- scripts/add_app_links.py (원본 생성 스크립트도 같은 주소로)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://holyjoekang.github.io/keeptrip/"
REPL = [
    ("https://keeptrip.ai.studio/", URL),
    ("keeptrip.ai.studio · 시제품(Google AI Studio) · 설치 없이 링크로", "holyjoekang.github.io/keeptrip · 시제품 · 설치 없이 링크로"),
    ("keeptrip.ai.studio · 시제품(Google AI Studio)", "holyjoekang.github.io/keeptrip · 시제품"),
]
for f in ["content/pages/keeptrip.html", "content/pages/product.html", "scripts/add_app_links.py"]:
    p = ROOT / f
    t = p.read_text(encoding="utf-8")
    for a, b in REPL:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
print("  KeepTrip 링크 →", URL)
