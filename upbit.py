import requests
from bs4 import BeautifulSoup

# The URL of the page you want to scrape
url = 'https://coinmarketcap.com/exchanges/upbit/?type=spot'

# Send a GET request to the page
response = requests.get(url)
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
            coin_links.append(link_name)
    else:
        print("Table with the specified class not found.")

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table with the specific class
    table = soup.find('table', class_='sc-14cb040a-3 ldpbBC cmc-table')

    # #Get all coins listed on upbit
    # find_names(table)

    #Scrape through all coins
    scrape_coins_links(table)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
