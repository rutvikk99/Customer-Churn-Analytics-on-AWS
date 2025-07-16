-- Query churn rate by customer segment
SELECT customer_segment,
       COUNT(CASE WHEN churn = 'Yes' THEN 1 END)*100.0 / COUNT(*) AS churn_rate
FROM customer_churn
GROUP BY customer_segment;

-- Identify top churn reasons
SELECT churn_reason, COUNT(*) AS frequency
FROM customer_churn
WHERE churn = 'Yes'
GROUP BY churn_reason
ORDER BY frequency DESC;
