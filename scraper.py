import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Browser setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Background mein run hone ke liye
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://markaz-clone.onrender.com/"
driver.get(url)

# Wait for page/JS to load completely
time.sleep(3)

products = []

# XPath se saare product cards extract karein
cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'card')]")

for card in cards:
    try:
        title = card.find_element(By.XPATH, ".//h5").text.strip()
    except:
        title = "N/A"
        
    try:
        price = card.find_element(By.XPATH, ".//p[contains(@class, 'price')] | .//p").text.strip()
    except:
        price = "N/A"
        
    try:
        badge = card.find_element(By.XPATH, ".//span[contains(@class, 'badge')]").text.strip()
    except:
        badge = "Regular"
        
    try:
        img_url = card.find_element(By.XPATH, ".//img").get_attribute("src")
    except:
        img_url = "No Image"

    if title != "N/A" and title != "":
        products.append({
            "Product Name": title,
            "Price": price,
            "Badge": badge,
            "Image URL": img_url
        })

driver.quit()

# Data ko Excel file mein save karein
df = pd.DataFrame(products)
df.to_excel("Markaz_Products.xlsx", index=False)
print("XPath scraping complete! Data saved to Markaz_Products.xlsx")