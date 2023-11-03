from selenium import webdriver
import config

driver = webdriver.Chrome(executable_path=config.CHROMEDRIVER_PATH, chrome_options=config.get_chrome_options())
driver.get("https://medium.com")
print(driver.page_source)
print("Finished!")
