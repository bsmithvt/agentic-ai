"""Seed in-memory datasets for customer orders analysis.

Provides three module-level dictionaries used by the analysis code:
- `CATEGORIES`: list of 5 product category names
- `PRODUCTS`: dict mapping product name -> (price, category)
- `CUSTOMERS`: dict mapping customer name -> list of ordered product names
"""
# Use builtin generic types (list, dict, tuple) for annotations (Python 3.9+)
import random

# Deterministic output for reproducibility
random.seed(42)

# 1) Generate 20 random customer names
first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn",
    "Avery", "Parker", "Rowan", "Skyler", "Dakota", "Reese", "Emery",
    "Hayden", "Blake", "Kai", "Payton", "Sage", "Spencer", "Logan",
]

last_names = [
    "Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis",
    "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor",
    "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
]

def _make_unique_names(count: int) -> list[str]:
    all_names = [f"{fn} {ln}" for fn in sorted(first_names) for ln in sorted(last_names)]
    rng = random.Random(42)
    return rng.sample(all_names, count)

CUSTOMER_COUNT = 20
CUSTOMERS_LIST = _make_unique_names(CUSTOMER_COUNT)

# 2) Create 5 unique product categories
CATEGORIES: list[str] = [
    "Electronics",
    "Clothing",
    "Home Essentials",
    "Books",
    "Toys",
]

# 3) Create 50 unique products distributed across categories
PRODUCT_COUNT = 50

adjectives = [
    "Smart", "Ultra", "Eco", "Pro", "Compact", "Deluxe", "Classic", "Modern",
    "Portable", "Premium", "Lightweight", "Advanced", "Stylish", "Durable",
]

nouns = [
    "Speaker", "Headphones", "Blender", "Jacket", "Lamp", "Mug", "Notebook",
    "Backpack", "Vacuum", "Camera", "Watch", "Sneakers", "Book", "Toy", "Chair",
    "Table", "Pillow", "Thermos", "Drone", "Router",
]

PRODUCTS: dict[str, tuple[float, str]] = {}
product_names: list[str] = []
# Map nouns to realistic categories
noun_category_map = {
    "Speaker": "Electronics",
    "Headphones": "Electronics",
    "Blender": "Home Essentials",
    "Jacket": "Clothing",
    "Lamp": "Home Essentials",
    "Mug": "Home Essentials",
    "Notebook": "Books",
    "Backpack": "Clothing",
    "Vacuum": "Home Essentials",
    "Camera": "Electronics",
    "Watch": "Electronics",
    "Sneakers": "Clothing",
    "Book": "Books",
    "Toy": "Toys",
    "Chair": "Home Essentials",
    "Table": "Home Essentials",
    "Pillow": "Home Essentials",
    "Thermos": "Home Essentials",
    "Drone": "Electronics",
    "Router": "Electronics",
}

for i in range(PRODUCT_COUNT):
    adj = adjectives[i % len(adjectives)]
    noun = nouns[i % len(nouns)]
    # include index to guarantee uniqueness
    name = f"{adj} {noun} {i+1}"
    # assign realistic category based on noun, fallback to Home Essentials
    category = noun_category_map.get(noun, "Home Essentials")
    price = round(random.uniform(10.0, 500.0), 2)
    PRODUCTS[name] = (price, category)
    product_names.append(name)

# 4) Map customers to lists of ordered products (product names)
CUSTOMERS: dict[str, list[str]] = {}
cheap_products = [name for name, (price, _) in PRODUCTS.items() if price < 40]
moderate_products = [name for name, (price, _) in PRODUCTS.items() if 40 <= price <= 100]
expensive_products = [name for name, (price, _) in PRODUCTS.items() if price > 100]


def _generate_order_for_segment(segment: str, seed: int) -> list[str]:
    rng = random.Random(seed)
    for _ in range(50):
        if segment == "Low-Value":
            orders = rng.choices(cheap_products, k=rng.randint(1, 4))
        elif segment == "Moderate":
            orders = (
                rng.choices(moderate_products, k=rng.randint(1, 3))
                + rng.choices(cheap_products, k=rng.randint(0, 1))
            )
        else:
            orders = (
                rng.choices(expensive_products, k=rng.randint(1, 3))
                + rng.choices(moderate_products, k=rng.randint(0, 2))
            )

        total_spent = sum(PRODUCTS[product][0] for product in orders)
        if segment == "Low-Value" and total_spent < 50:
            return orders
        if segment == "Moderate" and 50 <= total_spent <= 100:
            return orders
        if segment == "High-Value" and total_spent > 100:
            return orders

    return orders

for index, cust in enumerate(CUSTOMERS_LIST):
    if index < 7:
        segment = "High-Value"
    elif index < 14:
        segment = "Moderate"
    else:
        segment = "Low-Value"
    CUSTOMERS[cust] = _generate_order_for_segment(segment, seed=1000 + index)

