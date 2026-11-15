"""Generate the Brand Shop using the company page shell and the site's SVG symbols."""

import json
import re
from dataclasses import dataclass, replace
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


def mockup(photo, ink, left, top, width, alt, *, featured=False, finish=None, size=(418, 418), url_label=None):
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
        if url_label:
            x, y, font_size = url_label
            artwork += f'<text x="{x}" y="{y}" fill="white" text-anchor="middle" font-size="{font_size}" font-family="sans-serif">keep121.co.kr</text>'
    w, h = size
    return f'''<div class="shop-photo">
      <img src="assets/pics/brand-shop/{photo}.jpg" alt="{alt}" width="{w}" height="{h}" loading="{'eager' if featured else 'lazy'}">
      <svg viewBox="0 0 {w} {h}" aria-hidden="true" color="{ink}">
        {artwork}
      </svg>
    </div>'''


def symbol_mockup(spec, ink, *, featured=False, size=(418, 418)):
    # The official symbol has 29 × 35 units of visible ink in its 48-unit viewBox.
    # Center that ink (24, 25) on the chosen panel, not the transparent bounds.
    scale = spec.ink_mm * spec.reference_px / spec.reference_mm / 29
    x = round(spec.center_x - 24 * scale, 2)
    y = round(spec.center_y - 25 * scale, 2)
    finish = "자수" if spec.finish == "thread" else "인쇄"
    caption = f"{spec.placement} · {finish} 폭 {spec.ink_mm / 10:g}cm"
    color = "#EEECE5" if ink == "white" else ink
    image = mockup(spec.photo, color, x, y, round(48 * scale, 2), caption, featured=featured, finish=spec.finish, size=size)
    return image, caption


def inquiry_link(email, item=""):
    subject = "[Keep121 브랜드 샵] " + (item or "단체 제작") + " 문의"
    body = f"관심 품목: {item}\r\n예상 수량: \r\n희망 일정: \r\n단체명 및 요청 사항: "
    return f"mailto:{email}?subject={quote(subject)}&amp;body={quote(body)}"


def product_cards(email):
    groups = []
    for photo, name, description, ink, x, y, width in PRODUCTS:
        symbol, placement = symbol_mockup(SYMBOLS[photo], ink)
        basic = mockup(photo, ink, x, y, width, f"{name} 기본 로고 시안. {description}")
        cards = []
        for design, image, caption in (("심벌 단독", symbol, placement), ("기본 로고", basic, description)):
            item = f"{name} · {design}"
            cards.append(f'''    <div class="shop-card">
      {image}
      <h4>{design}</h4>
      <p>{caption}</p>
      <a href="{inquiry_link(email, item)}" aria-label="{item} 제작 문의">제작 문의 <span aria-hidden="true">↗</span></a>
    </div>''')
        groups.append(f'<article class="shop-product"><h3>{name}</h3><div class="shop-variants">{"".join(cards)}</div></article>')
    return "\n".join(groups)


def worn_gallery():
    # Measured on the portrait crops: hoodie body between the sleeves, cap across the crown.
    hoodie = replace(SYMBOLS["hoodie"], photo="worn-hoodie-back", reference_px=328, center_x=256, center_y=493)
    cap = replace(SYMBOLS["cap"], photo="worn-cap", reference_px=374, center_x=315, center_y=184)
    torso_scale = hoodie.reference_px / SYMBOLS["hoodie"].reference_px
    cap_scale = cap.reference_px / SYMBOLS["cap"].reference_px
    hoodie_size = (512, 880)
    cap_size = (512, 704)
    plain = '<div class="shop-photo"><img src="assets/pics/brand-shop/worn-hoodie-front.jpg" width="512" height="880" loading="lazy" alt="심벌 단독 후드티를 입은 모델의 무지 앞면"></div>'
    back, _ = symbol_mockup(hoodie, "white", size=hoodie_size)
    hat, _ = symbol_mockup(cap, "white", size=cap_size)
    views = [
        ("집업 후드티 앞면", plain, mockup("worn-hoodie-front", "white", 322, 394, 43 * torso_scale,
                                  "착용자 왼쪽 가슴의 기본 로고", size=hoodie_size)),
        ("집업 후드티 뒷면", back, mockup("worn-hoodie-back", "white", 256 - 71 * torso_scale, 444, 142 * torso_scale,
                                   "후드 아래 등판에 놓인 기본 로고와 웹사이트 주소", size=hoodie_size,
                                   url_label=(256, round(444 + 50 * torso_scale), round(10 * torso_scale)))),
        ("볼캡 앞면", hat, mockup("worn-cap", "white", 261 - 48 * cap_scale, 155, 96 * cap_scale,
                                "착용한 볼캡 앞판 중앙의 기본 로고", size=cap_size)),
    ]
    groups = []
    for title, symbol, classic in views:
        groups.append(f'''<div class="shop-view"><h3>{title}</h3>
      <div class="shop-variants">
        <figure>{symbol}<figcaption>심벌 단독</figcaption></figure>
        <figure>{classic}<figcaption>기본 로고</figcaption></figure>
      </div></div>''')
    return "\n".join(groups)


def build_catalog(email):
    front = mockup("hoodie", "white", 248, 170, 43, "집업 후드티 앞면의 왼쪽 가슴 로고", featured=True)
    back = mockup("hoodie-back", "white", 138, 197, 142, "집업 후드티 뒷면의 로고와 keep121.co.kr", featured=True, url_label=(209, 247, 10))
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
      <a class="btn btn-dawn" href="#wear">착용 시안 보기 <span aria-hidden="true">↓</span></a>
    </div>
    <figure>
      <div class="shop-pair">{front}{back}</div>
      <figcaption>집업 후드티 <span>앞면 · 뒷면 제작 시안</span></figcaption>
    </figure>
  </div>
</section>
<section class="shop-wear" id="wear" aria-labelledby="wear-title">
  <div class="wrap">
    <h2 id="wear-title">착용 시안</h2>
    <p class="shop-note">AI 모델 착용 시안입니다. 심벌 단독 디자인의 목표 폭은 후드티 등판 14cm, 볼캡 왼쪽 앞 패널 2.5cm입니다.</p>
    <div class="shop-views">{worn_gallery()}</div>
  </div>
</section>
<section class="shop-catalog" id="catalog" aria-labelledby="catalog-title">
  <div class="wrap">
    <h2 id="catalog-title">굿즈 카탈로그</h2>
    <p class="shop-note">심벌 폭은 제작 시안의 목표 치수입니다. 최종 크기와 위치는 선택한 제품의 도안에 맞춰 조정합니다.</p>
    <div class="shop-grid">
{product_cards(email)}
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
    shell = shell.replace("</head>", '  <link rel="stylesheet" href="assets/css/brand-shop.css?v=4">\n</head>')
    write(SHOP, shell)
    write("content/pages/brand-shop.html", build_catalog(email))


if __name__ == "__main__":
    main()
