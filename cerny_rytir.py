from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import logging
import configparser

def get_file_path():
    config = configparser.ConfigParser()
    config.read('config.ini')

    data_file_path = config.get('Paths', 'data_file_path')

    return data_file_path

def check_and_insert(real_name, card_name, new_price, new_stock):
    # Check if the price has changed for the card
    select_query = "SELECT card_price FROM CR_data WHERE real_name = ? ORDER BY entry_date DESC LIMIT 1"
    for name in real_name:
        cursor.execute(select_query, (name,))

    latest_price = cursor.fetchone()
    
    if latest_price is None or new_price != latest_price[0]:
        # Price has changed or it's the first entry
        insert_query = "INSERT INTO CR_data (real_name, card_name, card_price, card_stock, entry_date) VALUES (?, ?, ?, ?, ?)"
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        for name in real_name:
            cursor.execute(insert_query, (name, card_name, new_price, new_stock, current_datetime))

        db_connection.commit()

        logging.info(f"Inserted new entry for {real_name} with price {new_price} and stock {new_stock}")

def load_list(path):
    list =  pd.read_csv(path,header=0)
    return list

# Initialize the WebDriver
def init_driver():
    driver = webdriver.Chrome()
    driver.get("https://cernyrytir.cz/")
    return driver

# Find "Seach button", CTRL+A and type the name of the card
def search_card(card):
    # Locate the search element and perform a search
    search = driver.find_element(By.ID, "left_hint")
    # Select all in the search box
    search.send_keys(Keys.CONTROL, "a")
    # Type the desired card
    search.send_keys(card)
    # Press enter
    search.send_keys(Keys.RETURN)

def find_lowest_price(tag,name,price,stock):
    # Loop through the font tags with custom index starting from 1, 2, and 3
    # The cards are repeated every 3 values. e.g. name 1, price 1, stock 1, name 2, price 2, stock 2
    for n in range(3):
        for index, font_tag in enumerate(tag, start=n):
            if index % 3 == 0:
                value = font_tag.get_text().strip()
                # Get card name
                if n == 0:
                    name.append(value)
                # Get card price
                elif n == 1:
                    price.append(value)
                # Get card stock
                elif n == 2:
                    stock.append(value)
                else:
                    "Error"

# Take the last value only (The lowest)
def append_final(real_name,name,price,stock):
    index_to_append = get_first_non_zero_from_end(stock)
    if index_to_append != None:
        final_real_name.append(real_name)
        
    final_card_name.append(name[index_to_append])
    final_card_price.append(price[index_to_append])
    final_card_stock.append(stock[index_to_append])

def get_first_non_zero_from_end(lst):
    for idx, value in enumerate(reversed(lst)):
        if value[0] != "0":
            return len(lst) - 1 - idx
        
def get_prices(list_, driver):
    for card in list_:
        real_name = []
        card_name = []
        card_price = []
        card_stock = []

        try:
            # Search for the card
            search_card(card)
            # Wait for a bit to allow the page to load
            driver.implicitly_wait(10)  # Wait for up to 10 seconds
            # Get the updated page source after the search action
            page_source = driver.page_source
            # Parse the updated page source with Beautiful Soup
            soup = BeautifulSoup(page_source, "lxml")
            # Find the <font> tag with the specified style
            font_tags = soup.findAll('font', style='font-weight : bolder;')

            find_lowest_price(font_tags, card_name, card_price, card_stock)
            
            # If no error, will append the real name
            real_name.append(card)

            # Append the final lists
            append_final(real_name, card_name, card_price, card_stock)


        except NoSuchElementException:
            print(f"Card '{card}' not found on the website. Skipping...")
        except Exception as e:
            print(f"An error occurred while processing '{card}': {e}") 

def create_df(real_name,name,price,stock):
    dataframe = {
    "Real Name": real_name,
    "Card Name": name,
    "Card Price": price,
    "Card Stock": stock
    }
    df = pd.DataFrame(dataframe)
    # Add today's date
    df['Date'] = datetime.today().date()
    return df

# Run this in the terminal
def run_today():
    query = f"""
SELECT
  real_name,
  card_price,
  entry_date,
  COALESCE(card_price - LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 0) AS price_change,
  COALESCE(round(CAST(card_price AS FLOAT) / LEAD(card_price) OVER (PARTITION BY real_name ORDER BY entry_date DESC), 2), 1) AS change
FROM
  CR_data
WHERE real_name IN (
  SELECT real_name
  FROM CR_data
  WHERE entry_date = DATE('now')
)
ORDER BY
  entry_date DESC, real_name
LIMIT (
	SELECT count(*)
	FROM CR_data
	WHERE entry_date = DATE('now'))
"""

    cursor.execute(query)
    output = cursor.fetchall()
    
    for row in output:
        # Replace non-breaking space with a regular space
        formatted_price = row[1].replace('\xa0', ' ')
        # Print the formatted row
        print((row[0], formatted_price, row[2], row[3], row[4]))


if __name__ == "__main__":
    main_path = get_file_path()

    # Configure logging
    logging.basicConfig(filename=f'{main_path}\log_CR_cards.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    logging.info(f"Script ran on {datetime.now()}")

    # Initialize the SQLite database connection
    db_connection = sqlite3.connect(f'{main_path}\card_data.db')
    cursor = db_connection.cursor()

    # Define the SQL command to create a table if not exists
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS CR_data (
        id INTEGER PRIMARY KEY,
        real_name TEXT NOT NULL,
        card_name TEXT NOT NULL,
        card_price REAL NOT NULL,
        card_stock TEXT NOT NULL,
        entry_date TEXT NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    db_connection.commit()

    card_list = load_list(r"mtg list.csv")
    loop_cards = card_list.iloc[:,0].tolist()

    driver = init_driver()
    final_real_name = []
    final_card_name = []
    final_card_price = []
    final_card_stock = []
    get_prices(loop_cards,driver)

    df = create_df(final_real_name,final_card_name,final_card_price,final_card_stock)

    # Insert new data into the database
    for card in range(len(final_real_name)):
        real_name = final_real_name[card]
        card_name = final_card_name[card]
        card_price = final_card_price[card]
        card_stock = final_card_stock[card]
        check_and_insert(real_name, card_name, card_price, card_stock)

    # Close the WebDriver
    driver.quit()

    # Run today's output
    run_today()

    # Close the database connection
    db_connection.close()

    input("Press Enter to exit.")

    # df.to_csv("MTG Collected Prices.csv")