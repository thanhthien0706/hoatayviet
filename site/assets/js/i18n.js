/* Hoa Tay Việt — language switcher (Tiếng Việt / English).
   The pages are authored in Vietnamese. English is applied client-side by
   swapping text nodes and a few attributes through the dictionary below, so
   switching back restores the original text exactly. Choice is kept in
   localStorage. */
(function () {
  'use strict';

  var KEY = 'hty-lang';

  var DICT = {
    // top bar / header
    'Hướng dẫn mua hàng': 'Buying guide',
    'Tìm kiếm sản phẩm': 'Search products',
    'Tìm kiếm': 'Search',
    'Tất cả': 'All',
    'Danh mục': 'Category',
    'Danh mục sản phẩm': 'Product categories',
    'Tài khoản': 'Account',
    'Giỏ hàng': 'Cart',
    'Giỏ hàng /': 'Cart /',
    'Menu chính': 'Main menu',
    'Mở menu': 'Open menu',
    'Đóng menu': 'Close menu',
    'Mở danh mục': 'Open categories',
    'Mở mục con': 'Open submenu',
    'Lên đầu trang': 'Back to top',
    // main nav
    'Trang chủ': 'Home',
    'Giới thiệu': 'About us',
    'Sản phẩm': 'Products',
    'Tin tức': 'News',
    'Liên hệ': 'Contact',
    'Liên hê': 'Contact',
    'Hướng dẫn': 'Guide',
    'Hướng Dẫn Sử Dụng': 'User guide',
    'Hướng dẫn sử dụng': 'User guide',
    'Đăng nhập': 'Log in',
    // categories
    'Tàu Du Lịch – Du Thuyền': 'Cruise Ships – Yachts',
    'Tàu Chở Hàng': 'Cargo Ships',
    'Thuyền Buồm': 'Sailing Boats',
    'Thuyền (Dùng đi dạo)': 'Boats (For Leisure)',
    'Thuyền (Bơi Được)': 'Boats (Floatable)',
    'Du Thuyền Hiện Đại': 'Modern Yachts',
    'Nội Thất': 'Furniture',
    'Sản Phẩm Khác': 'Other Products',
    'Tàu Du Lịch': 'Cruise Ships',
    'Du Thuyền': 'Yachts',
    'Khung Mica': 'Acrylic Frames',
    // footer
    'Thông tin liên hệ': 'Contact information',
    'CÔNG TY TNHH HOA TAY VIỆT': 'HOA TAY VIET CO., LTD',
    '199 ấp 1B, Phước Thái, Long Thành, Đồng Nai': '199 Hamlet 1B, Phuoc Thai, Long Thanh, Dong Nai',
    '84 35234 4343 – Contact (Ms Tram)': '84 35234 4343 – Contact (Ms Tram)',
    'Bản đồ Hoa Tay Việt': 'Hoa Tay Viet map',
    'Chào mừng quý khách đến với đại gia đình HOA TAY VIỆT.': 'Welcome to the HOA TAY VIET family.',
    'Công ty chúng tôi chuyên xuất khẩu ngành hàng thủ công mỹ nghệ có bề dày kinh nghiệm trong ngành thủ công làm bằng tay':
      'We export handcrafted art and craft goods and have long experience in the handmade craft trade.',
    'Gọi ngay': 'Call now',
    // home / slider
    'Ảnh nổi bật': 'Featured images',
    'Ảnh trước': 'Previous image',
    'Ảnh sau': 'Next image',
    'Chọn ảnh': 'Choose image',
    'Mô hình tàu Caledonian MacBrayne': 'Caledonian MacBrayne ship model',
    'Mô hình du thuyền Hoa Tay Việt': 'Hoa Tay Viet yacht model',
    'Mô hình thuyền buồm thủ công': 'Handmade sailing boat model',
    'Xưởng sản xuất thuyền mỹ nghệ': 'Art boat workshop',
    'Xưởng Sản Xuất Thuyền Mỹ Nghệ Hoa Tay Việt': 'Hoa Tay Viet Art Boat Workshop',
    'Trang Chủ': 'Home',
    // listing / product
    'Chưa có sản phẩm trong danh mục này.': 'There are no products in this category yet.',
    'Mã sản phẩm': 'Product code',
    'Kích thước': 'Size',
    'Kích thước:': 'Size:',
    'Giá': 'Price',
    'Liên hệ': 'Contact us',
    'LH': 'Contact',
    'Mua ngay': 'Buy now',
    'Gọi điện xác nhận và giao hàng tận nơi': 'Call to confirm, delivered to your door',
    'Danh mục:': 'Category:',
    'Mô tả': 'Description',
    'Sản phẩm tương tự': 'Related products',
    'Ảnh sản phẩm': 'Product images',
    // cart & checkout
    'Số lượng': 'Quantity', 'Giảm': 'Decrease', 'Tăng': 'Increase',
    'Thêm vào giỏ hàng': 'Add to cart',
    'Thanh toán khi nhận hàng hoặc quét mã QR': 'Cash on delivery or pay by QR code',
    'Đã thêm vào giỏ hàng.': 'Added to cart.',
    'Xem giỏ hàng': 'View cart',
    'Tiếp tục mua sắm': 'Continue shopping',
    'Hãy chọn những mô hình thuyền bạn yêu thích để bắt đầu.': 'Pick the boat models you love to get started.',
    'Tổng giỏ hàng': 'Cart totals',
    'Tạm tính': 'Subtotal',
    'Tổng cộng': 'Total',
    'Xóa': 'Remove',
    'Tiến hành thanh toán': 'Proceed to checkout',
    'Sản phẩm giá “Liên hệ” chưa được tính vào tổng, chúng tôi sẽ báo giá khi xác nhận đơn.':
      'Items priced “Contact us” are not included in the total; we will quote the price when confirming your order.',
    'Thanh toán': 'Checkout',
    'Thông tin giao hàng': 'Delivery information',
    'Họ và tên *': 'Full name *',
    'Số điện thoại *': 'Phone number *',
    'Email': 'Email',
    'Địa chỉ nhận hàng *': 'Delivery address *',
    'Ghi chú': 'Notes',
    'Phương thức thanh toán': 'Payment method',
    'Thanh toán khi nhận hàng (COD)': 'Cash on delivery (COD)',
    'Trả tiền mặt cho nhân viên giao hàng khi nhận sản phẩm.': 'Pay the courier in cash when you receive your order.',
    'Thanh toán bằng mã QR': 'Pay by QR code',
    'Quét mã bằng ứng dụng ngân hàng hoặc ví điện tử.': 'Scan the code with your banking app or e-wallet.',
    'Mã QR thanh toán (demo)': 'Payment QR code (demo)',
    'Ngân hàng': 'Bank', 'Số tài khoản': 'Account number', 'Chủ tài khoản': 'Account holder',
    'Đây là mã QR demo, chưa dùng để nhận tiền thật.': 'This is a demo QR code and cannot receive real payments.',
    'Đơn hàng của bạn': 'Your order',
    'Phí vận chuyển': 'Shipping',
    'Báo khi xác nhận': 'Quoted on confirmation',
    'Đặt hàng': 'Place order',
    'Đặt hàng thành công!': 'Order placed successfully!',
    'Mã đơn hàng:': 'Order code:',
    'Nội dung chuyển khoản:': 'Transfer note:',
    'Về trang chủ': 'Back to home',
    'Vui lòng nhập họ và tên.': 'Please enter your full name.',
    'Số điện thoại không hợp lệ.': 'Invalid phone number.',
    'Email không hợp lệ.': 'Invalid email address.',
    'Vui lòng nhập địa chỉ nhận hàng.': 'Please enter your delivery address.',
    'Vui lòng quét mã QR bên dưới để thanh toán. Chúng tôi sẽ xác nhận đơn ngay khi nhận được tiền.':
      'Please scan the QR code below to pay. We will confirm your order as soon as payment is received.',
    'Bạn sẽ thanh toán bằng tiền mặt khi nhận hàng. Nhân viên sẽ liên hệ xác nhận đơn qua điện thoại.':
      'You will pay in cash on delivery. Our staff will call you to confirm the order.',
    'Báo giá khi xác nhận': 'Quoted on confirmation',
    // search
    'Kết quả tìm kiếm': 'Search results',
    'Tất cả sản phẩm': 'All products',
    'Không tìm thấy sản phẩm phù hợp.': 'No matching products found.',
    // pages
    'Địa chỉ:': 'Address:',
    'Điện thoại:': 'Phone:',
    'Chưa có sản phẩm trong giỏ hàng.': 'Your cart is empty.',
    'Nội dung trang này chưa được thu thập (máy chủ gốc đang trả về lỗi 500).':
      'The content of this page has not been collected yet (the origin server returns error 500).',
    'Hoa Tay Việt là xưởng sản xuất thuyền mỹ nghệ, chuyên xuất khẩu ngành hàng thủ công mỹ nghệ với bề dày kinh nghiệm trong ngành thủ công làm bằng tay.':
      'Hoa Tay Viet is an art boat workshop that exports handcrafted goods and has long experience in the handmade craft trade.',
    'Sản phẩm gồm mô hình tàu du lịch, du thuyền, tàu chở hàng, thuyền buồm, thuyền dùng đi dạo và nội thất gỗ.':
      'Our products include cruise ship models, yachts, cargo ships, sailing boats, leisure boats and wooden furniture.',
    // a few product description lines
    'Qúy khách liên hệ để có giá sỉ.': 'Please contact us for wholesale prices.',
    'Chúng tôi là nhà sản xuất, trên đây là giá bán lẻ.Qúy khách liên hệ để có giá sỉ.':
      'We are the manufacturer; the above is the retail price. Please contact us for wholesale prices.',
    'GIÁ BÁN LẼ: LH': 'RETAIL PRICE: Contact us',
    'BÀN HỌC SINH GỖ THÔNG': 'PINE WOOD STUDENT DESK',
    'BÀN TRANG ĐIỂM GỖ TRÀM': 'MELALEUCA WOOD DRESSING TABLE'
  };

  var PATTERNS = [
    [/^(\d+) sản phẩm$/, '$1 products'],
    [/^Xem tất cả \((\d+)\)$/, 'View all ($1)'],
    [/^Xem (.+)$/, 'View $1'],
    [/^Thêm (.+) vào giỏ hàng$/, 'Add $1 to cart'],
    [/^Kết quả cho “(.*)”$/, 'Results for “$1”'],
    [/^Ảnh (\d+)$/, 'Image $1'],
    [/^Danh mục (.+) tại Hoa Tay Việt\.$/, 'Category $1 at Hoa Tay Viet.'],
    [/^Toàn bộ (\d+) sản phẩm của Hoa Tay Việt\.$/, 'All $1 products of Hoa Tay Viet.'],
    [/^Gọi ngay (.+)$/, 'Call $1 now'],
    [/^GIÁ SỈ: (.+) VND \( ĐƠN HÀNG ÍT NHẤT (\d+) CÁI \)$/, 'WHOLESALE PRICE: $1 VND (MINIMUM ORDER $2 PCS)']
  ];

  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }

  // Translate one string; returns null when nothing applies.
  function tr(raw) {
    var s = norm(raw);
    if (!s) return null;
    if (Object.prototype.hasOwnProperty.call(DICT, s)) return DICT[s];
    for (var i = 0; i < PATTERNS.length; i++) {
      if (PATTERNS[i][0].test(s)) {
        return s.replace(PATTERNS[i][0], function () {
          var a = arguments, out = PATTERNS[i][1];
          for (var k = 1; k < a.length - 2; k++) {
            var part = a[k];
            out = out.replace('$' + k, DICT[part] || part);
          }
          return out;
        });
      }
    }
    // "<name> - Hoa Tay Việt" page titles
    var m = s.match(/^(.*) - Hoa Tay Việt$/);
    if (m) return (tr(m[1]) || m[1]) + ' - Hoa Tay Viet';
    var m2 = s.match(/^(.*) - Xưởng Sản Xuất Thuyền Mỹ Nghệ Hoa Tay Việt$/);
    if (m2) return (tr(m2[1]) || m2[1]) + ' - Hoa Tay Viet Art Boat Workshop';
    return null;
  }

  var ATTRS = ['placeholder', 'aria-label', 'title', 'alt', 'content'];
  var origText = new WeakMap();   // text node  -> original string
  var origAttr = new WeakMap();   // element    -> { attr: original }
  var lang = 'vi';
  var observer = null;

  function translateText(node) {
    var raw = node.nodeValue;
    var t = tr(raw);
    if (t === null) return;
    if (!origText.has(node)) origText.set(node, raw);
    var lead = raw.match(/^\s*/)[0], trail = raw.match(/\s*$/)[0];
    node.nodeValue = lead + t + trail;
  }

  function translateAttrs(el) {
    var isMeta = el.tagName === 'META';
    if (isMeta && el.getAttribute('name') !== 'description') return;
    ATTRS.forEach(function (a) {
      if (a === 'content' && !isMeta) return;
      if (!el.hasAttribute(a)) return;
      var raw = el.getAttribute(a), t = tr(raw);
      if (t === null) return;
      var store = origAttr.get(el) || {};
      if (!(a in store)) store[a] = raw;
      origAttr.set(el, store);
      el.setAttribute(a, t);
    });
  }

  function walk(root) {
    if (root.nodeType === 3) { translateText(root); return; }
    if (root.nodeType !== 1) return;
    var tag = root.tagName;
    if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') return;
    translateAttrs(root);
    for (var c = root.firstChild; c; c = c.nextSibling) walk(c);
  }

  function restore(root) {
    var w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, null);
    var n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) {
        if (origText.has(n)) { n.nodeValue = origText.get(n); origText.delete(n); }
      } else if (origAttr.has(n)) {
        var store = origAttr.get(n);
        Object.keys(store).forEach(function (a) { n.setAttribute(a, store[a]); });
        origAttr.delete(n);
      }
    }
  }

  function observe(on) {
    if (!observer) {
      observer = new MutationObserver(function (muts) {
        observer.disconnect();
        muts.forEach(function (m) {
          if (m.type === 'childList') {
            each(m.addedNodes, walk);
          } else if (m.type === 'characterData') {
            origText.delete(m.target);
            translateText(m.target);
          }
        });
        observer.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
      });
    }
    if (on) observer.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
    else observer.disconnect();
  }

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  function setLang(next, persist) {
    if (next !== 'en' && next !== 'vi') next = 'vi';
    observe(false);
    if (next === 'en') {
      walk(document.documentElement);
      if (document.title) {
        var t = tr(document.title);
        if (t !== null) {
          if (!origText.has(document.head)) origText.set(document.head, document.title);
          document.title = t;
        }
      }
    } else {
      restore(document.documentElement);
      if (origText.has(document.head)) { document.title = origText.get(document.head); origText.delete(document.head); }
    }
    lang = next;
    document.documentElement.lang = next;
    each(document.querySelectorAll('[data-lang]'), function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-lang') === next ? 'true' : 'false');
    });
    if (persist) { try { localStorage.setItem(KEY, next); } catch (e) {} }
    if (next === 'en') observe(true);
  }

  function init() {
    // dropdown open / close
    each(document.querySelectorAll('.lang-switch'), function (box) {
      var btn = box.querySelector('.lang-toggle');
      function set(open) {
        box.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
      btn.addEventListener('click', function (e) { e.stopPropagation(); set(!box.classList.contains('is-open')); });
      document.addEventListener('click', function (e) { if (!box.contains(e.target)) set(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
      box.addEventListener('click', function (e) { if (e.target.closest('[data-lang]')) set(false); });
    });

    each(document.querySelectorAll('[data-lang]'), function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-lang'), true); });
    });

    var saved = 'vi';
    try { saved = localStorage.getItem(KEY) || 'vi'; } catch (e) {}
    setLang(saved, false);
  }

  window.htyI18n = { set: function (l) { setLang(l, true); }, get: function () { return lang; }, t: tr };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
