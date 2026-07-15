SITE = {

    "name": "IL_VANTO",

    "base_url": "https://il-vanto.com",

    "mode": "card",

    "original_mode": "page",

    "collections": [

        ("Men", "/collections/men"),
        ("Women", "/collections/women"),

    ],

    "pagination": "{path}?page={page}",

    "selectors": {

        "product": "product-card",

        "title": "span.product-card__title a",

        "link": "span.product-card__title a",

        "price": "sale-price",

        "original": "div.product-info__vendor a"

    }

}