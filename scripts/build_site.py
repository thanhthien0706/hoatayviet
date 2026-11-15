# -*- coding: utf-8 -*-
"""Generate the static clone (home, category pages, product pages, search)."""
import os, re, json, html, shutil, sys, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'site'
IMG_BASE = 'assets/img/'

PRODUCTS = json.load(open('_raw/products.json', encoding='utf-8'))
SECTIONS = json.load(open('_raw/home_sections.json', encoding='utf-8'))

CATEGORIES = [
    ('tau-du-lich-du-thuyen', 'Tàu Du Lịch – Du Thuyền'),
    ('tau-cho-hang',          'Tàu Chở Hàng'),
    ('thuyen-buom',           'Thuyền Buồm'),
    ('thuyen-dung-di-dao',    'Thuyền (Dùng đi dạo)'),
    ('du-thuyen-hien-dai',    'Du Thuyền Hiện Đại'),
    ('noi-that',              'Nội Thất'),
    ('san-pham-khac',         'Sản Phẩm Khác'),
]
CAT_NAME = dict(CATEGORIES)

MAIN_NAV = [
    ('',                       'Trang chủ',  'index.html',       False),
    ('gioi-thieu',             'Giới thiệu', 'gioi-thieu.html',  False),
    ('shop',                   'Sản phẩm',   'san-pham.html',    False),
    ('tin-tuc',                'Tin tức',    'tin-tuc.html',     False),
    ('lien-he',                'Liên hệ',    'lien-he.html',     False),
    ('huong-dan',              'Hướng dẫn',  'huong-dan.html',   True),
]
GUIDE_SUB = [
    ('Hướng Dẫn Sử Dụng', 'huong-dan-su-dung.html'),
    ('Hướng dẫn mua hàng', 'huong-dan-mua-hang.html'),
]

PHONE = '0908 062 685'
EMAIL = 'hoatayviet.modelship@gmail.com'

# --------------------------------------------------------------------------
# icons (inline SVG, shapes traced from FontAwesome 4.7 / Flatsome fl-icons)
# --------------------------------------------------------------------------
ICONS = {
 'phone':  '<path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57a1 1 0 0 0-1.02.24l-2.2 2.2a15.05 15.05 0 0 1-6.59-6.59l2.2-2.2a1 1 0 0 0 .25-1.02A11.36 11.36 0 0 1 8.5 4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1c0 9.39 7.61 17 17 17a1 1 0 0 0 1-1v-3.5a1 1 0 0 0-1-1z"/>',
 'mail':   '<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/>',
 'pin':    '<path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
 'bars':   '<path d="M3 6h18v2.4H3V6zm0 4.8h18v2.4H3v-2.4zM3 15.6h18V18H3v-2.4z"/>',
 'search': '<path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"/>',
 'user':   '<path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm0 2c-3.33 0-10 1.67-10 5v3h20v-3c0-3.33-6.67-5-10-5z"/>',
 'basket': '<path d="M17 8V6A5 5 0 0 0 7 6v2H3.6a1 1 0 0 0-1 1.1l1.3 10.4a2 2 0 0 0 2 1.75h12.2a2 2 0 0 0 2-1.75l1.3-10.4a1 1 0 0 0-1-1.1zM9 6a3 3 0 0 1 6 0v2H9z"/>',
 'down':   '<path d="M12 15.5 5.5 9l1.4-1.4 5.1 5.1 5.1-5.1L18.5 9z"/>',
 'up':     '<path d="m12 8.5 6.5 6.5-1.4 1.4-5.1-5.1-5.1 5.1L5.5 15z"/>',
 'left':   '<path d="M14.5 18.5 8 12l6.5-6.5L15.9 6.9 10.8 12l5.1 5.1z"/>',
 'right':  '<path d="M9.5 5.5 16 12l-6.5 6.5L8.1 17.1 13.2 12 8.1 6.9z"/>',
 'close':  '<path d="M18.3 5.7 12 12l6.3 6.3-1.4 1.4L10.6 13.4 6.3 17.7 4.9 16.3 11.2 10 4.9 3.7 6.3 2.3l4.3 4.3L16.9 4.3z"/>',
 'file':   '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zm-1 7V3.5L18.5 9z"/>',
}

