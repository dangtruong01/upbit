import requests
from bs4 import BeautifulSoup

# The URL of the page you want to scrape
base_url = 'https://coinmarketcap.com'
url = 'https://coinmarketcap.com/exchanges/upbit/?type=spot'

# Send a GET request to the page
exchange_response = requests.get(url)
coin_links = []

#Funciton to find all names of all coins listed
def find_names(table):
    if table:
        names = table.find_all('p',class_='sc-4984dd93-0 kKpPOn')

        #print out each
        for name in names:
            print(name.text)
    else:
        print("No names are found")

def scrape_coins_links(table):
# Check if the table is found
    if table:
        # Find all the 'a' tags within this table
        links = table.find_all('a', href=True)
        
        # Print out each link's href attribute
        for link in links:
            link_name = link['href']
            if link_name[:5] == 'https':
                continue
            coin_links.append(base_url + link_name)
    else:
        print("Table with the specified class not found.")

# Function to scrape data from each individual coin page
def scrape_individual_coin(coin_url):
    print(coin_url)
    # Send a GET request to the coin page
    coin_response = requests.get(coin_url)
    if coin_response.status_code == 200:
        # Parse the content of the coin page
        coin_soup = BeautifulSoup(coin_response.text, 'html.parser')

        # Extract project categories (tags)
        tags = coin_soup.find('div', class_ = 'sc-f70bb44c-0 sc-9ee74f67-0 iGa-diC')
        categories = tags.find_all('a', class_ ='cmc-link')
        for category in categories:
            print("Category:",category.text)

        #Extract project about information
        about = coin_soup.find('div', class_ = 'sc-5f3326dd-0 kAOboQ')
        paragraphs = about.find_all('p')
        text = ''
        for paragraph in paragraphs:
            text = text + paragraph.text
        print(text)

        #Extract listed CEX


    else:
        print(f"Failed to retrieve the coin webpage. Status code: {coin_response.status_code}")

# Check if the request was successful
if exchange_response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(exchange_response.text, 'html.parser')
    
    # Find the table with the specific class
    table = soup.find('table', class_='sc-14cb040a-3 ldpbBC cmc-table')

    # #Get all coins listed on upbit
    # find_names(table)

    #Scrape through all coins
    scrape_coins_links(table)
else:
    print(f"Failed to retrieve the webpage. Status code: {exchange_response.status_code}")

#Scrape data from each coin
for coin_link in coin_links:
    scrape_individual_coin(coin_link)
