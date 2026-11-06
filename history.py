"""Order history and confirmation rendering."""

from html import escape
from threading import RLock


_orders = []
_lock = RLock()


def add_order(order, customer_name, customer_email):
    saved_order = {**order, "customer_name": customer_name, "customer_email": customer_email}
    with _lock:
        _orders.insert(0, saved_order)
    return saved_order


def render_history(placed_order_id=""):
    with _lock:
        orders = list(_orders)
    confirmation = ""
    if placed_order_id:
        matching = next((order for order in orders if order["id"] == placed_order_id), None)
        if matching:
            confirmation = f'<div class="confirmation"><span class="confirmation-mark" aria-hidden="true">&#10003;</span><div><strong>Order {escape(matching["id"])}, all set.</strong><p>A confirmation is ready for {escape(matching["customer_email"])}.</p></div></div>'
    if not orders:
        body = '<section class="empty-state history-empty"><p>No orders yet. The good things are waiting.</p><a class="button button-dark" href="/products">Browse the collection <span aria-hidden="true">&#8594;</span></a></section>'
    else:
        cards = []
        for order in orders:
            item_text = ", ".join(f'{escape(item["name"])} <span>× {item["quantity"]}</span>' for item in order["items"])
            cards.append(
                f"""<article class="order-card"><div class="order-topline"><div><p class="product-category">Order {escape(order['id'])}</p><h2>Made for {escape(order['customer_name'])}</h2></div><strong>${order['total']:.2f}</strong></div><p class="order-items">{item_text}</p><p class="order-email">{escape(order['customer_email'])}</p></article>"""
            )
        body = f'<section class="order-list">{"".join(cards)}</section>'
    return f"""<section class="page-heading compact-heading"><p class="eyebrow">A record of the good things</p><h1>Your orders.</h1><p>Orders placed during this visit appear here.</p></section>{confirmation}{body}"""