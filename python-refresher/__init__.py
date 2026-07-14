"""Package exports for customer_orders.

Expose seeded in-memory datasets for easy import:

from customer_orders import CATEGORIES, PRODUCTS, CUSTOMERS
"""

from .data_seed import CATEGORIES, PRODUCTS, CUSTOMERS

__all__ = ["CATEGORIES", "PRODUCTS", "CUSTOMERS"]
