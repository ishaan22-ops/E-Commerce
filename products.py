"""Product catalog and storefront rendering."""

from html import escape


PRODUCTS = [
    {"id": "field-speaker", "name": "Field Notes Speaker", "category": "Tech", "price": 89.00, "description": "Room-filling sound, wrapped in a take-anywhere shape.", "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=1000&q=85", "label": "Bestseller"},
    {"id": "everyday-tote", "name": "Everyday Carryall", "category": "Accessories", "price": 48.00, "description": "A sturdy canvas companion for all the in-between.", "image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1000&q=85", "label": "New"},
    {"id": "studio-headphones", "name": "Studio Headphones", "category": "Tech", "price": 129.00, "description": "A quieter world, with warm and balanced sound.", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=85", "label": ""},
    {"id": "softlight-lamp", "name": "Softlight Table Lamp", "category": "Home", "price": 76.00, "description": "A gentle pool of light for the end of the day.", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1000&q=85", "label": "Small batch"},
    {"id": "daily-watch", "name": "Daily Watch", "category": "Accessories", "price": 112.00, "description": "A considered classic with a brushed steel finish.", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1000&q=85", "label": ""},
    {"id": "35mm-camera", "name": "35mm Pocket Camera", "category": "Tech", "price": 154.00, "description": "For the moments that deserve to be kept.", "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1000&q=85", "label": "Staff pick"},
]


def get_product(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)


def render_product_grid(items, compact=False):
    cards = []
    for product in items:
        label = f'<span class="product-label">{escape(product["label"])}</span>' if product["label"] else ""
        cards.append(
            f"""<article class="product-card">
  <a class="product-image" href="/products" aria-label="Shop {escape(product['name'])}">
    <img src="{escape(product['image'], quote=True)}" alt="{escape(product['name'])}" loading="lazy">{label}
  </a>
  <div class="product-info"><div><p class="product-category">{escape(product['category'])}</p><h3>{escape(product['name'])}</h3></div><strong>${product['price']:.2f}</strong></div>
  <p class="product-description">{escape(product['description'])}</p>
  <form method="post" action="/cart/add" class="add-form"><input type="hidden" name="product_id" value="{escape(product['id'], quote=True)}"><button class="button button-dark" type="submit"><span aria-hidden="true">+</span> Add to bag</button></form>
</article>"""
        )
    grid_class = "product-grid product-grid-compact" if compact else "product-grid"
    return f'<div class="{grid_class}">{"".join(cards)}</div>'


def render_catalog(search="", category="All"):
    categories = ["All", "Tech", "Home", "Accessories"]
    normalized_search = search.casefold().strip()
    filtered = [
        product for product in PRODUCTS
        if (category == "All" or product["category"] == category)
        and (not normalized_search or normalized_search in product["name"].casefold() or normalized_search in product["description"].casefold())
    ]
    options = "".join(
        f'<option value="{name}"{" selected" if name == category else ""}>{name}</option>'
        for name in categories
    )
    results = render_product_grid(filtered) if filtered else '<p class="empty-state">No pieces match that search. Try another word or category.</p>'
    return f"""<section class="page-heading"><p class="eyebrow">The considered edit</p><h1>Good things,<br><em>well chosen.</em></h1><p>A small collection of useful things, made to be kept.</p></section>
<form class="catalog-tools" method="get" action="/products"><label class="search-field"><span class="visually-hidden">Search products</span><input name="q" type="search" value="{escape(search, quote=True)}" placeholder="Search the collection"><button type="submit" aria-label="Search">&#8594;</button></label><label class="filter-field"><span>Filter</span><select name="category" onchange="this.form.requestSubmit()">{options}</select></label><span class="result-count">{len(filtered)} pieces</span></form>
{results}"""