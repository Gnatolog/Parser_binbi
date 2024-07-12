import time
from googletrans import Translator, constants
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from presenter import JsoneFormater
from selenium.common.exceptions import NoSuchElementException


class Parser:
    def __init__(self, qwery: str):
        self.qwery = qwery

    def change_using(self, driver, element_name, ):
        """
        Метод перехода по ссылкам
        :param element_name: имя селектора
        :param driver:
        :return:
        """

        find_elements = driver.find_elements(By.CSS_SELECTOR, element_name)

        return find_elements

    def rbc_parser(self, driver):
        url = 'https://www.rbc.ru/search/?query'

        link_list = []
        title_list = []
        description_list = []
        date_list = []
        content_list = []

        driver.get(url + '=' + self.qwery)
        time.sleep(5)
        find_elements = driver.find_elements(By.CSS_SELECTOR, '.search-item')
        for item in range(len(find_elements)):
            try:
                title = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__title').text
                description = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__text').text
                url = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__link').get_attribute('href')
                date = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__category').text
                print(f'title= {title}')
                print(f'description= {description}')
                print(f'url= {url}')
                print(f'date={date}')
                link_list.append(url)
                title_list.append(title)
                description_list.append(description)
                date_list.append(date)
            except NoSuchElementException:
                description = "Element not found"
                print(f'description= {description}')
                continue

        for link in link_list:
            print(link)
            driver.get(link)
            time.sleep(5)
            try:
                print(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
            except NoSuchElementException:
                try:
                    print(driver.find_element(By.CSS_SELECTOR, '.news-detail__content').text)
                except NoSuchElementException:
                    print("no element")
                    continue
                continue