def icon(name, cls='icon'):
    return ('<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
            % (cls, ICONS[name]))

def e(s):
    return html.escape(s or '', quote=True)

def img_path(url, prefix=''):
    """Map an original uploads URL to the local copy."""
    if not url:
        return prefix + IMG_BASE + 'placeholder.png'
    p = urllib.parse.urlparse(url).path
    if '/wp-content/uploads/' in p:
        return prefix + IMG_BASE + p.split('/wp-content/uploads/', 1)[1]
    return url

# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------
def search_form(prefix, extra_class=''):
    opts = ['<option value="">Tất cả</option>']
    for slug, name in sorted(CATEGORIES, key=lambda c: c[1]):
        opts.append('<option value="%s">%s</option>' % (slug, e(name)))
    return '''<form class="searchform %s" role="search" data-base="%s" action="%stim-kiem.html" method="get">
            <label class="sr-only" for="search-cat-%s">Danh mục</label>
            <select class="search-cats" name="cat" id="search-cat-%s">%s</select>
            <label class="sr-only" for="search-q-%s">Tìm kiếm sản phẩm</label>
            <input class="search-field" type="search" name="s" id="search-q-%s" placeholder="Tìm kiếm sản phẩm" autocomplete="off">
            <button class="search-submit" type="submit" aria-label="Tìm kiếm">%s</button>
          </form>''' % (extra_class, prefix, prefix, extra_class or 'main', extra_class or 'main',
                        ''.join(opts), extra_class or 'main', extra_class or 'main', icon('search'))

def cart_badge(cls=''):
    return '<span class="cart-icon %s"><strong>0</strong></span>' % cls

def header(prefix, active_href=None):
    cat_items = ''.join(
        '<li><a href="%sdanh-muc/%s/index.html">%s</a></li>' % (prefix, slug, e(name))
        for slug, name in CATEGORIES)

    nav_items = []
    for _key, label, href, has_sub in MAIN_NAV:
        cls = []
        if has_sub: cls.append('has-dropdown')
        if href == active_href: cls.append('is-active')
        sub = ''
        caret = ''
        if has_sub:
            caret = icon('down')
            sub = '<ul class="nav-dropdown">%s</ul>' % ''.join(
                '<li><a href="%s%s">%s</a></li>' % (prefix, h, e(t)) for t, h in GUIDE_SUB)
        nav_items.append(
            '<li class="%s"><a href="%s%s"%s>%s%s</a>%s</li>'
            % (' '.join(cls), prefix, href,
               ' aria-expanded="false" aria-haspopup="true"' if has_sub else '',
               e(label), caret, sub))

    return '''<header class="header" id="header">
  <div class="header-bar">
    <div class="container header-row">
      <button class="burger" type="button" data-open-menu aria-label="Mở menu" aria-controls="mobile-menu" aria-expanded="false">{bars}</button>
      <a class="logo" href="{prefix}index.html" rel="home" title="Xưởng Sản Xuất Thuyền Mỹ Nghệ Hoa Tay Việt">
        <img src="{logo}" width="120" height="60" alt="Hoa Tay Việt - Xưởng Sản Xuất Thuyền Mỹ Nghệ">
      </a>
      <nav class="main-nav-wrap" aria-label="Menu chính">
        <ul class="main-nav">{nav}</ul>
      </nav>
      <div class="header-actions">
        <a class="search-toggle" href="{prefix}tim-kiem.html" aria-label="Tìm kiếm sản phẩm">{search_icon}</a>
        <a class="btn btn-call" href="tel:{phone_raw}">{phone_icon}<span>{phone}</span></a>
      </div>
    </div>
  </div>
</header>'''.format(
        prefix=prefix, phone=PHONE, phone_raw=PHONE.replace(' ', ''),
        phone_icon=icon('phone'), search_icon=icon('search'), bars=icon('bars'),
        logo=prefix + IMG_BASE + '2023/06/logo.jpg', nav=''.join(nav_items))


