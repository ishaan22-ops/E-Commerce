"""Run the locally hosted Good Things storefront with `python home.py`."""

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from urllib.parse import parse_qs, urlparse

import cart
import history
import products


STYLES = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;1,500;1,600&display=swap');
:root{--ink:#202a24;--muted:#758079;--paper:#f8f8f4;--line:#e4e8e1;--green:#d5ec83;--white:#fff;--serif:'Playfair Display',Georgia,serif;--sans:'DM Sans',sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration:none}button,input,select{font:inherit}.announcement{min-height:34px;background:var(--ink);color:#f9faf6;text-align:center;padding:9px 16px;font-size:10px;letter-spacing:1.2px;text-transform:uppercase}.site-header{height:82px;padding:0 6.2%;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;border-bottom:1px solid var(--line);background:var(--paper)}.brand{font-family:var(--serif);font-size:26px;font-weight:600;letter-spacing:0}.brand span{color:#7a9b45}.main-nav{display:flex;gap:34px;align-items:center;font-size:12px}.main-nav a{transition:color .2s}.main-nav a:hover,.main-nav a.active{color:#759540}.header-right{justify-self:end;display:flex;align-items:center;gap:9px;font-size:12px}.bag-count{height:24px;min-width:24px;padding:0 6px;border-radius:50%;display:grid;place-items:center;background:var(--green);font-size:11px}.page{max-width:1380px;margin:0 auto;padding:0 6.2% 110px}.hero{position:relative;min-height:460px;margin:30px 0 94px;overflow:hidden;background:#52664d;display:flex;align-items:center;color:#fff}.hero-image{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 55%;filter:brightness(.72)}.hero-content{position:relative;max-width:520px;padding:60px 7%}.eyebrow{text-transform:uppercase;letter-spacing:1.8px;font-size:10px;font-weight:700;color:#788a5c;margin:0 0 18px}.hero .eyebrow{color:#e1f3ab}.hero h1,.page-heading h1{font-family:var(--serif);font-size:clamp(42px,5.5vw,70px);font-weight:500;line-height:1.04;margin:0;letter-spacing:0}.hero h1 em,.page-heading h1 em{font-weight:500}.hero-copy{font-size:14px;line-height:1.8;max-width:340px;color:#f0f3ec;margin:22px 0 28px}.button{min-height:46px;padding:0 21px;display:inline-flex;align-items:center;justify-content:center;gap:15px;border:0;font-size:11px;font-weight:700;cursor:pointer;transition:background .2s,transform .2s}.button:hover{transform:translateY(-2px)}.button-light{background:var(--green);color:var(--ink)}.button-light:hover{background:#e5f5b5}.button-dark{background:var(--ink);color:white}.button-dark:hover{background:#455448}.button-dark span,.button-light span{font-size:16px}.section-top{display:flex;justify-content:space-between;align-items:end;margin-bottom:26px}.section-top h2{font-family:var(--serif);font-size:34px;font-weight:500;margin:0}.text-link{font-size:11px;font-weight:700;border-bottom:1px solid var(--ink);padding-bottom:5px}.product-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:38px 22px}.product-card{min-width:0;animation:rise .55s both}.product-image{position:relative;display:block;aspect-ratio:1/1.08;background:#e8eae4;overflow:hidden}.product-image img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s}.product-image:hover img{transform:scale(1.035)}.product-label{position:absolute;top:13px;left:13px;padding:7px 10px;background:var(--paper);font-size:9px;text-transform:uppercase;letter-spacing:1px}.product-info{display:flex;justify-content:space-between;gap:12px;align-items:end;margin-top:15px}.product-category{margin:0 0 5px;color:var(--muted);font-size:9px;letter-spacing:1.2px;text-transform:uppercase}.product-info h3{margin:0;font-size:14px;font-weight:600}.product-info>strong{font-size:12px;white-space:nowrap}.product-description{font-size:11px;color:var(--muted);margin:9px 0 14px;line-height:1.6}.add-form .button{width:100%;min-height:40px}.page-heading{padding:70px 0 28px}.page-heading h1{font-size:56px}.page-heading>p:last-child{color:var(--muted);font-size:13px;margin:17px 0 0;line-height:1.7}.compact-heading{padding:66px 0 28px}.compact-heading h1{font-size:50px}.catalog-tools{display:flex;align-items:center;gap:24px;padding:17px 0;margin-bottom:25px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.search-field{display:flex;align-items:center;width:min(100%,360px);border-bottom:1px solid #aeb8af}.search-field input{width:100%;height:38px;border:0;outline:0;background:transparent;font-size:12px}.search-field button{border:0;background:none;font-size:18px;cursor:pointer}.filter-field{display:flex;align-items:center;gap:10px;font-size:10px;color:var(--muted)}.filter-field select{border:0;background:transparent;color:var(--ink);font-weight:600;font-size:11px;padding:8px 18px 8px 0}.result-count{margin-left:auto;color:var(--muted);font-size:10px}.cart-layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:70px;align-items:start}.bag-row{display:grid;grid-template-columns:94px minmax(0,1fr) 106px 75px 26px;gap:17px;align-items:center;padding:19px 0;border-top:1px solid var(--line)}.bag-row>img{width:94px;aspect-ratio:1;object-fit:cover}.bag-product h2{font-size:13px;margin:0 0 6px}.bag-product>p:last-child{font-size:11px;color:var(--muted);margin:0}.quantity-form{display:flex;align-items:center;gap:8px}.quantity-form input{width:52px;height:34px;border:1px solid var(--line);background:transparent;padding:0 8px}.text-button{border:0;border-bottom:1px solid var(--muted);padding:3px 0;background:none;font-size:10px;cursor:pointer}.line-total{font-size:12px}.remove-button{border:0;background:none;color:var(--muted);font-size:22px;cursor:pointer}.order-summary{background:#eff1e9;padding:24px 23px}.order-summary h2{font-family:var(--serif);font-size:23px;font-weight:500;margin:0 0 16px}.shipping-note{font-size:10px;color:#637c47;padding:10px 0;border-top:1px solid #dfe3d8;border-bottom:1px solid #dfe3d8}.summary-line{display:flex;justify-content:space-between;margin:14px 0;font-size:11px}.summary-total{padding-top:14px;border-top:1px solid #d6dbd1;font-size:14px}.checkout-form{margin-top:22px}.checkout-form label{display:block;margin:13px 0;font-size:10px;font-weight:600}.checkout-form input{display:block;width:100%;height:39px;margin-top:7px;padding:0 10px;border:1px solid #d6dbd1;background:var(--paper)}.button-wide{width:100%;margin-top:10px}.demo-note{text-align:center;color:var(--muted);font-size:9px}.empty-bag,.history-empty{padding:32px 0;border-top:1px solid var(--line);color:var(--muted);font-size:13px}.empty-bag .button{margin-top:8px}.order-list{max-width:780px}.order-card{border-top:1px solid var(--line);padding:23px 0}.order-topline{display:flex;justify-content:space-between;align-items:center}.order-topline h2{font-size:15px;margin:4px 0}.order-topline>strong{font-size:13px}.order-items{font-size:12px;line-height:1.8}.order-items span{color:var(--muted)}.order-email{font-size:10px;color:var(--muted)}.confirmation{max-width:780px;background:#e9f1d8;display:flex;gap:14px;align-items:center;padding:17px 20px;margin-bottom:24px}.confirmation-mark{width:28px;height:28px;display:grid;place-items:center;background:#d3e6af;border-radius:50%}.confirmation strong{font-size:12px}.confirmation p{font-size:10px;color:#59664b;margin:5px 0 0}.site-footer{background:var(--ink);color:#f7f8f3;padding:42px 6.2%;display:flex;justify-content:space-between;align-items:center}.footer-brand{font-family:var(--serif);font-size:20px}.footer-note{font-size:10px;color:#b9c1b8}.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.empty-state{padding:25px 0;color:var(--muted);font-size:13px}@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:800px){.site-header{height:70px;padding:0 5%;grid-template-columns:auto 1fr auto}.main-nav{justify-self:center;gap:17px}.page{padding-left:5%;padding-right:5%}.hero{min-height:390px;margin:22px 0 70px}.product-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 16px}.cart-layout{grid-template-columns:1fr;gap:26px}.order-summary{max-width:none}.bag-row{grid-template-columns:74px minmax(0,1fr) 80px 55px 20px;gap:10px}.bag-row>img{width:74px}.quantity-form{flex-wrap:wrap}.site-footer{padding-left:5%;padding-right:5%}}
@media(max-width:520px){.announcement{font-size:9px}.site-header{height:auto;min-height:72px;grid-template-columns:1fr auto;row-gap:0}.brand{font-size:23px}.main-nav{grid-row:2;grid-column:1/-1;justify-self:start;padding:0 0 14px;gap:24px}.header-right{grid-column:2;grid-row:1}.page{padding-bottom:70px}.hero{min-height:410px;margin:16px 0 58px}.hero-content{padding:45px 8%}.hero h1{font-size:49px}.section-top h2{font-size:27px}.product-grid{gap:26px 12px}.product-info{align-items:start;flex-direction:column;gap:5px}.product-info h3{font-size:12px}.product-description{min-height:35px;font-size:10px}.page-heading{padding-top:52px}.page-heading h1{font-size:45px}.compact-heading h1{font-size:42px}.catalog-tools{gap:13px;flex-wrap:wrap}.search-field{width:100%;order:0}.filter-field{order:1}.result-count{order:2}.bag-row{grid-template-columns:66px minmax(0,1fr) auto 20px;gap:9px}.bag-row>img{width:66px}.quantity-form{grid-column:2;grid-row:2}.line-total{grid-column:3;grid-row:1}.bag-row>form:last-child{grid-column:4;grid-row:1}.bag-product h2{font-size:12px}.site-footer{align-items:flex-start;gap:12px;flex-direction:column}}
"""


def page(title, active, body):
    links = [("Home", "/"), ("Products", "/products"), ("Our story", "/history")]
    navigation = "".join(
        f'<a class="{"active" if path == active else ""}" href="{path}">{label}</a>'
        for label, path in links
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f8f8f4"><title>{escape(title)} | Good Things</title><style>{STYLES}</style></head><body><div class="announcement">A little more considered. A little less ordinary.</div><header class="site-header"><a class="brand" href="/">good things<span>.</span></a><nav class="main-nav" aria-label="Main navigation">{navigation}</nav><a class="header-right" href="/cart" aria-label="Shopping bag, {cart.item_count()} items">Bag <span class="bag-count">{cart.item_count()}</span></a></header><main class="page">{body}</main><footer class="site-footer"><a class="footer-brand" href="/">good things.</a><span class="footer-note">Thoughtfully picked. Made to be lived with.</span></footer></body></html>"""


def home_content():
    featured = products.render_product_grid(products.PRODUCTS[:3], compact=True)
    return f"""<section class="hero"><img class="hero-image" src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=2000&q=90" alt="Sunlit shelves in a thoughtfully curated shop"><div class="hero-content"><p class="eyebrow">A better kind of everyday</p><h1>Find your<br><em>favorite things.</em></h1><p class="hero-copy">Useful, lovely, and made to earn their place. Meet the little collection that makes the everyday feel considered.</p><a class="button button-light" href="/products">Shop the collection <span aria-hidden="true">&#8594;</span></a></div></section><section><div class="section-top"><div><p class="eyebrow">Picked with purpose</p><h2>Good, from the get-go.</h2></div><a class="text-link" href="/products">View all pieces &#8594;</a></div>{featured}</section>"""


class StoreHandler(BaseHTTPRequestHandler):
    def respond(self, content, status=200):
        payload = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def read_form(self):
        length = min(int(self.headers.get("Content-Length", "0")), 16000)
        return parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"))

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/":
            body, title, active = home_content(), "Home", "/"
        elif parsed.path == "/products":
            body, title, active = products.render_catalog(query.get("q", [""])[0], query.get("category", ["All"])[0]), "Products", "/products"
        elif parsed.path == "/cart":
            body, title, active = cart.render_cart(), "Your bag", "/cart"
        elif parsed.path == "/history":
            body, title, active = history.render_history(query.get("placed", [""])[0]), "Order history", "/history"
        else:
            self.respond(page("Not found", "", '<section class="page-heading"><h1>That page wandered off.</h1><a class="text-link" href="/">Back to the shop</a></section>'), 404)
            return
        self.respond(page(title, active, body))

    def do_POST(self):
        parsed = urlparse(self.path)
        form = self.read_form()
        product_id = form.get("product_id", [""])[0]
        if parsed.path == "/cart/add":
            cart.add_item(product_id)
            self.redirect("/cart")
        elif parsed.path == "/cart/update":
            try:
                quantity = int(form.get("quantity", ["1"])[0])
            except ValueError:
                quantity = 1
            cart.update_item(product_id, quantity)
            self.redirect("/cart")
        elif parsed.path == "/cart/remove":
            cart.remove_item(product_id)
            self.redirect("/cart")
        elif parsed.path == "/checkout":
            name = form.get("name", [""])[0].strip()[:80]
            email = form.get("email", [""])[0].strip()[:120]
            order = cart.checkout() if name and email and "@" in email else None
            if order:
                saved_order = history.add_order(order, name, email)
                self.redirect(f"/history?placed={saved_order['id']}")
            else:
                self.redirect("/cart")
        else:
            self.respond(page("Not found", "", '<section class="page-heading"><h1>That page wandered off.</h1><a class="text-link" href="/">Back to the shop</a></section>'), 404)

    def log_message(self, format_string, *args):
        pass


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), StoreHandler)
    print(f"Listening on {host}:{port}; browse to http://<VM_PUBLIC_IP>:{port} from outside the VM.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Good Things.")
        server.server_close()