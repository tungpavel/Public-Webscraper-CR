from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


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

def get_prices(list_,driver):
    for card in list_:
        card_name = []
        card_price = []
        card_stock = []

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

        find_lowest_price(font_tags,card_name,card_price,card_stock)

        append_final(card_name,card_price,card_stock) 

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
    loop_cards = ["Erebos, God of the Dead",
                "Liliana of the Veil"]
    final_card_name = []
    final_card_price = []
    final_card_stock = []

    driver = init_driver()
    get_prices(loop_cards,driver)
    df = create_df(final_card_name,final_card_price,final_card_stock)
    print(df)

    for x in loop_cards:
        print(x)