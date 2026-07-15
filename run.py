from engine import scrape
from merge_brands import merge_brands
from sites import SITES

print(f"Found {len(SITES)} brands.\n")

for site in SITES:

    print("=" * 60)
    print(f"Scraping {site['name']}")
    print("=" * 60)

    try:
        scrape(site)

    except Exception as e:
        print(f"❌ {site['name']} -> {e}")

print("\nUpdating Price Comparison...\n")

merge_brands()

print("\nFinished ✔")