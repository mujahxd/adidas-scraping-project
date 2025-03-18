import curl_cffi.requests as requests
from typing import List, Optional
from dataclasses import dataclass
import html, time, csv 

@dataclass
class Product:
    product_id: str
    sku: str
    name: str
    regular_price: float
    final_price: float
    launching_date: str
    link_product: str
    description: str

CATEGORY_URL = "https://www.adidas.co.id/graphql?hash=2757426801&_sort_0={{recommended_score:DESC}}&_filter_0={{category_id:{{eq:261}},customer_group_id:{{eq:0}}}}&_pageSize_0=24&_currentPage_0={}"
DETAIL_URL_TEMPLATE = "https://www.adidas.co.id/graphql?hash=1081972869&_filter_0={{sku:{{eq:{}}},customer_group_id:{{eq:0}}}}"
PRODUCT_PAGE_TEMPLATE = "https://www.adidas.co.id{}"

def fetch_skus(page: int) -> List[str]:
    url = CATEGORY_URL.format(page)
    print(f"Fetching SKUs from page {page}...")

    try:
        response = requests.get(url, impersonate="chrome110", timeout=10)  
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error while fetching SKUs: {e}")
        return []

    items = data.get("data", {}).get("products", {}).get("items", [])
    if not items:
        print(f"No SKUs found on page {page}, stopping.")
        return []

    skus = [item.get("sku") for item in items if item.get("sku")]
    print(f"✔ {len(skus)} SKUs found on page {page}")
    return skus

def fetch_product_details(sku) -> Optional[Product]:

    url = DETAIL_URL_TEMPLATE.format(sku)
    print(f"Fetching details for SKU: {sku}")

    try:
        response = requests.get(url, impersonate="chrome110", timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error while fetching product details for {sku}: {e}")
        return None

    try:
        items = data.get("data", {}).get("products", {}).get("items", [])
        if not items:
            print(f"No details found for SKU {sku}.")
            return None

        item = items[0]  # Get the first product
        product_id = str(item.get("id", "Unknown"))
        name = item.get("name", "No Name")

        price_info = item.get("price_range", {}).get("minimum_price", {})
        regular_price = float(price_info.get("regular_price", {}).get("value", 0))
        final_price = float(price_info.get("final_price", {}).get("value", 0))

        launching_date = item.get("custom_attributes").get("launch_date", {}).get("value", "Unknown")
        link_product = PRODUCT_PAGE_TEMPLATE.format(item.get("url"))

        # Extract description from short_description -> html
        short_desc = item.get("short_description", {})
        description = short_desc.get("html", "No Description Available") if short_desc else "No Description Available"

        description = html.unescape(description)
        description = description.replace("\r\n", "\n")  
        description = description.replace("\n", "")
        
        return Product(
            product_id=product_id,
            sku=sku,
            name=name,
            regular_price=regular_price,
            final_price=final_price,
            launching_date=launching_date,
            link_product=link_product,
            description=description
        )
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error while processing product {sku}: {e}")
        return None

def save_to_csv(products: List[Product], filename="products.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Product ID", "SKU", "Name", "Regular Price", "Final Price", "Launching Date", "Link Product", "Description"])
            for product in products:
                writer.writerow([
                    product.product_id, product.sku, product.name,
                    product.regular_price, product.final_price,
                    product.launching_date, product.link_product, product.description
                ])
        print(f"✔ Data successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Error while saving CSV: {e}")

def scrape_adidas(max_pages=5, rate_limit=3):
    all_products = []
    page = 1

    while page <= max_pages:
        skus = fetch_skus(page)
        if not skus:
            break  # Stop if no SKUs are found on this page

        print(f"🎯 Fetching product details for {len(skus)} SKUs on page {page}...")

        for sku in skus:
            product = fetch_product_details(sku)
            if product:
                all_products.append(product)
            time.sleep(rate_limit)  # Rate limiting per SKU

        print(f"✅ Finished processing page {page}, moving to the next page...\n")
        page += 1
        time.sleep(rate_limit)  # Rate limiting before switching pages

    if all_products:
        save_to_csv(all_products)
    else:
        print("❌ No product data was successfully retrieved.")

# Run the script
if __name__ == "__main__":
    scrape_adidas(max_pages=3, rate_limit=2)  # Fetch max 3 pages with a 2-second delay
