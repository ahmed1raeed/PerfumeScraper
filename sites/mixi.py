SITE = {

    "name": "MIXI",

    "base_url": "https://mixifragrances.com",

    "mode": "card",

    "original_mode": "listing",

    "collections": [

        ("Men", "/collections/men-s-fragrances"),
        ("Women", "/collections/women-s-fragrances"),
        ("Unisex", "/collections/unisex-fragrances"),

    ],

    "pagination": "{path}?page={page}",

    "selectors": {

        "product": "li.grid__item",

        "title": "h3 a",

        "link": "h3 a",

        "original": "div.product-card__subtitle",

        "price": "span.price-item"

    }

}