"""In-memory shopping bag and cart page."""

from html import escape
from threading import RLock
from uuid import uuid4

import products


_items = {}
_lock = RLock()


def add_item(product_id):
    if products.get_product(product_id) is None:
        return False
    with _lock:
        _items[product_id] = _items.get(product_id, 0) + 1
    return True


def update_item(product_id, quantity):
    if products.get_product(product_id) is None:
        return
    with _lock:
        if quantity <= 0:
            _items.pop(product_id, None)
        else:
            _items[product_id] = min(quantity, 99)


def remove_item(product_id):
    with _lock:
        _items.pop(product_id, None)


def item_count():
    with _lock:
        return sum(_items.values())


def snapshot():
    with _lock:
        return [(products.get_product(product_id), quantity) for product_id, quantity in _items.items()]


def checkout():
    with _lock:
        lines = [(products.get_product(product_id), quantity) for product_id, quantity in _items.items()]
        lines = [(product, quantity) for product, quantity in lines if product]
        if not lines:
            return None
        subtotal = sum(product["price"] * quantity for product, quantity in lines)
        shipping = 0 if subtotal >= 100 else 6.95
        order = {"id": uuid4().hex[:8].upper(), "items": [{"name": product["name"], "price": product["price"], "quantity": quantity} for product, quantity in lines], "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping}
        _items.clear()
        return order


def render_cart():
    lines = snapshot()
    if not lines:
        return """<section class="page-heading compact-heading"><p class="eyebrow">Your bag</p><h1>A little room<br><em>for something good.</em></h1></section><section class="empty-bag"><p>Your bag is taking a breather.</p><a class="button button-dark" href="/products">Explore the collection <span aria-hidden="true">&#8594;</span></a></section>"""

    subtotal = sum(product["price"] * quantity for product, quantity in lines)
    shipping = 0 if subtotal >= 100 else 6.95
    rows = []
    for product, quantity in lines:
        rows.append(
            f"""<article class="bag-row"><img src="{escape(product['image'], quote=True)}" alt="{escape(product['name'])}"><div class="bag-product"><p class="product-category">{escape(product['category'])}</p><h2>{escape(product['name'])}</h2><p>${product['price']:.2f} each</p></div><form method="post" action="/cart/update" class="quantity-form"><input type="hidden" name="product_id" value="{escape(product['id'], quote=True)}"><label><span class="visually-hidden">Quantity for {escape(product['name'])}</span><input type="number" name="quantity" value="{quantity}" min="0" max="99"></label><button class="text-button" type="submit">Update</button></form><strong class="line-total">${product['price'] * quantity:.2f}</strong><form method="post" action="/cart/remove"><input type="hidden" name="product_id" value="{escape(product['id'], quote=True)}"><button class="remove-button" type="submit" aria-label="Remove {escape(product['name'])}">&#215;</button></form></article>"""
        )
    free_shipping_message = "You have complimentary shipping." if shipping == 0 else f"Add ${100 - subtotal:.2f} for complimentary shipping."
    shipping_label = "Complimentary" if shipping == 0 else f"${shipping:.2f}"
    return f"""<section class="page-heading compact-heading"><p class="eyebrow">Your bag / {sum(quantity for _, quantity in lines)} pieces</p><h1>Good choice.</h1></section><div class="cart-layout"><section class="bag-lines">{''.join(rows)}</section><aside class="order-summary"><h2>Order summary</h2><p class="shipping-note">{free_shipping_message}</p><div class="summary-line"><span>Subtotal</span><span>${subtotal:.2f}</span></div><div class="summary-line"><span>Shipping</span><span>{shipping_label}</span></div><div class="summary-line summary-total"><strong>Total</strong><strong>${subtotal + shipping:.2f}</strong></div><form method="post" action="/checkout" class="checkout-form"><label>Name<input name="name" required maxlength="80" autocomplete="name"></label><label>Email<input name="email" type="email" required maxlength="120" autocomplete="email"></label><button class="button button-dark button-wide" type="submit">Place demo order <span aria-hidden="true">&#8594;</span></button><p class="demo-note">Demo checkout. No payment is collected.</p></form></aside></div>"""