def offcanvas(prefix):
    items = []
    items.append('<li><a href="%sindex.html">Trang chủ</a></li>' % prefix)
    items.append('<li><a href="%sgioi-thieu.html">Giới thiệu</a></li>' % prefix)
    sub = ''.join('<li><a href="%sdanh-muc/%s/index.html">%s</a></li>' % (prefix, s, e(n))
                  for s, n in CATEGORIES)
    items.append(
        '<li><a href="%ssan-pham.html">Sản phẩm'
        '<button class="toggle-sub" type="button" aria-expanded="false" aria-label="Mở danh mục">%s</button>'
        '</a><ul class="sub">%s</ul></li>' % (prefix, icon('down'), sub))
    items.append('<li><a href="%stin-tuc.html">Tin tức</a></li>' % prefix)
    items.append('<li><a href="%slien-he.html">Liên hê</a></li>' % prefix)
    gsub = ''.join('<li><a href="%s%s">%s</a></li>' % (prefix, h, e(t)) for t, h in GUIDE_SUB)
    items.append(
        '<li><a href="%shuong-dan.html">Hướng dẫn'
        '<button class="toggle-sub" type="button" aria-expanded="false" aria-label="Mở mục con">%s</button>'
        '</a><ul class="sub">%s</ul></li>' % (prefix, icon('down'), gsub))
    items.append('<li><a href="%stai-khoan.html">Đăng nhập</a></li>' % prefix)

    return '''<div class="offcanvas-backdrop" hidden-aria></div>
<aside class="offcanvas" id="mobile-menu" aria-hidden="true" aria-label="Menu">
  <div class="offcanvas-head">
    <strong>Menu</strong>
    <button class="offcanvas-close" type="button" data-close-menu aria-label="Đóng menu">%s</button>
  </div>
  %s
  <ul class="offcanvas-nav">%s</ul>
</aside>''' % (icon('close'), search_form(prefix, 'in-offcanvas'), ''.join(items))


def footer(prefix):
    cats = ''.join('<li><a href="%sdanh-muc/%s/index.html">%s</a></li>' % (prefix, sl, e(n))
                   for sl, n in CATEGORIES)
    return '''<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-main">
      <h2 class="footer-brand">Hoa Tay Việt</h2>
      <p>Công ty TNHH Hoa Tay Việt<br>199 ấp 1B, Phước Thái, Long Thành, Đồng Nai</p>
      <p><a href="tel:0908062685">0908 062 685</a> · <a href="tel:+84352344343">84 35234 4343</a> (Ms Tram)<br>
         <a href="mailto:hoatayviet.modelship@gmail.com">hoatayviet.modelship@gmail.com</a><br>
         <a href="mailto:lywoodenmodelboat@gmail.com">lywoodenmodelboat@gmail.com</a></p>
    </div>
    <div>
      <h2 class="footer-title">Sản phẩm</h2>
      <ul class="footer-list footer-cats">{cats}</ul>
      <ul class="footer-links">
        <li><a href="{prefix}gioi-thieu.html">Giới thiệu</a></li>
        <li><a href="{prefix}huong-dan-mua-hang.html">Hướng dẫn mua hàng</a></li>
        <li><a href="{prefix}lien-he.html">Liên hệ</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom"><div class="container">© 2026 Hoa Tay Việt</div></div>
  <a class="back-to-top" href="#top" aria-label="Lên đầu trang">{up}</a>
  <a class="call-bar" href="tel:0908062685">{phone_icon}<span>Gọi ngay {phone}</span></a>
</footer>'''.format(cats=cats, prefix=prefix, up=icon('up'), phone_icon=icon('phone'), phone=PHONE)


def page(title, body_class, content, prefix, desc='', active=None):
    return '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{prefix}{img}2023/06/cropped-logo-32x32.jpg" sizes="32x32">
