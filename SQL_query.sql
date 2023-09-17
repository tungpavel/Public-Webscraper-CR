SELECT *
FROM card_data
WHERE card_name IN (
    SELECT card_name
    FROM card_data
    WHERE entry_date like '2023-09%'
)
order by card_name, entry_date desc;