# Expose variables at module level
__all__ = [
    "CATEGORIES",
    "PRODUCTS",
    "CUSTOMERS",
    "classify_customers",
    "calculate_category_spending",
    "customers_who_bought_electronics",
    "top_n_customers",
    "customers_with_multiple_categories",
    "customers_with_electronics_and_clothing",
]


def classify_customers() -> dict[str, tuple[float, str]]:
    """Return customer spend and value classification.

    Returns:
        A dictionary mapping customer name to a tuple of
        (total_spent, classification).
    """
    customer_summary: dict[str, tuple[float, str]] = {}

    for customer, orders in CUSTOMERS.items():
        total_spent = sum(PRODUCTS[product][0] for product in orders)
        if total_spent > 100:
            classification = "High-Value"
        elif total_spent >= 50:
            classification = "Moderate"
        else:
            classification = "Low-Value"
        customer_summary[customer] = (total_spent, classification)

    return customer_summary


def calculate_category_spending() -> dict[str, float]:
    """Calculate total amount spent per product category.

    Returns:
        Dictionary mapping category name to total spending amount.
    """
    category_spending: dict[str, float] = {category: 0.0 for category in CATEGORIES}

    for customer, orders in CUSTOMERS.items():
        for product in orders:
            price, category = PRODUCTS[product]
            category_spending[category] += price

    return category_spending


def customers_who_bought_electronics() -> list[str]:
    """Return all customers who purchased at least one Electronics product."""
    return [
        customer
        for customer, orders in CUSTOMERS.items()
        if any(PRODUCTS[product][1] == "Electronics" for product in orders)
    ]


def top_n_customers(n: int = 3) -> list[str]:
    """Return the top N customers by total spend."""
    customer_summary = classify_customers()
    sorted_customers = sorted(
        customer_summary.items(), key=lambda item: item[1][0], reverse=True
    )
    return [customer for customer, _ in sorted_customers[:n]]


def customers_with_multiple_categories() -> list[str]:
    """Return customers who purchased products from more than one category."""
    return [
        customer
        for customer, orders in CUSTOMERS.items()
        if len({PRODUCTS[product][1] for product in orders}) > 1
    ]


def customers_with_electronics_and_clothing() -> list[str]:
    """Return customers who purchased both Electronics and Clothing items."""
    electronics_buyers = {
        customer
        for customer, orders in CUSTOMERS.items()
        if any(PRODUCTS[product][1] == "Electronics" for product in orders)
    }
    clothing_buyers = {
        customer
        for customer, orders in CUSTOMERS.items()
        if any(PRODUCTS[product][1] == "Clothing" for product in orders)
    }
    return sorted(electronics_buyers & clothing_buyers)


def most_frequently_purchased_products() -> list[tuple[str, int]]:
    """Return products sorted by purchase frequency in descending order."""
    product_counts: dict[str, int] = {}
    for orders in CUSTOMERS.values():
        for product in orders:
            product_counts[product] = product_counts.get(product, 0) + 1
    return sorted(product_counts.items(), key=lambda item: item[1], reverse=True)


def _print_report_header(title: str) -> None:
    header_line = "-" * len(title)
    print(f"\n{header_line}")
    print(title)
    print(header_line)


if __name__ == "__main__":
    summary = classify_customers()
    _print_report_header("CUSTOMER VALUE CLASSIFICATION")
    for customer, (total_spent, classification) in summary.items():
        print(f"{customer:<25} ${total_spent:>10.2f} {classification:>15}")

    category_totals = calculate_category_spending()
    _print_report_header("CATEGORY SPENDING SUMMARY")
    for category, total in category_totals.items():
        print(f"{category:<18} ${total:>10.2f}")

    electronics_customers = customers_who_bought_electronics()
    _print_report_header("CUSTOMERS WHO BOUGHT ELECTRONICS")
    for customer in electronics_customers:
        print(f"- {customer}")

    top_customers = top_n_customers(3)
    _print_report_header("TOP 3 HIGHEST SPENDING CUSTOMERS")
    for index, customer in enumerate(top_customers, start=1):
        print(f"{index}. {customer}")

    multiple_category_customers = customers_with_multiple_categories()
    _print_report_header("CUSTOMERS WHO BOUGHT FROM MULTIPLE CATEGORIES")
    for customer in multiple_category_customers:
        print(f"- {customer}")

    electronics_and_clothing_customers = customers_with_electronics_and_clothing()
    _print_report_header("CUSTOMERS WHO BOUGHT BOTH ELECTRONICS AND CLOTHING")
    for customer in electronics_and_clothing_customers:
        print(f"- {customer}")

    _print_report_header("MOST FREQUENTLY PURCHASED PRODUCTS")
    print(f"{'Product':<35} {'Count':>5}")
    print("-" * 42)
    for product, count in most_frequently_purchased_products():
        print(f"{product:<35} {count:>5}")