<link rel="apple-touch-icon" href="{prefix}{img}2023/06/cropped-logo-180x180.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Roboto+Condensed:wght@700&display=swap">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>
<body class="{body_class}" id="top">
<a class="skip-link" href="#main">Bỏ qua, đến nội dung</a>
{header}
<main id="main">
{content}
</main>
{footer}
{offcanvas}
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
'''.format(title=e(title), desc=e(desc), prefix=prefix, img=IMG_BASE,
           body_class=body_class, header=header(prefix, active),
           content=content, footer=footer(prefix), offcanvas=offcanvas(prefix))


# --------------------------------------------------------------------------
# product card
# --------------------------------------------------------------------------
BY_SLUG = {p['slug']: p for p in PRODUCTS}

def card(slug, name=None, image=None, hover=None, prefix=''):
    p = BY_SLUG.get(slug, {})
    name  = name  or p.get('name') or slug
    image = image or p.get('thumb') or (p.get('gallery') or [None])[0]
    gal   = p.get('gallery') or []
    if not hover:
        hover = next((g for g in gal if g != image), None)

    href = '%ssp/%s/index.html' % (prefix, slug)
    meta = ' · '.join(x for x in [p.get('sku'), (p.get('size') or '').split(' / ')[0]] if x)
    return '''<article class="product-card">
  <a class="product-link" href="{href}">
    <span class="product-media"><img src="{img}" alt="{alt}" loading="lazy" decoding="async"></span>
    <span class="product-name">{name}</span>
    {meta}
  </a>
</article>'''.format(href=href, img=img_path(image, prefix), alt=e(name), name=e(name),
                     meta=('<span class="product-meta-line">%s</span>' % e(meta)) if meta else '')


# --------------------------------------------------------------------------
# home
# --------------------------------------------------------------------------
HERO_PHOTOS = [
    ('2022/11/z3487042728597_daf745f2e9f46dcaf6295ec7df19df7d-768x579-1.jpg', 'Mô hình tàu Caledonian MacBrayne'),
    ('2022/11/z3150831024697_8d7e0c59a1b1af27a544a517bb227612.jpg',           'Mô hình du thuyền Hoa Tay Việt'),
    ('2022/11/366219_n-768x613-1.gif',                                        'Mô hình thuyền buồm thủ công'),
]

def section_block(title, href, cards, count=None, variant=''):
    grid = 'grid-products' if not variant else 'grid-feature ' + variant
    return '''<section class="catalog-section {tone}">
  <div class="container">
    <div class="section-head">
      <h2 class="section-title"><a href="{href}">{title}</a></h2>
      <a class="section-more" href="{href}">Xem tất cả{count}</a>
    </div>
    <div class="{grid}">{cards}</div>
  </div>
</section>'''.format(href=href, title=e(title), cards=cards, grid=grid,
                      tone='tone-dark' if 'dark' in variant else ('tone-tint' if 'tint' in variant else ''),
                      count=(' (%d)' % count) if count else '')

def build_home():
    src, alt = HERO_PHOTOS[0]
    photo = '<img src="%s%s" alt="%s" width="768" height="579">' % (IMG_BASE, src, e(alt))

    counts = {sl: sum(1 for p in PRODUCTS if p['categorySlug'] == sl) for sl, _ in CATEGORIES}
    cat_row = ''.join('<li><a href="danh-muc/%s/index.html">%s<span>%d</span></a></li>'
                      % (sl, e(n), counts[sl]) for sl, n in CATEGORIES)

    hero = '''<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <h1 class="hero-title">Mô hình tàu thuyền <em>làm thủ công</em></h1>
      <p class="hero-deck">Xưởng Hoa Tay Việt chế tác tàu du lịch, du thuyền, thuyền buồm và nội thất gỗ, từng chi tiết làm bằng tay.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="san-pham.html">Xem sản phẩm</a>
        <a class="btn btn-outline" href="tel:0908062685">{phone_icon}<span>Gọi {phone}</span></a>
      </div>
    </div>
    <figure class="hero-media">{photo}<figcaption>{caption}</figcaption></figure>
  </div>
</section>
<nav class="category-row" aria-label="Danh mục sản phẩm">
  <div class="container"><ul>{cat_row}</ul></div>
