Assuming an `orders` table with `customer_id`, `order_date`, and `total_amount` columns:

```sql
SELECT
    customer_id,
    SUM(total_amount) AS revenue
FROM orders
WHERE order_date >= '2025-01-01'
  AND order_date <  '2026-01-01'
GROUP BY customer_id
ORDER BY revenue DESC, customer_id
LIMIT 5;
```