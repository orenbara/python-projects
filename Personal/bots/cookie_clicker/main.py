from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

start_time = time.time()

# Define the chrome_driver object
service = Service("C:\\Users\\orenb\\Desktop\\programming\\100_Days_Python\\chrome_dev\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Define timeout
timeout = time.time() + 5
five_mins = time.time() + 5 * 60

# Get cookie for clicking purposes:
cookie_element = driver.find_element(by=By.ID, value="cookie")

# Get the html ID of the items in store:
store_item_elements = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
store_item_ids = [item_element.get_attribute("id") for item_element in store_item_elements]

while True:
    cookie_element.click()

    # following code will execute every 5 minutes:
    if time.time() > timeout:

        # Get <b> tags from store
        item_prices_element_list = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")

        # Convert <b> text to integer data:
        item_prices_list = []
        for item in item_prices_element_list:
            if item.text != "":
                cost = int(item.text.split("-")[1].strip().replace(",", ""))
                item_prices_list.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices_list)):
            cookie_upgrades[item_prices_list[n]] = store_item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        element_to_click = driver.find_element(by=By.ID, value=affordable_upgrades[max(affordable_upgrades.keys())])
        element_to_click.click()

        # Reload timeout
        timeout = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() > five_mins:
            cookie_per_s = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_s)
            break