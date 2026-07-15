import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time


def scrape(site):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    data = []

    # منع التكرار داخل نفس القسم فقط
    visited = set()

    for category, path in site["collections"]:

        page = 1

        while True:

            if "pagination" in site:
                if page == 1:
                    url = site["base_url"] + path
                else:
                    url = site["base_url"] + site["pagination"].format(
                        path=path,
                        page=page
                    )
            else:
                url = site["base_url"] + path

            try:

                r = requests.get(url, headers=headers, timeout=15)

                if r.status_code != 200:
                    break

                soup = BeautifulSoup(r.text, "html.parser")

                products = soup.select(site["selectors"]["product"])

                print(f"{category} - Page {page} : {len(products)}")

                if len(products) == 0:
                    break

                new_products = 0

                for product in products:

                    try:

                        # -----------------------------
                        # اسم العطر
                        # -----------------------------
                        title = product.select_one(
                            site["selectors"]["title"]
                        )

                        if title is None:
                            continue

                        name = title.get_text(" ", strip=True)

                        # -----------------------------
                        # الرابط
                        # -----------------------------
                        if "link" in site["selectors"]:

                            link_tag = product.select_one(
                                site["selectors"]["link"]
                            )

                        else:

                            link_tag = title

                        if link_tag is None:
                            continue

                        href = link_tag.get("href")

                        if not href:
                            continue

                        if href.startswith("http"):
                            link = href
                        else:
                            link = site["base_url"] + href

                        # منع التكرار داخل نفس القسم فقط
                        key = (category, link)

                        if key in visited:
                            continue

                        visited.add(key)

                        new_products += 1

                        # -----------------------------
                        # السعر
                        # -----------------------------
                        price = None

                        p = product.select_one(
                            site["selectors"]["price"]
                        )

                        if p:

                            txt = p.get_text(" ", strip=True)

                            nums = re.findall(
                                r"\d+(?:,\d{3})*(?:\.\d+)?",
                                txt
                            )

                            if nums:
                                price = float(
                                    nums[0].replace(",", "")
                                )

                        # -----------------------------
                        # Original Perfume
                        # -----------------------------
                        original = ""

                        if site.get("original_in_listing", False):

                            org = product.select_one(
                                site["selectors"]["original"]
                            )

                            if org:
                                original = org.get_text(
                                    " ",
                                    strip=True
                                )

                        else:

                            rr = requests.get(
                                link,
                                headers=headers,
                                timeout=15
                            )

                            if rr.status_code == 200:

                                psoup = BeautifulSoup(
                                    rr.text,
                                    "html.parser"
                                )

                                org = psoup.select_one(
                                    site["selectors"]["original"]
                                )

                                if org:
                                    original = org.get_text(
                                        " ",
                                        strip=True
                                    )

                            time.sleep(0.2)

                        # -----------------------------
                        data.append({

                            "القسم": category,
                            "اسم العطر": name,
                            "Original Perfume": original,
                            "السعر": price

                        })

                        print(name)

                    except Exception as e:

                        print("Error:", e)

                if new_products == 0:
                    break

                page += 1

            except Exception as e:

                print("Page Error:", e)
                break

    df = pd.DataFrame(data)

    os.makedirs("output", exist_ok=True)

    filename = f'output/{site["name"]}.xlsx'

    df.to_excel(filename, index=False)

    print("=" * 50)
    print("تم استخراج", len(df), "منتج")
    print("تم حفظ الملف:", filename)
    print("=" * 50)