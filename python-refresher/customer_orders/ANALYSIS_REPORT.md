# Order Analysis Report

Command executed:

```bash
python3 -m order_analysis
```

Raw output

```
-----------------------------
CUSTOMER VALUE CLASSIFICATION
-----------------------------
Rowan Jones               $    618.95      High-Value
Blake White               $    313.07      High-Value
Alex Rodriguez            $    994.26      High-Value
Skyler Wilson             $    618.90      High-Value
Jordan Anderson           $    864.48      High-Value
Hayden Jackson            $    896.58      High-Value
Emery Taylor              $    296.09      High-Value
Casey Moore               $     98.20        Moderate
Skyler White              $     59.49        Moderate
Blake Rodriguez           $     52.60        Moderate
Sage Johnson              $     52.60        Moderate
Quinn Wilson              $     78.45        Moderate
Blake Hernandez           $     57.39        Moderate
Riley Davis               $     98.20        Moderate
Morgan Thompson           $     24.60       Low-Value
Alex Thompson             $     13.18       Low-Value
Alex Thomas               $     49.36       Low-Value
Blake Jones               $     24.60       Low-Value
Emery Moore               $     24.60       Low-Value
Emery Wilson              $     24.60       Low-Value

-------------------------
CATEGORY SPENDING SUMMARY
-------------------------
Electronics        $   1280.86
Clothing           $   1017.14
Home Essentials    $   2183.70
Books              $    778.50
Toys               $      0.00

--------------------------------
CUSTOMERS WHO BOUGHT ELECTRONICS
--------------------------------
- Skyler Wilson
- Hayden Jackson
- Morgan Thompson
- Alex Thompson
- Alex Thomas
- Blake Jones
- Emery Moore
- Emery Wilson

--------------------------------
TOP 3 HIGHEST SPENDING CUSTOMERS
--------------------------------
1. Alex Rodriguez
2. Hayden Jackson
3. Jordan Anderson

---------------------------------------------
CUSTOMERS WHO BOUGHT FROM MULTIPLE CATEGORIES
---------------------------------------------
- Rowan Jones
- Alex Rodriguez
- Skyler Wilson
- Jordan Anderson
- Hayden Jackson
- Emery Taylor
- Alex Thomas

--------------------------------------------------
CUSTOMERS WHO BOUGHT BOTH ELECTRONICS AND CLOTHING
--------------------------------------------------
- Skyler Wilson

----------------------------------
MOST FREQUENTLY PURCHASED PRODUCTS
----------------------------------
Product                             Count
------------------------------------------
Eco Lamp 45                             5
Premium Camera 10                       4
Modern Backpack 8                       3
Stylish Notebook 27                     3
Deluxe Router 20                        3
Durable Backpack 28                     2
Compact Notebook 47                     2
Stylish Book 13                         2
Classic Chair 35                        1
Compact Lamp 5                          1
Premium Thermos 38                      1
Pro Sneakers 32                         1
Pro Mug 46                              1
Classic Notebook 7                      1
Ultra Camera 30                         1
Advanced Sneakers 12                    1
Deluxe Mug 6                            1
Portable Pillow 37                      1
Lightweight Drone 39                    1
Classic Speaker 21                      1
Pro Jacket 4                            1
Portable Blender 23                     1
```

Key insights

- Customer segmentation:
  - 7 customers are classified as High-Value (top spenders including `Alex Rodriguez`, `Hayden Jackson`, `Jordan Anderson`).
  - Several customers fall in the Moderate band (~$50–$100); the remainder are Low-Value.

- Category spend distribution:
  - `Home Essentials` leads total spending at $2,183.70 (highest of all categories).
  - `Electronics` ($1,280.86) and `Clothing` ($1,017.14) are the next largest contributors.
  - `Toys` shows $0.00 spending — either no toy products were selected or toy items were not generated/assigned purchases in this seeded dataset.

- Top customers and behavior:
  - `Alex Rodriguez` is the top spender (~$994.26), followed by `Hayden Jackson` and `Jordan Anderson`.
  - Customers who purchased from multiple categories are likely more diverse buyers; seven customers met this criterion.
  - Only `Skyler Wilson` purchased both Electronics and Clothing items in this run.

- Product popularity:
  - `Eco Lamp 45` is the most frequently purchased product (5 purchases), followed by `Premium Camera 10` (4 purchases).
  - A small number of products account for multiple purchases; long tail of one-off purchases exists.

Recommendations / next steps

- Investigate why `Toys` has zero spending — check product generation logic and noun-category mapping.
- Add unit tests for the analysis functions (e.g., `classify_customers`, `calculate_category_spending`) using deterministic seeds.
- If conducting repeated analysis, consider exporting results (CSV/JSON) for downstream reporting and visualization.
