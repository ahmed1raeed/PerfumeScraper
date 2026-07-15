brand = input("Brand Name: ").strip()

base_url = input("Base URL: ").strip()

print("\n--- Collections ---")
print("Write the sections in the format:")
print("Men=/collections/men")
print("Women=/collections/women")
print("Unisex=/collections/unisex")
print("Press Enter twice when you're done..\n")

collections = []

while True:

    line = input("> ").strip()

    if not line:
        break

    name, path = line.split("=", 1)

    collections.append((name.strip(), path.strip()))

print("\n--- Selectors ---")

product = input("Product Selector : ").strip()
title = input("Title Selector   : ").strip()
link = input("Link Selector    : ").strip()
price = input("Price Selector   : ").strip()
original = input("Original Selector: ").strip()

listing = input("Is the original on the product page? (y/n): ").lower() == "y"

filename = f"sites/{brand.lower()}.py"

with open(filename, "w", encoding="utf-8") as f:

    f.write("SITE = {\n\n")

    f.write(f'    "name": "{brand.upper()}",\n\n')

    f.write(f'    "base_url": "{base_url}",\n\n')

    f.write('    "collections": [\n\n')

    for c, p in collections:
        f.write(f'        ("{c}", "{p}"),\n')

    f.write("\n    ],\n\n")

    f.write('    "pagination": "{path}?page={page}",\n\n')

    f.write(f'    "original_in_listing": {str(listing)},\n\n')

    f.write('    "selectors": {\n\n')

    f.write(f'        "product": "{product}",\n\n')
    f.write(f'        "title": "{title}",\n\n')
    f.write(f'        "link": "{link}",\n\n')
    f.write(f'        "price": "{price}",\n\n')
    f.write(f'        "original": "{original}"\n\n')

    f.write("    }\n\n")

    f.write("}\n")

print("\nFile created:", filename)