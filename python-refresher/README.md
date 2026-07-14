# Customer Orders — order_analysis

Overview
- Small Python module that seeds in-memory datasets and provides analysis helpers for customer orders.

Quick start
- Ensure Python 3.9+ is installed.
- (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Run the script as a module:

```bash
python3 -m order_analysis
```

or directly:

```bash
python3 order_analysis.py
```

What it provides
- Module-level data: `CATEGORIES`, `PRODUCTS`, `CUSTOMERS` (seeded deterministically).
- Analysis functions: `classify_customers()`, `calculate_category_spending()`, `customers_who_bought_electronics()`, `top_n_customers()`, `customers_with_multiple_categories()`, `customers_with_electronics_and_clothing()`, and `most_frequently_purchased_products()`.

Developer notes
- Deterministic seeding: the module uses `random.seed(42)` and local Random instances for reproducible outputs.
- Requires Python 3.9+ for the in-source generic type annotations (e.g. `dict[str, ...]`).
- The file was renamed from `data_seed.py` to `order_analysis.py` — update any imports accordingly.

Testing & linting
- No test suite is included. For quick checks, run the module (see Quick start).
- Lint with `flake8` or `ruff` if desired.

Contributing
- Open a PR with focused changes. Keep seeded data deterministic unless changing a test that requires variability.

License
- None specified.