</nav>'''.format(photo=photo, caption=e(alt), cat_row=cat_row, phone=PHONE, phone_icon=icon('phone'))

    blocks = [hero]
    for idx, sec in enumerate(SECTIONS):
        title = sec['title'] or ''
        cat_slug = next((s for s, n in CATEGORIES if n == title), None)
        title_href = 'danh-muc/%s/index.html' % cat_slug if cat_slug else 'san-pham.html'
        cards = []
        for pr in sec['products']:
            slug = (pr['url'] or '').rstrip('/').rsplit('/', 1)[-1]
            cards.append(card(slug, pr['name'], pr['image'], pr['hoverImage']))
        # layout rhythm: feature-left, tint row, dark feature-right, ...
        variant, keep = [('feature', 5), ('tint', 4), ('feature flip dark', 5),
                         ('tint', 2), ('feature flip', 5), ('tint', 4)][idx % 6]
        tone = ''
        if idx % 6 in (1, 3, 5):
            variant, tone = '', 'tint'
        sect = section_block(title, title_href, ''.join(cards[:keep]),
                             counts.get(cat_slug) if cat_slug else None, variant)
        if tone:
            sect = sect.replace('class="catalog-section "', 'class="catalog-section tone-tint"')
        blocks.append(sect)

    blocks.append('''<section class="contact-band">
  <div class="container contact-grid">
    <div>
      <h2>Chọn mẫu, gọi xưởng để nhận báo giá</h2>
      <p>Giá từng mô hình tuỳ kích thước và yêu cầu. Xưởng trả lời trong ngày.</p>
    </div>
    <div class="contact-actions">
      <a class="contact-phone" href="tel:0908062685">{phone}</a>
      <a class="contact-mail" href="mailto:{email}">{email}</a>
    </div>
  </div>
</section>'''.format(phone=PHONE, email=EMAIL))

    return page('Trang Chủ - Xưởng Sản Xuất Thuyền Mỹ Nghệ Hoa Tay Việt',
                'is-home', '\n'.join(blocks), '',
                desc='Xưởng sản xuất thuyền mỹ nghệ Hoa Tay Việt — mô hình tàu, du thuyền, thuyền buồm và nội thất gỗ thủ công.',
                active='index.html')


# --------------------------------------------------------------------------
# category + product + listing pages
# --------------------------------------------------------------------------
def build_category(slug, name):
    prefix = '../../'
    items = [p for p in PRODUCTS if p['categorySlug'] == slug]
    cards = ''.join(card(p['slug'], prefix=prefix) for p in items)
    body = '' if items else '<p class="empty-note">Chưa có sản phẩm trong danh mục này.</p>'

    content = '''<div class="page-wrap">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="{p}index.html">Trang chủ</a><span>/</span>
      <a href="{p}san-pham.html">Sản phẩm</a><span>/</span>{name}
    </nav>
    <div class="section-head">
      <h1 class="section-title">{name}</h1>
      <span class="section-more">{count} sản phẩm</span>
    </div>
    <div class="grid-products">{cards}</div>
    {body}
  </div>
</div>'''.format(p=prefix, name=e(name), count=len(items), cards=cards, body=body)

    return page('%s - Hoa Tay Việt' % name, 'is-category', content, prefix,
                desc='Danh mục %s tại Hoa Tay Việt.' % name, active='san-pham.html')


def build_product(p):
    prefix = '../../'
    gal = p['gallery'] or []
    main = gal[0] if gal else p['thumb']

    thumbs = ''.join(
        '<button type="button" role="tab" aria-selected="%s" data-full="%s" data-alt="%s">'
        '<img src="%s" alt="" loading="lazy"></button>'
        % ('true' if i == 0 else 'false', img_path(g, prefix), e(p['name']), img_path(g, prefix))
        for i, g in enumerate(gal)) if len(gal) > 1 else ''

    specs = []
    if p['sku']:   specs.append(('Mã sản phẩm', p['sku']))
    if p['size']:  specs.append(('Kích thước',  p['size']))
    specs.append(('Giá', p['price'] or 'Liên hệ'))
    spec_html = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(k), e(v)) for k, v in specs)

    body_txt = ''.join('<p>%s</p>' % e(l) for l in p['body'])
    desc_imgs = ''.join('<img src="%s" alt="" loading="lazy">' % img_path(u, prefix)
                        for u in p['descImages'])
    desc_block = ''
    if body_txt or desc_imgs:
        desc_block = ('<div class="product-desc"><h2 class="section-title">Mô tả</h2>'
                      '<div>%s%s</div></div>' % (body_txt, desc_imgs))

    cat_slug = p['categorySlug']
    cat_name = CAT_NAME.get(cat_slug, p['category'] or '')

    related = [q for q in PRODUCTS if q['categorySlug'] == cat_slug and q['slug'] != p['slug']][:4]
    rel_html = ''
    if related:
        rel_html = '''<section class="catalog-section">
  <div class="container">
    <div class="section-head"><h2 class="section-title">Sản phẩm tương tự</h2></div>
    <div class="grid-products">%s</div>
  </div>
