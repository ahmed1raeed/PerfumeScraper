SITE = {

    "name": "Lail",

    "base_url": "https://lailfragrances.com",

    "mode": "card",

    "original_mode": "page",

    "collections": [

        ("Men", "/collections/mens"),
        ("Women", "/collections/womens"),
        ("Unisex", "/collections/unisex"),

    ],

    "pagination": "{path}?page={page}",

    "selectors": {

        "product": "li.collection-product-card",

        "title": "h3.card__title a",

        "link": "h3.card__title a",

        "price": "span.price-item",

        "original": "div.product-text"

    }

}