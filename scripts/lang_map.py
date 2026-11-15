# -*- coding: utf-8 -*-
"""Vietnamese <-> English page mapping shared by build_site.py and build_en.py.

Every Vietnamese page has an English twin:

    gio-hang.html                -> cart.html
    danh-muc/<vi>/index.html     -> category/<en>/index.html
    sp/<vi>/index.html           -> product/<en>/index.html
"""
import os

# top-level pages (Vietnamese path -> English path)
ROOT_PAGES = {
    'index.html':             'home.html',
    'gioi-thieu.html':        'about.html',
    'san-pham.html':          'products.html',
    'tin-tuc.html':           'news.html',
    'lien-he.html':           'contact.html',
    'huong-dan.html':         'guide.html',
    'huong-dan-su-dung.html': 'user-guide.html',
    'huong-dan-mua-hang.html': 'buying-guide.html',
    'gio-hang.html':          'cart.html',
    'thanh-toan.html':        'checkout.html',
    'tai-khoan.html':         'account.html',
    'tim-kiem.html':          'search.html',
}

CATEGORY_SLUGS = {
    'tau-du-lich-du-thuyen': 'cruise-ships-yachts',
    'tau-cho-hang':          'cargo-ships',
    'thuyen-buom':           'sailing-boats',
    'thuyen-dung-di-dao':    'leisure-boats',
    'du-thuyen-hien-dai':    'modern-yachts',
    'noi-that':              'furniture',
    'san-pham-khac':         'other-products',
}

PRODUCT_SLUGS = {
    'american-sconut':          'american-sconut',
    'anteo':                    'anteo',
    'ban-go':                   'wooden-table',
    'ban-hinh-thuyen':          'boat-shaped-table',
    'ban-hoc-sinh':             'student-desk',
    'batterses-mo-hinh-thuyen': 'batterses-boat-model',
    'cannon':                   'cannon',
    'christian-radich-model':   'christian-radich-model',
    'ky-niem-chuong':           'commemorative-medal',
    'lagoon-450-yacht-model':   'lagoon-450-yacht-model',
    'laustrl-mo-hinh-tau':      'laustrl-ship-model',
    'mo-hinh-tau-astor':        'astor-ship-model',
    'mo-hinh-tau-asuka-ll':     'asuka-ll-ship-model',
    'mo-hinh-tau-erzherzog-franz-ferdinand': 'erzherzog-franz-ferdinand-ship-model',
    'mo-hinh-tau-mississippi':  'mississippi-ship-model',
    'mo-hinh-tau-thuyen':       'broom-35-european-ship-model',
    'mo-hinh-thuen':            'callista-boat-model',
    'mo-hinh-thuyen-batavia':   'batavia-boat-model',
    'mo-hinh-thuyen-buom-2':    'wasa-sailing-boat-model',
    'mo-hinh-thuyen-buom':      'htv-sailing-boat-model',
    'mo-hinh-thuyen':           'ha-long-sailing-boat-model',
    'model-ships-thorsen-axel-1810-na-uy': 'model-ships-thorsen-axel-1810-norway',
    'noi-that-go-tram':         'melaleuca-dressing-table',
    'quay-ba':                  'bar-counter',
    'silver-dee':               'silver-dee',
    'star-1-mo-hinh-thuyen':    'star-1-boat-model',
    'thuyen-my-nghe':           'la-jacinthe-art-boat',
    'tranh-thuyen-2':           'boat-painting-2',
    'tranh-thuyen':             'boat-painting',
    'tu-go':                    'wooden-cabinet',
    'victory':                  'victory',
    'xuong-go':                 'wooden-canoe',
}

# Vietnamese product titles that have to be translated (the rest are proper
# names of ships and stay as they are).
PRODUCT_NAMES_EN = {
    'Bàn Gỗ': 'Wooden Table',
    'BÀN HÌNH THUYỀN': 'BOAT-SHAPED TABLE',
    'BÀN HỌC SINH': 'STUDENT DESK',
    'Kỷ niệm chương': 'Commemorative Medal',
    'THUYỀN BUỒM HTV': 'HTV SAILING BOAT',
    'Thuyền buồm HẠ LONG': 'HA LONG Sailing Boat',
    'BÀN TRANG ĐIỂM': 'DRESSING TABLE',
    'QUẦY BA': 'BAR COUNTER',
    'TRANH THUYỀN': 'BOAT PAINTING',
    'Tủ Gỗ': 'Wooden Cabinet',
    'XUỒNG': 'CANOE',
}

CATEGORY_NAMES_EN = {
    'Tàu Du Lịch – Du Thuyền': 'Cruise Ships – Yachts',
    'Tàu Chở Hàng': 'Cargo Ships',
    'Thuyền Buồm': 'Sailing Boats',
    'Thuyền (Dùng đi dạo)': 'Boats (For Leisure)',
    'Du Thuyền Hiện Đại': 'Modern Yachts',
    'Nội Thất': 'Furniture',
    'Sản Phẩm Khác': 'Other Products',
}


def build_path_map():
    """Vietnamese site-relative path -> English site-relative path."""
    m = dict(ROOT_PAGES)
    for vi, en in CATEGORY_SLUGS.items():
        m['danh-muc/%s/index.html' % vi] = 'category/%s/index.html' % en
    for vi, en in PRODUCT_SLUGS.items():
        m['sp/%s/index.html' % vi] = 'product/%s/index.html' % en
    return m


PATH_MAP = build_path_map()
REV_MAP = {en: vi for vi, en in PATH_MAP.items()}


def counterpart(path, lang):
    """The `lang` ('vi' or 'en') version of a site-relative page path."""
    if lang == 'en':
        return PATH_MAP.get(path, path)
    return REV_MAP.get(path, path)


def rel(target, from_path):
    """Relative URL of `target` as seen from the page at `from_path`."""
    return os.path.relpath(target, os.path.dirname(from_path) or '.').replace(os.sep, '/')
