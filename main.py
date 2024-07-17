from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from viewer import Parser

# поключаем driver
# region parametr Brauser
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new")  # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome()  # режим браузера:  options true безгаловый

qweru = 'Футбол'
#

rdc = Parser(qweru)
rdc_parser = rdc.rbc_parser(driver)



