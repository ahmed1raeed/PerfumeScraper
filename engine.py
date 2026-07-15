import os
import re
import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ==========================================================
# Helpers
# ==========================================================

def download(url):

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    r.raise_for_status()

    return BeautifulSoup(r.text, "html.parser")


def first(element, selector):

    if not selector:
        return None

    return element.select_one(selector)


def clean(text):

    if text is None:
        return ""

    return " ".join(text.split()).strip()


def extract_price(text):

    if text is None:
        return None

    nums = re.findall(
        r"\d+(?:,\d{3})*(?:\.\d+)?",
        text
    )

    if not nums:
        return None

    return float(
        nums[0].replace(",", "")
    )


def build_url(base, href):

    if href.startswith("http"):

        return href

    return urljoin(base, href)


# ==========================================================
# Product Extractors
# ==========================================================

def get_title(card, site):

    tag = first(
        card,
        site["selectors"]["title"]
    )

    if tag is None:

        return ""

    return clean(
        tag.get_text(" ", strip=True)
    )


def get_link(card, site):

    selector = site["selectors"].get(
        "link"
    )

    if selector:

        tag = first(card, selector)

    else:

        tag = first(
            card,
            site["selectors"]["title"]
        )

    if tag is None:

        return None

    href = tag.get("href")

    if not href:

        return None

    return build_url(
        site["base_url"],
        href
    )


def get_price(card, site):

    tag = first(
        card,
        site["selectors"]["price"]
    )

    if tag is None:

        return None

    return extract_price(
        tag.get_text(" ", strip=True)
    )


# ==========================================================
# Original Modes
# ==========================================================

def original_from_listing(card, site):

    tag = first(
        card,
        site["selectors"]["original"]
    )

    if tag is None:

        return ""

    return clean(
        tag.get_text(" ", strip=True)
    )


def original_from_page(link, site):

    soup = download(link)


    parser = site.get("original_parser", "selector")

    if parser == "meta_description":
        tag = soup.select_one('meta[name="description"]')

    if tag:
        text = tag.get("content", "").strip()

        if " is " in text:
            return text.split(" is ", 1)[0]

        return text


    tag = first(
        soup,
        site["selectors"]["original"]
    )

    if tag is None:

        return ""

    return clean(
        tag.get_text(" ", strip=True)
    )


def original_from_split(title, site):

    keyword = site.get(
        "split_keyword",
        "Inspired by"
    )

    if keyword not in title:

        return title, ""

    left, right = title.split(
        keyword,
        1
    )

    return (
        clean(left),
        clean(right)
    )
# ==========================================================
# Collection Readers
# ==========================================================

def get_cards(soup, site):

    mode = site.get("mode", "card")

    if mode == "card":

        selector = site["selectors"]["product"]

    else:

        selector = site["selectors"]["link"]

    return soup.select(selector)


def get_original(card, title, link, site):

    mode = site.get(
        "original_mode",
        "page"
    )

    if mode == "listing":

        return title, original_from_listing(
            card,
            site
        )

    elif mode == "split":

        return original_from_split(
            title,
            site
        )

    else:

        return (
            title,
            original_from_page(
                link,
                site
            )
        )


def read_card(card, category, site):

    title = get_title(
        card,
        site
    )

    if not title:

        return None

    link = get_link(
        card,
        site
    )

    if not link:

        return None

    price = get_price(
        card,
        site
    )

    title, original = get_original(

        card,

        title,

        link,

        site

    )

    return {

        "القسم": category,

        "اسم العطر": title,

        "Original Perfume": original,

        "السعر": price,

        "_link": link

    }


# ==========================================================
# Main Scraper
# ==========================================================

def scrape(site):

    data = []

    visited = set()

    for category, path in site["collections"]:

        page = 1

        while True:

            if page == 1:

                url = urljoin(

                    site["base_url"],

                    path

                )

            else:

                url = urljoin(

                    site["base_url"],

                    site["pagination"].format(

                        path=path,

                        page=page

                    )

                )

            try:

                soup = download(url)

            except Exception:

                break

            cards = get_cards(

                soup,

                site

            )

            if not cards:

                break

            print(

                f"{category} - Page {page} : {len(cards)}"

            )

            new_products = 0

            for card in cards:

                try:

                    product = read_card(

                        card,

                        category,

                        site

                    )

                    if product is None:

                        continue

                    key = (

                        category,

                        product["_link"]

                    )

                    if key in visited:

                        continue

                    visited.add(key)

                    del product["_link"]

                    data.append(product)

                    print(

                        product["اسم العطر"]

                    )

                    new_products += 1

                    time.sleep(.1)

                except Exception as e:

                    print(e)

            if new_products == 0:

                break

            page += 1
                # ==========================================================
    # Save Excel
    # ==========================================================

    if len(data) == 0:

        print("=" * 50)
        print("لم يتم استخراج أي منتجات")
        print("=" * 50)
        return

    df = pd.DataFrame(data)

    columns = [

        "القسم",

        "اسم العطر",

        "Original Perfume",

        "السعر"

    ]

    df = df[columns]

    df = df.drop_duplicates()

    df = df.sort_values(

        by=[

            "القسم",

            "اسم العطر"

        ]

    )

    os.makedirs(

        "output",

        exist_ok=True

    )

    filename = os.path.join(

        "output",

        f"{site['name']}.xlsx"

    )

    df.to_excel(

        filename,

        index=False

    )

    print()

    print("=" * 60)

    print(

        f"Brand      : {site['name']}"

    )

    print(

        f"Products   : {len(df)}"

    )

    print(

        f"Excel File : {filename}"

    )

    print("=" * 60)


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print(

        "Engine V3 Loaded."

    )