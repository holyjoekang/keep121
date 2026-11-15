"""Generate the Brand Shop using the company page shell and the site's SVG symbols."""

import json
import re
from dataclasses import dataclass
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


@dataclass(frozen=True)
class SymbolPlacement:
    photo: str
    reference_mm: int  # Nominal width of the blank, not a supplier specification.
    reference_px: int  # Same span measured on the 418px photo (body only, no sleeves/handles).
    ink_mm: int        # Width of the actual printed strokes, excluding SVG viewBox padding.
    center_x: int
    center_y: int
    finish: str
    placement: str


SYMBOLS = {
    "hoodie": SymbolPlacement("hoodie-back", 550, 186, 140, 209, 198, "print", "후드 아래의 평평한 등판 중앙"),
    "cap": SymbolPlacement("cap", 195, 264, 25, 248, 178, "thread", "중앙 봉제선을 비운 왼쪽 앞 패널"),
    "polo": SymbolPlacement("polo", 520, 232, 42, 264, 143, "thread", "단추 여밈 옆 왼쪽 가슴"),
    "notebook": SymbolPlacement("notebook", 148, 229, 26, 280, 313, "print", "스프링에서 떨어진 표지 오른쪽 아래"),
    "diary": SymbolPlacement("diary", 148, 232, 24, 198, 255, "print", "밴드 안쪽, 표지 중앙보다 조금 아래"),
    "tumbler": SymbolPlacement("tumbler", 70, 113, 20, 210, 224, "print", "곡면이 정면으로 보이는 몸체 중앙"),
    "tote": SymbolPlacement("tote", 360, 264, 95, 209, 272, "print", "손잡이 박음선과 바닥 솔기 사이"),
    "lanyard": SymbolPlacement("lanyard", 54, 66, 13, 209, 351, "print", "명찰 홀더의 안쪽 카드 중앙"),
}


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, value):
    (ROOT / path).write_text(value, encoding="utf-8")


def mockup(photo, ink, left, top, width, alt, *, featured=False, finish=None):
    unit = width if finish else width / 4
    artwork = f'<use href="#logo" x="{left}" y="{top}" width="{unit}" height="{unit}"/>'
    if finish:
        if finish == "thread":
            mask = f'{photo}-thread-{"hero" if featured else "card"}'
            artwork = (f'<defs><mask id="{mask}" style="mask-type:alpha">{artwork}</mask></defs>'
                       f'{artwork}<rect x="{left}" y="{top}" width="{unit}" height="{unit}" '
                       f'fill="url(#shop-stitches)" mask="url(#{mask})"/>')
        artwork = f'<g class="shop-ink-{finish}">{artwork}</g>'
    else:
        artwork += f'<use href="#wordmark" x="{left + unit}" y="{top}" width="{width - unit}" height="{unit}"/>'
        if photo == "hoodie-back":
            artwork += '<text x="209" y="247" fill="white" text-anchor="middle" font-size="10" font-family="sans-serif">keep121.co.kr</text>'
    return f'''<div class="shop-photo">
      <img src="assets/pics/brand-shop/{photo}.jpg" alt="{alt}" width="418" height="418" loading="{'eager' if featured else 'lazy'}">
      <svg viewBox="0 0 418 418" aria-hidden="true" color="{ink}">
        {artwork}
      </svg>
    </div>'''


def symbol_mockup(product, ink, *, featured=False):
    spec = SYMBOLS[product]
    # The official symbol has 29 × 35 units of visible ink in its 48-unit viewBox.
    # Center that ink (24, 25) on the chosen panel, not the transparent bounds.
    scale = spec.ink_mm * spec.reference_px / spec.reference_mm / 29
    x = round(spec.center_x - 24 * scale, 2)
    y = round(spec.center_y - 25 * scale, 2)
    finish = "자수" if spec.finish == "thread" else "인쇄"
    caption = f"{spec.placement} · {finish} 폭 {spec.ink_mm / 10:g}cm"
    color = "#EEECE5" if ink == "white" else ink
    image = mockup(spec.photo, color, x, y, round(48 * scale, 2), caption, featured=featured, finish=spec.finish)
    return image, caption


def inquiry_link(email, item=""):
    subject = "[Keep121 브랜드 샵] " + (item or "단체 제작") + " 문의"
    body = f"관심 품목: {item}\r\n예상 수량: \r\n희망 일정: \r\n단체명 및 요청 사항: "
    return f"mailto:{email}?subject={quote(subject)}&amp;body={quote(body)}"


def product_cards(email, *, symbol_only):
    cards = []
    for photo, name, description, ink, x, y, width in PRODUCTS:
        design = "심벌 단독" if symbol_only else "기본 로고"
        if symbol_only:
            image, description = symbol_mockup(photo, ink)
        else:
            image = mockup(photo, ink, x, y, width, f"{name} {design} 시안. {description}")
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
        image, _ = symbol_mockup(product, "white", featured=True)
        hero_images.append(image)
    front = mockup("hoodie", "white", 248, 170, 43, "집업 후드티 앞면의 왼쪽 가슴 로고", featured=True)
    back = mockup("hoodie-back", "white", 138, 197, 142, "집업 후드티 뒷면의 로고와 keep121.co.kr", featured=True)
    return f'''<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <defs><pattern id="shop-stitches" patternUnits="userSpaceOnUse" width="2" height="2" patternTransform="rotate(28)">
    <path d="M0 0V2" stroke="#332e25" stroke-opacity=".28" stroke-width=".65"/>
  </pattern></defs>
</svg>
<section class="shop-hero">
  <div class="wrap shop-spread">
    <div>
      <nav class="shop-crumb" aria-label="현재 위치"><a href="company.html#vision">회사소개</a><span aria-hidden="true"> / </span>브랜드 샵</nav>
      <h1>브랜드 샵</h1>
      <p>문 하나, 점 하나. Keep121의 약속을 단체로 함께 입고 쓰는 여덟 가지 굿즈에 담았습니다.</p>
      <a class="btn btn-dawn" href="#catalog">굿즈 둘러보기 <span aria-hidden="true">↓</span></a>
    </div>
    <figure class="shop-large">
      <div class="shop-pair">{"".join(hero_images)}</div>
      <figcaption>심벌 단독 <span>집업 후드티 뒷면 · 볼캡 앞면</span></figcaption>
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
    <p class="shop-note">심벌 폭은 제작 시안의 목표 치수입니다. 최종 크기와 위치는 선택한 제품의 도안에 맞춰 조정합니다.</p>
    <fieldset class="shop-design">
      <legend>디자인 선택</legend>
      <label><input type="radio" name="shop-design" value="large" checked> 심벌 단독</label>
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
    shell = shell.replace("</head>", '  <link rel="stylesheet" href="assets/css/brand-shop.css?v=3">\n</head>')
    write(SHOP, shell)
    write("content/pages/brand-shop.html", build_catalog(email))


if __name__ == "__main__":
    main()
