# Card Data Scraper

The Card Data Scraper is a Python script that helps you scrape card information from a website, store it in a SQLite database, and generate a DataFrame for analysis. It utilizes the Selenium WebDriver for web scraping and BeautifulSoup for HTML parsing.

## Features

- Web scrape card information from a specific website.
- Store card data in a SQLite database.
- Generate a DataFrame with card information for further analysis.
- Check and insert updated card data into the database.

## Requirements

- Python 3.x
- Selenium
- Beautiful Soup
- pandas
- Chrome WebDriver (chromedriver)

## Setup

1. Install the required Python libraries using pip:
   
pip install selenium beautifulsoup4 pandas

sql
Copy code

2. Download the Chrome WebDriver (chromedriver) compatible with your Chrome version and add it to your system's PATH.

3. Clone the repository:

git clone https://github.com/tungpavel/Public-Webscraper-CR

css
Copy code

4. Move to the project directory:

cd card-data-scraper

markdown
Copy code

5. Update `mtg list.xlsx` with the list of cards you want to scrape.

## Usage

1. Run the script:

python scraper.py

markdown
Copy code

2. The script will perform the following steps:
- Initialize the SQLite database connection.
- Create a database table if it doesn't exist.
- Scrape card data from the specified website.
- Store the scraped data in the database.
- Generate a DataFrame with card information.
- Close the WebDriver and the database connection.

3. Check the generated DataFrame for analysis.

## Install pipx and virtualenv
* In the command line, type 
```
py -m pip install --user pipx
py -m pipx ensurepath
py -m pipx install virtualenv
```

## Clone this repository 
* Navigate to the directory you want to clone to `cd <dir>` e.g. `cd "C:\Users\John Smith\Python\"`
* Clone this repo: `git clone git@github.com:tungpavel/WebScraping-LetsRecycle-.git`

## Set up virtual environment
* Navigate to the repo location `cd <dir>` e.g. `cd "C:\Users\John Smith\Python\Data-Team-Utilities"` - if continuing form the previous step, just type `cd Data-Team-Utilities`
* Run the following commands (you can replace "venv" with a meaningful name if you like).
```
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! If you find a bug or want to enhance the script, feel free to submit a pull request.
