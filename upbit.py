import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
import time

# The URL of the page you want to scrape
base_url = 'https://coinmarketcap.com'
url = 'https://coinmarketcap.com/exchanges/upbit/?type=spot'

# Send a GET request to the page
coin_links = []
twitter_followers = []
coin_names = []
coin_info = []
coin_category = []
coin_telegram = []

#Funciton to find all names of all coins listed
def find_names(table):
    if table:
        names = table.find_all('p',class_='sc-4984dd93-0 kKpPOn')

        #print out each
        for name in names:
            coin_names.append(name.text)
    else:
        print("No names are found")

#Function to create list of all coins links
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

#Function to get each coin categories
def scrape_coin_categories(coin_soup):
    tags = coin_soup.find('div', class_ = 'sc-f70bb44c-0 sc-9ee74f67-0 iGa-diC')
    info = ''
    if tags:
        categories = tags.find_all('a', class_ ='cmc-link')
        for category in categories:
            # print("Category:",category.text)
            info += category.text
    coin_category.append(info)

#Function to get each coin information
def scrape_coin_info(coin_soup):
    about = coin_soup.find('div', class_ = 'sc-5f3326dd-0 kAOboQ')
    paragraphs = about.find_all('p')
    text = ''
    for paragraph in paragraphs:
        text = text + paragraph.text
    coin_info.append(text)

# #Function to scrapte coin's twitter
# def scrape_coin_twitter(coin_soup):
#     socials = coin_soup.find_all('div', class_ = 'sc-f70bb44c-0 sc-7f0f401-2 hEvwxv')[1]
#     # links = [social.find('div') for social in socials]
#     links = socials.find_all('a')
#     hrefs = [link.get('href') for link in links]

#     for href in hrefs:
#         if 'twitter' in href:
#             print('Twitter',href)
#             twitter_response = requests.get(href)
#             if twitter_response.status_code == 200:
#                 print("PASSSSSSSSSSSSSSS")
#                 twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')

#                 box = twitter_soup.find('div', class_ = 'css-175oi2r r-13awgt0 r-18u37iz r-1w6e6rj')
#                 followers = box.find_all('span', class_ = 'css-1qaijid r-bcqeeo r-qvutc0 r-poiln3')
                
#                 for follower in followers:
#                     print(follower.text)

#Function to scrapte coin's telegram
def scrape_coin_telegram(coin_soup):
    socials = coin_soup.find_all('div', class_ = 'sc-f70bb44c-0 sc-7f0f401-2 hEvwxv')[1]
    # links = [social.find('div') for social in socials]
    links = socials.find_all('a')
    hrefs = [link.get('href') for link in links]

    for href in hrefs:
        if 't.me' in href:
            print('Telegram:',href)
            telegram_response = requests.get(href)
            if telegram_response.status_code == 200:
                telegram_soup= BeautifulSoup(telegram_response.text, 'html.parser')
                box = telegram_soup.find('div', class_ = 'tgme_page_extra')
                if box:
                    text = box.text
                    members = text.split(',')
                    coin_telegram.append(members[0])
                else:
                    coin_telegram.append('0')
        else:
            coin_telegram.append('0')

# Function to scrape data from each individual coin page
def scrape_individual_coin(coin_url):
    print(coin_url)
    # Send a GET request to the coin page
    coin_response = requests.get(coin_url)
    if coin_response.status_code == 200:
        # Parse the content of the coin page
        coin_soup = BeautifulSoup(coin_response.text, 'html.parser')

        # Extract project categories (tags)
        scrape_coin_categories(coin_soup)

        #Extract project about information
        scrape_coin_info(coin_soup)

        # #Extract listed CEX

        # #Extract twitter
        # scrape_coin_twitter(coin_soup)

        #Extract tele
        scrape_coin_telegram(coin_soup)

    else:
        print(f"Failed to retrieve the coin webpage. Status code: {coin_response.status_code}")


# Setup the Selenium WebDriver
driver = webdriver.Chrome()
driver.get(url)  # replace with the actual URL

# # Loop to click the button until it disappears
while True:
    try:
        print("NOOOO")
        # Find the button by its class name (update the class name to match your button)
        button = driver.find_element(By.XPATH,"//button[@class='sc-2861d03b-0 iqkKeD sc-d36bb8b9-11 hQuCHd']")
        print(button)
        button.click()
        print("Button clicked")

        # # Wait for the button to be clickable
        # wait = WebDriverWait(driver, 10)  # Adjust timeout as needed
        # button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='sc-2861d03b-0 iqkKeD sc-d36bb8b9-11 hQuCHd']")))
        
        # # Check if the button is enabled
        # if button.is_enabled():
        #     button.click()
        #     print("Button clicked")
        # else:
        #     break  # If button is disabled, exit the loop
        
        # Wait for the page to load, adjust the sleep time as necessary
        time.sleep(5)
    except ElementClickInterceptedException:
        # If the click is intercepted by another element
        print("Click intercepted, trying again.")
        time.sleep(2)
    except NoSuchElementException:
        # If the button is not found, break from the loop
        print('rip')
        break

# Continue with the rest of your code or close the browser
# driver.quit()

exchange_response = requests.get(url)

# Check if the request was successful
if exchange_response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the table with the specific class
    table = soup.find('table', class_='sc-14cb040a-3 ldpbBC cmc-table')

    #Get all coins listed on upbit
    find_names(table)

    #Scrape through all coins
    scrape_coins_links(table)
else:
    print(f"Failed to retrieve the webpage. Status code: {exchange_response.status_code}")

#Scrape data from each coin
for coin_link in coin_links:
    scrape_individual_coin(coin_link)


print(coin_names)