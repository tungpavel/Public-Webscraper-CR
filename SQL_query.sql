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
	WHERE entry_date like "2023-11-22%")
ORDER BY
  real_name, entry_date DESC;
