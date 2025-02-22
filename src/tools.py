import random
import re

# Sample product database with different categories
PRODUCTS_DB = {
    "shoes": [{"name": "Running Shoes", "price": 80, "size": "9"}, {"name": "Casual Sneakers", "price": 50, "size": "10"}],
    "shirt": [{"name": "Formal Shirt", "price": 45, "size": "L"}, {"name": "Casual T-Shirt", "price": 20, "size": "M"}],
    "belt": [{"name": "Leather Belt", "price": 25, "size": "One Size"}],
    "socks": [{"name": "Cotton Socks (3 Pack)", "price": 12, "size": "One Size"}],
    "dress": [{"name": "Summer Dress", "price": 60, "size": "S"}, {"name": "Evening Gown", "price": 120, "size": "M"}],
    "blouse": [{"name": "Silk Blouse", "price": 50, "size": "M"}, {"name": "Cotton Blouse", "price": 30, "size": "L"}]
}

def extract_price_limit(query):
    """Extract the price limit from the query if 'under' is mentioned."""
    match = re.search(r"under\s*\$?(\d+)", query, re.IGNORECASE)
    return int(match.group(1)) if match else None

def search_products(query):
    """Search for products based on query, price, and size."""
    results = []
    query_lower = query.lower()
    max_price = extract_price_limit(query)

    for category, products in PRODUCTS_DB.items():
        if category in query_lower:
            for product in products:
                if max_price is None or product["price"] <= max_price:
                    results.append(product)

    # If no products found, return competitor price
    if not results:
        competitor_info = compare_competitor_prices(query)
        return {
            "message": "Sorry, we don’t have that, but there is another supplier.",
            "competitor": competitor_info
        }

    return results

def check_discount(product_name):
    """Check discount availability for a product."""
    discount = random.choice([10, 15, 20, 25]) if "No matching" not in product_name else 0
    return {"name": product_name, "discount": f"{discount}%" if discount else "No discount available"}

def estimate_shipping_time(product_name):
    """Estimate shipping time for a product."""
    shipping_days = random.choice(["2-3 days", "3-5 days", "5-7 days"]) if "No matching" not in product_name else "N/A"
    return {"name": product_name, "shipping_time": shipping_days}

def compare_competitor_prices(product_name):
    """Mock competitor price comparison."""
    competitor_stores = ["FashionHub", "StyleZone", "TrendMart"]
    competitor_price = random.randint(5, 20) if "No matching" not in product_name else 0
    return {"name": product_name, "store": random.choice(competitor_stores), "price": competitor_price}

def check_return_policy(product_name):
    """Mock return policy retrieval."""
    policies = ["30-day free return", "No return on discounted items", "Return within 14 days with receipt"]
    return {"name": product_name, "policy": random.choice(policies) if "No matching" not in product_name else "N/A"}

# Test cases
if __name__ == "__main__":
    print(search_products("Find a dress under $50"))
    print(search_products("Find a blouse under $100"))
    print(search_products("Find shoes under $30"))
    print(check_discount("Summer Dress"))
    print(estimate_shipping_time("Running Shoes"))
    print(compare_competitor_prices("Formal Shirt"))
    print(check_return_policy("Leather Belt"))
