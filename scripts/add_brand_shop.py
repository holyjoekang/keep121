"""Generate the Brand Shop using the company page shell and the site's SVG symbols."""

import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SHOP = "brand-shop.html"
TITLE = "브랜드 샵"
DESCRIPTION = "Keep121 로고를 담은 의류, 문구, 현장 소품 8종의 제작 시안을 살펴보고 단체 제작을 문의하세요."

# Coordinates place the official symbols on each 418 × 418 studio photo.
# (photo, name, description, ink, left, top, lockup width)
PRODUCTS = [
    ("hoodie", "집업 후드티", "왼쪽 가슴에는 작은 로고를, 등에는 워드마크와 웹사이트 주소를 담았습니다.", "white", 248, 170, 43),
    ("cap", "볼캡", "네이비색 모자 앞판의 중앙에 밝은 로고가 놓입니다.", "white", 161, 156, 96),
    ("polo", "폴로셔츠", "현장 스태프가 함께 입을 수 있도록 왼쪽 가슴에 로고를 작게 배치했습니다.", "white", 250, 138, 46),
    ("notebook", "스프링 노트", "회의와 답사 기록을 위한 노트입니다. 밝은 표지에 인디고 로고를 넣었습니다.", "#23306B", 168, 176, 106),
    ("diary", "다이어리", "일정과 프로젝트 기록을 담는 다이어리입니다. 짙은 표지에 밝은 워드마크를 더했습니다.", "white", 136, 179, 121),
    ("tumbler", "텀블러", "금속 몸체의 중앙에 인디고 로고를 배치한 휴대용 텀블러입니다.", "#23306B", 172, 220, 76),
    ("tote", "에코백", "교육 자료와 소지품을 담는 가방입니다. 앞면에 로고를 넓게 배치했습니다.", "#23306B", 135, 237, 147),
    ("lanyard", "명찰·랜야드", "행사와 단체 이동에 쓰는 목걸이형 명찰입니다. 카드 상단에 로고를 넣었습니다.", "#23306B", 184, 307, 51),
]

# On the zip hoodie the uninterrupted back panel carries the large symbol.
# (photo, left, top, symbol size, placement description)
LARGE_SYMBOLS = {
    "hoodie": ("hoodie-back", 89, 114, 240, "검정 후드티 등판 한가운데에 흰색 아치와 금빛 점을 크게 배치했습니다."),
    "cap": ("cap", 126, 89, 166, "챙 바로 위, 네이비색 앞판 중앙에 흰색 심벌을 크게 넣었습니다."),
    "polo": ("polo", 123, 140, 172, "단추 아래 가슴 중앙에 흰색 심벌을 크게 배치했습니다."),
    "notebook": ("notebook", 105, 87, 222, "밝은 종이 표지 한가운데에 인디고색 심벌을 넓게 담았습니다."),
    "diary": ("diary", 95, 89, 211, "네이비색 표지에서 오른쪽 밴드를 피해 흰색 심벌을 가운데 놓았습니다."),
    "tumbler": ("tumbler", 142, 141, 136, "은빛 몸체 전면에 인디고색 심벌을 세로로 길게 담았습니다."),
    "tote": ("tote", 87, 155, 244, "가방 앞면을 넓게 써서 인디고색 아치와 금빛 점이 멀리서도 보이도록 했습니다."),
    "lanyard": ("lanyard", 157, 286, 104, "랜야드에 달린 밝은 명찰 카드 중앙에 인디고색 심벌을 넣었습니다."),
}


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, value):
    (ROOT / path).write_text(value, encoding="utf-8")


def mockup(photo, ink, left, top, width, alt, *, featured=False, symbol_only=False):
    unit = width if symbol_only else width / 4
    artwork = f'<use href="#logo" x="{left}" y="{top}" width="{unit}" height="{unit}"/>'
    if not symbol_only:
        artwork += f'<use href="#wordmark" x="{left + unit}" y="{top}" width="{width - unit}" height="{unit}"/>'
        if photo == "hoodie-back":
            artwork += '<text x="209" y="247" fill="white" text-anchor="middle" font-size="10" font-family="sans-serif">keep121.co.kr</text>'
    return f'''<div class="shop-photo">
      <img src="assets/pics/brand-shop/{photo}.jpg" alt="{alt}" width="418" height="418" loading="{'eager' if featured else 'lazy'}">
      <svg viewBox="0 0 418 418" aria-hidden="true" color="{ink}">
        {artwork}
      </svg>
    </div>'''


def inquiry_link(email, item=""):
    subject = "[Keep121 브랜드 샵] " + (item or "단체 제작") + " 문의"
    body = f"관심 품목: {item}\r\n예상 수량: \r\n희망 일정: \r\n단체명 및 요청 사항: "
    return f"mailto:{email}?subject={quote(subject)}&amp;body={quote(body)}"


