from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3

# Initialize the SQLite database connection
db_connection = sqlite3.connect('card_data.db')
cursor = db_connection.cursor()

# Define the SQL command to create a table if not exists
create_table_query = '''
    CREATE TABLE IF NOT EXISTS card_data (
    id INTEGER PRIMARY KEY,
    card_name TEXT NOT NULL,
    card_price REAL NOT NULL,
    card_stock TEXT NOT NULL,
    entry_date TEXT NOT NULL
);
'''
cursor.execute(create_table_query)
db_connection.commit()

def check_and_insert(card_name, new_price, new_stock):
    # Check if the price has changed for the card
    select_query = "SELECT card_price FROM card_data WHERE card_name = ? ORDER BY entry_date DESC LIMIT 1"
    cursor.execute(select_query, (card_name,))
    latest_price = cursor.fetchone()
    
    if latest_price is None or new_price != latest_price[0]:
        # Price has changed or it's the first entry
        insert_query = "INSERT INTO card_data (card_name, card_price, card_stock, entry_date) VALUES (?, ?, ?, ?)"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(insert_query, (card_name, new_price, new_stock, current_datetime))
        db_connection.commit()

        print(f"Inserted new entry for {card_name} with price {new_price} and stock {new_stock}")

def load_list(path):
    list =  pd.read_excel(path)
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
    for n in range(3):
        for index, font_tag in enumerate(tag, start=n):
            if index % 3 == 0:
                value = font_tag.get_text().strip()
                if n == 0:
                    name.append(value)
                elif n == 1:
                    price.append(value)
                elif n == 2:
                    stock.append(value)
                else:
                    "Error"

# Take the last value only (The lowest)
def append_final(name,price,stock):
    final_card_name.append(name[-1])
    final_card_price.append(price[-1])
    final_card_stock.append(stock[-1])

def get_prices(list_, driver):
    for card in list_:
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
            append_final(card_name, card_price, card_stock)

        except NoSuchElementException:
            print(f"Card '{card}' not found on the website. Skipping...")
        except Exception as e:
            print(f"An error occurred while processing '{card}': {e}")



def create_df(name,price,stock):
    dataframe = {
    "Card Name": name,
    "Card Price": price,
    "Card Stock": stock
    }

    df = pd.DataFrame(dataframe)
    # Add today's date
    df['Date'] = datetime.today().date()

    return df


if __name__ == "__main__":
    card_list = load_list(r'Tajic fr.xlsx')
    loop_cards = card_list.iloc[:,0].tolist()

    driver = init_driver()
    final_card_name = []
    final_card_price = []
    final_card_stock = []
    get_prices(loop_cards,driver)

    df = create_df(final_card_name,final_card_price,final_card_stock)

    # Insert new data into the database
    for card in range(len(final_card_name)):
        card_name = final_card_name[card]
        card_price = final_card_price[card]
        card_stock = final_card_stock[card]
        check_and_insert(card_name, card_price, card_stock)

            # Close the WebDriver
    driver.quit()

    # Close the database connection
    db_connection.close()