</section>''' % ''.join(card(q['slug'], prefix=prefix) for q in related)

    content = '''<div class="page-wrap">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="{p}index.html">Trang chủ</a><span>/</span>
      <a href="{p}danh-muc/{cslug}/index.html">{cname}</a><span>/</span>{name}
    </nav>

    <div class="row product-detail">
      <div class="gallery-col">
        <div class="gallery-main"><img src="{main}" alt="{name}"></div>
        <div class="gallery-thumbs" role="tablist" aria-label="Ảnh sản phẩm">{thumbs}</div>
      </div>

      <div class="info-col">
        <h1>{name}</h1>
        <dl class="spec-list">{specs}</dl>
        <a class="btn btn-cta btn-buy" href="tel:0908062685">{phone_icon}<span>Gọi báo giá 0908 062 685</span></a>
        <p class="product-meta">Danh mục: <a href="{p}danh-muc/{cslug}/index.html">{cname}</a></p>
        {desc}
      </div>
    </div>
  </div>
  {rel}
</div>'''.format(p=prefix, cslug=cat_slug, cname=e(cat_name), name=e(p['name']),
                 main=img_path(main, prefix), thumbs=thumbs, specs=spec_html,
                 desc=desc_block, rel=rel_html, phone_icon=icon('phone'))

    return page('%s - Hoa Tay Việt' % p['name'], 'is-product', content, prefix,
                desc='%s — %s. %s' % (p['name'], cat_name, p['size'] or ''),
                active='san-pham.html')


def build_all_products():
    prefix = ''
    blocks = []
    for slug, name in CATEGORIES:
        items = [p for p in PRODUCTS if p['categorySlug'] == slug]
        if not items:
            continue
        blocks.append(section_block(name, 'danh-muc/%s/index.html' % slug,
                                    ''.join(card(p['slug']) for p in items), len(items)))

    content = ('<div class="page-wrap"><div class="container"><nav class="breadcrumb">'
               '<a href="index.html">Trang chủ</a><span>/</span>Sản phẩm</nav></div>'
               + '\n'.join(blocks) + '</div>')
    return page('Sản phẩm - Hoa Tay Việt', 'is-shop', content, prefix,
                desc='Toàn bộ %d sản phẩm của Hoa Tay Việt.' % len(PRODUCTS),
                active='san-pham.html')


def build_search():
    content = '''<div class="page-wrap"><div class="container">
  <nav class="breadcrumb"><a href="index.html">Trang chủ</a><span>/</span>Tìm kiếm</nav>
  <h1 id="search-heading">Kết quả tìm kiếm</h1>
  </div>
<div class="container">
  <form class="searchform" role="search" action="tim-kiem.html" method="get">
    <label class="sr-only" for="q">Tìm kiếm sản phẩm</label>
    <input class="search-field" type="search" name="s" id="q" placeholder="Tên hoặc mã sản phẩm" autocomplete="off">
    <button class="btn btn-primary" type="submit">Tìm</button>
  </form>
  <div class="grid-products" id="search-results"></div>
  <p class="empty-note" id="search-empty" hidden>Không tìm thấy sản phẩm phù hợp.</p>
</div></div>
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var term = (q.get('s') || '').trim().toLowerCase();
  var cat  = q.get('cat') || '';
  var head = document.getElementById('search-heading');
  head.textContent = term ? 'Kết quả cho “' + term + '”' : 'Tất cả sản phẩm';

  function strip(s) {
    return (s || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/đ/g, 'd').toLowerCase();
  }

  fetch('assets/data/products.json').then(function (r) { return r.json(); }).then(function (items) {
    var t = strip(term);
    var out = items.filter(function (p) {
      if (cat && p.categorySlug !== cat) return false;
      if (!t) return true;
      return strip(p.name).indexOf(t) > -1 || strip(p.sku).indexOf(t) > -1 || strip(p.category).indexOf(t) > -1;
    });
    var box = document.getElementById('search-results');
    if (!out.length) { document.getElementById('search-empty').hidden = false; return; }
    box.innerHTML = out.map(function (p) {
      var href = 'sp/' + p.slug + '/index.html';
      return '<article class="product-card"><a class="product-link" href="' + href + '">'
        + '<span class="product-media"><img src="' + p.thumb + '" alt="' + p.name + '" loading="lazy"></span>'
        + '<span class="product-name">' + p.name + '</span></a></article>';
    }).join('');
  });
})();
</script>'''
    return page('Tìm kiếm - Hoa Tay Việt', 'is-search', content, '', active='san-pham.html')


def build_stub(title, heading, body, filename, active=None):
    content = '''<div class="page-wrap"><div class="container">
  <nav class="breadcrumb"><a href="index.html">Trang chủ</a><span>/</span>{h}</nav>
  <h1>{h}</h1>
  {b}