def product_cards(email, *, symbol_only):
    cards = []
    for photo, name, description, ink, x, y, width in PRODUCTS:
        design = "대형 심벌" if symbol_only else "기본 로고"
        if symbol_only:
            photo, x, y, width, description = LARGE_SYMBOLS[photo]
        image = mockup(photo, ink, x, y, width, f"{name} {design} 시안. {description}", symbol_only=symbol_only)
        item = f"{name} · {design}"
        cards.append(f'''    <article class="shop-card">
      {image}
      <h3>{name}</h3>
      <p>{description}</p>
      <a href="{inquiry_link(email, item)}" aria-label="{item} 제작 문의">제작 문의 <span aria-hidden="true">↗</span></a>
    </article>''')
    return "\n".join(cards)


def build_catalog(email):
    hero_images = []
    for product in ("hoodie", "cap"):
        photo, x, y, width, description = LARGE_SYMBOLS[product]
        hero_images.append(mockup(photo, "white", x, y, width, description, featured=True, symbol_only=True))
    front = mockup("hoodie", "white", 248, 170, 43, "집업 후드티 앞면의 왼쪽 가슴 로고", featured=True)
    back = mockup("hoodie-back", "white", 138, 197, 142, "집업 후드티 뒷면의 로고와 keep121.co.kr", featured=True)
    return f'''<section class="shop-hero">
  <div class="wrap shop-spread">
    <div>
      <nav class="shop-crumb" aria-label="현재 위치"><a href="company.html#vision">회사소개</a><span aria-hidden="true"> / </span>브랜드 샵</nav>
      <h1>브랜드 샵</h1>
      <p>문 하나, 점 하나. Keep121의 약속을 단체로 함께 입고 쓰는 여덟 가지 굿즈에 담았습니다.</p>
      <a class="btn btn-dawn" href="#catalog">굿즈 둘러보기 <span aria-hidden="true">↓</span></a>
    </div>
    <figure class="shop-large">
      <div class="shop-pair">{"".join(hero_images)}</div>
      <figcaption>대형 심벌 <span>집업 후드티 뒷면 · 볼캡 앞면</span></figcaption>
    </figure>
    <figure class="shop-classic">
      <div class="shop-pair">{front}{back}</div>
      <figcaption>집업 후드티 <span>앞면 · 뒷면 제작 시안</span></figcaption>
    </figure>
  </div>
</section>
<section class="shop-catalog" id="catalog" aria-labelledby="catalog-title">
  <div class="wrap">
    <h2 id="catalog-title">굿즈 카탈로그</h2>
    <p class="shop-note">상품 이미지는 제작 시안입니다. 색상과 로고 인쇄 방식은 제작 문의 시 협의합니다.</p>
    <fieldset class="shop-design">
      <legend>디자인 선택</legend>
      <label><input type="radio" name="shop-design" value="large" checked> 대형 심벌</label>
      <label><input type="radio" name="shop-design" value="classic" id="shop-classic"> 기본 로고</label>
    </fieldset>
    <div class="shop-grid shop-large">
{product_cards(email, symbol_only=True)}
    </div>
    <div class="shop-grid shop-classic">
{product_cards(email, symbol_only=False)}
    </div>
  </div>
</section>
<section class="shop-contact" aria-labelledby="shop-contact-title">
  <div class="wrap">
    <div><h2 id="shop-contact-title">단체 제작 문의</h2><p>관심 품목과 예상 수량, 필요한 날짜를 알려주세요.</p></div>
    <div><a class="btn btn-primary" href="{inquiry_link(email)}">이메일로 문의하기 <span aria-hidden="true">↗</span></a>
      <p class="shop-email">{escape(email)}</p></div>
  </div>
</section>
'''


def main():
    site = json.loads(read("data/site.json"))
    company = next(group for group in site["menu"] if group["en"] == "Company")
    company["label"] = "회사소개"
    footer = next(col for col in site["footer"]["columns"] if col["title"] == "Company")
    email = next(link["href"].removeprefix("mailto:") for link in footer["links"] if link["href"].startswith("mailto:"))
    for links in [company["items"], footer["links"]]:
        if not any(link["href"] == SHOP for link in links):
            contact = next(i for i, link in enumerate(links) if link["href"] == "company.html#contact")
            links.insert(contact, {"href": SHOP, "label": TITLE})
    if not any(page["file"] == SHOP for page in site["pages"]):
        index = next(i for i, page in enumerate(site["pages"]) if page["id"] == "company")
        site["pages"].insert(index + 1, {"id": "brand-shop", "file": SHOP, "name": TITLE})
    write("data/site.json", json.dumps(site, ensure_ascii=False, indent=2) + "\n")

    shell = read("company.html").replace("회사 · Keep121", "브랜드 샵 · Keep121")
    shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]+', lambda m: m[1] + DESCRIPTION, shell)
    shell = re.sub(r'(<meta property="og:url" content=")[^"]+', r'\g<1>https://keep121.co.kr/brand-shop.html', shell)
    shell = shell.replace('data-page="company"', 'data-page="brand-shop"')
    shell = re.sub(r'  <link rel="stylesheet" href="assets/css/b2b[^"]+">\n', '', shell)
    shell = shell.replace("</head>", '  <link rel="stylesheet" href="assets/css/brand-shop.css?v=2">\n</head>')
    write(SHOP, shell)
    write("content/pages/brand-shop.html", build_catalog(email))


if __name__ == "__main__":
    main()
