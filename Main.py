
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")


try:
    # Dismiss language
    language_button = driver.find_element(by=By.ID, value="langSelect-EN")
    
    language_button.click()
    
except NoSuchElementException:
    print("Language selection not found")



# Find the item to click
cookie = driver.find_element(by=By.ID, value="bigCookie")

# All store items 
item_ids = [f"product{n}" for n in range(18)]

#timers

wait_time = 10 
timeout = time() + wait_time  # Check for purchases every 10 seconds

ten_min = time() + 60 * 10 # Final result


while True:
    cookie.click()

    # Every 10 seconds, try to buy the most expensive item we can afford
    
    if time() > timeout:
        try:
            cookies_element = driver.find_element(by=By.ID, value="cookies")
            cookie_text = cookies_element.text
            
            cookie_count = int(cookie_text.split()[0].replace(",", ""))

            
            products = driver.find_elements(by=By.CSS_SELECTOR, value="div[id^='product']")

            # Find the most expensive item 
            best_item = None
            for product in reversed(products):  #find the most expensive item
                # Check if item is available and affordable 
                if "enabled" in product.get_attribute("class"):
                    best_item = product
                    break

            # Buy the best item if found
            if best_item:
                best_item.click()
                print(f"Bought item: {best_item.get_attribute('id')}")

        except (NoSuchElementException, ValueError):
            print("Couldn't find cookie count or items")

        # Reset timer
        timeout = time() + wait_time

    # Stop after 10 minutes
    if time() > ten_min:
        try:
            cookies_element = driver.find_element(by=By.ID, value="cookies")
            print(f"Final result: {cookies_element.text}")
        except NoSuchElementException:
            print("Couldn't get final cookie count")
        break
