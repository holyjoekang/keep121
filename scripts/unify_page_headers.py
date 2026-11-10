from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
for name,photo in [('solution','photo-1639763703351-c27defbb51b1'),('business','photo-1544620347-c4fd4a3d5957')]:
 p=r/'content/pages'/f'{name}.html';s=p.read_text();s=s.replace('<section class="v-hero">',f'<section class="v-hero photo-hero" style="--hero-photo:url(\'https://images.unsplash.com/{photo}?auto=format&amp;fit=crop&amp;w=1800&amp;q=80\')">',1);p.write_text(s)
 p=r/f'{name}.html';s=p.read_text().replace('<body class="product-aligned">','<body>')
 if 'assets/css/photo-headers.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="assets/css/photo-headers.css">\n</head>')
 p.write_text(s)
for name in ['keeptrip','modoo']:
 p=r/'content/pages'/f'{name}.html';s=p.read_text();s=re.sub(r'^<section[^>]*>.*?<strong>사업계획 업데이트 · 2026\.11</strong>.*?</section>\s*','',s,count=1,flags=re.S)
 if name=='modoo':s=s.replace('<section class="page-hero">','<section class="page-hero has-photo" style="--bg:url(\'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&amp;fit=crop&amp;w=1800&amp;q=80\')">',1)
 p.write_text(s)
(r/'assets/css/photo-headers.css').write_text('''/* Match the site's photo-backed page headers; body sections retain their own palette. */
.vp .v-hero.photo-hero{background:linear-gradient(90deg,rgba(14,18,38,.96),rgba(14,18,38,.87) 45%,rgba(14,18,38,.63)),var(--hero-photo) center/cover no-repeat;background-color:#0e1226;color:white;padding-top:140px;padding-bottom:72px}
.vp .photo-hero h1{color:white}.vp .photo-hero .v-k{color:#a8dcc5}.vp .photo-hero .v-lead{color:#d6dcef}.vp .photo-hero .btn-primary{background:white;color:#23306b}.vp .photo-hero .btn-ghost{color:white;border-color:#9ba6c1;background:transparent}.vp .photo-hero .btn-ghost:hover{background:#ffffff20}.vp .photo-hero .v-status span{background:#10172dc9;color:#edf1ff;border-color:#7e8ba8}.vp .photo-hero .s-journey{color:#141a2e}.vp .photo-hero .s-journey p{color:#5e667d}
@media(max-width:800px){.vp .v-hero.photo-hero{padding-top:135px;padding-bottom:50px;background:linear-gradient(180deg,rgba(14,18,38,.88),rgba(14,18,38,.96)),var(--hero-photo) center/cover no-repeat;background-color:#0e1226}}
''')
