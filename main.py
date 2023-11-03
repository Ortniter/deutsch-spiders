from selenium import webdriver
import config

driver = webdriver.Chrome(service=config.get_chrome_service(), options=config.get_chrome_options())
driver.get("https://medium.com")
print(driver.page_source)
print("Finished!")
