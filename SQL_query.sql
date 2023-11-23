SELECT
  card_name,
  card_price,
  entry_date,
  COALESCE(card_price - LEAD(card_price) OVER (PARTITION BY card_name ORDER BY entry_date DESC), 0) AS price_change,
  COALESCE(round(CAST(card_price AS FLOAT) / LEAD(card_price) OVER (PARTITION BY card_name ORDER BY entry_date DESC), 2),1) AS change
FROM
  card_data
WHERE card_name in (
	SELECT card_name
	FROM card_data
	WHERE entry_date >= "2023-11-22%")
ORDER BY
  card_name, entry_date DESC;
