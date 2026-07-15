SITE = {
    "name": "HYPNOS",

    "base_url": "https://hypnosfragrances.com",

    "collections": [
        ("Men", "/collections/for-him"),
        ("Women", "/collections/for-her")
    ],

    "pagination": "{path}?page={page}",

    "mode": "card",

    "original_mode": "page",
    "original_parser": "meta_description",
    "selectors": {
        "product": "product-card",
        "title": "h3",
        "price": ".price",
        "link": "a[href*='/products/']",

        # هنقرأ الـ meta description
        "original": 'meta[name="description"]'
    }
}
