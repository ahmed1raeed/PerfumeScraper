SITE = {

    "name": "COZY",

    "base_url": "https://cozyfragrances.shop",

    "mode": "card",

    "original_mode": "listing",

    "collections": [

        ("Men", "/collections/for-him"),
        ("Unisex", "/collections/unisex"),

    ],

    "pagination": "{path}?page={page}",

    "selectors": {

        "product": "li.product-grid__item",

        "title": "h3",

        "link": "a.product-card__link",

        "price": "span.price",

        "original": "rte-formatter"

    }

}