</div></div>'''.format(h=e(heading), b=body)
    return page(title, 'is-page', content, '', active=active)


# --------------------------------------------------------------------------
def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)

def main():
    n = 0
    write('index.html', build_home()); n += 1

    for slug, name in CATEGORIES:
        write('danh-muc/%s/index.html' % slug, build_category(slug, name)); n += 1

    for p in PRODUCTS:
        write('sp/%s/index.html' % p['slug'], build_product(p)); n += 1

    write('san-pham.html', build_all_products()); n += 1
    write('tim-kiem.html', build_search()); n += 1

    contact = '''<p><strong>CÔNG TY TNHH HOA TAY VIỆT</strong></p>
<p>Địa chỉ: 199 ấp 1B, Phước Thái, Long Thành, Đồng Nai</p>
<p>Điện thoại: <a href="tel:0908062685">0908 062 685</a> — 84 35234 4343 (Ms Tram)</p>
<p>Email: <a href="mailto:hoatayviet.modelship@gmail.com">hoatayviet.modelship@gmail.com</a></p>'''
    intro = '''<p>Hoa Tay Việt là xưởng sản xuất thuyền mỹ nghệ, chuyên xuất khẩu ngành hàng thủ công mỹ nghệ
với bề dày kinh nghiệm trong ngành thủ công làm bằng tay.</p>
<p>Sản phẩm gồm mô hình tàu du lịch, du thuyền, tàu chở hàng, thuyền buồm, thuyền dùng đi dạo và nội thất gỗ.</p>'''
    todo = '<p>Nội dung trang này chưa được thu thập (máy chủ gốc đang trả về lỗi 500).</p>'

    for title, heading, body, fn in [
        ('Giới thiệu - Hoa Tay Việt',        'Giới thiệu',          intro,   'gioi-thieu.html'),
        ('Liên hệ - Hoa Tay Việt',           'Liên hệ',             contact, 'lien-he.html'),
        ('Tin tức - Hoa Tay Việt',           'Tin tức',             todo,    'tin-tuc.html'),
        ('Hướng dẫn - Hoa Tay Việt',         'Hướng dẫn',           todo,    'huong-dan.html'),
        ('Hướng dẫn sử dụng - Hoa Tay Việt', 'Hướng Dẫn Sử Dụng',   todo,    'huong-dan-su-dung.html'),
        ('Hướng dẫn mua hàng - Hoa Tay Việt','Hướng dẫn mua hàng',  todo,    'huong-dan-mua-hang.html'),
        ('Giỏ hàng - Hoa Tay Việt',          'Giỏ hàng',            '<p>Chưa có sản phẩm trong giỏ hàng.</p>', 'gio-hang.html'),
        ('Tài khoản - Hoa Tay Việt',         'Đăng nhập',           todo,    'tai-khoan.html'),
    ]:
        write(fn, build_stub(title, heading, body, fn)); n += 1

    # product data for the search page
    slim = [{'slug': p['slug'], 'name': p['name'], 'sku': p['sku'] or '',
             'size': p['size'] or '', 'price': p['price'],
             'category': p['category'] or '', 'categorySlug': p['categorySlug'] or '',
             'thumb': img_path(p['thumb'])} for p in PRODUCTS]
    write('assets/data/products.json', json.dumps(slim, ensure_ascii=False, indent=1))

    print('pages written:', n)
    print('products     :', len(PRODUCTS))
    print('categories   :', len(CATEGORIES))

main()
