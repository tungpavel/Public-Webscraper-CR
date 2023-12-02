-- To view analytics of new entries
SELECT
  real_name,
  card_price,
  entry_date,
  COALESCE(card_price - LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 0) AS price_change,
  COALESCE(round(CAST(card_price AS FLOAT) / LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 2),1) AS change
FROM
  card_data
WHERE real_name in (
	SELECT real_name
	FROM card_data
	WHERE entry_date is DATE('now'))
ORDER BY
  real_name, entry_date DESC;


-- For Python script to see new entries and their change vs old price
SELECT
  real_name,
  card_price,
  entry_date,
  COALESCE(card_price - LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 0) AS price_change,
  COALESCE(round(CAST(card_price AS FLOAT) / LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 2), 1) AS change
FROM
  card_data
WHERE real_name IN (
  SELECT real_name
  FROM card_data
  WHERE entry_date = DATE('now')
)
ORDER BY
  entry_date DESC, real_name
LIMIT (
	SELECT count(*)
	FROM card_data
	WHERE entry_date = DATE('now'))