import time
from googletrans import Translator, constants
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from presenter import JsoneFormater
from selenium.common.exceptions import NoSuchElementException
from model import save_json


class Parser:
    def __init__(self, qwery: str):
        self.qwery = qwery

    def rbc_parser(self, driver):
        """
        Парсер сайта РБК
        :param driver:
        :return:
        """
        url = 'https://www.rbc.ru/search/?query'

        link_list = []
        title_list = []
        description_list = []
        date_list = []
        all_data = []
        content_list = []

        driver.get(url + '=' + self.qwery)
        time.sleep(5)

        # TODO Скролинг страницы
        for scroll in range(0, 7): # количество прокруторк до конца страницы
            hight_page = driver.execute_script("return document.body.scrollHeight")
            # Прокручиваем страницу вниз
            driver.execute_script(f"window.scrollTo(0, {hight_page});")
            time.sleep(5)

        find_elements = driver.find_elements(By.CSS_SELECTOR, '.search-item')
        print(len(find_elements))  # количесвто полученный статей


        #TODO Получение данных
        for item in range(len(find_elements)):
            try:
                title = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__title').text
                description = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__text').text
                url = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__link').get_attribute('href')
                date = find_elements[item].find_element(By.CSS_SELECTOR, '.search-item__category').text
                # print(f'title= {title}')
                # print(f'description= {description}')
                # print(f'url= {url}')
                # print(f'date={date}')
                link_list.append(url)
                title_list.append(title)
                description_list.append(description)
                date_list.append(date)
            except NoSuchElementException:
                description = "Element not found"
                description_list.append(description)
                # print(f'description= {description}')
                continue

        for link in link_list:
            print(link)    # ссылки для перехода
            driver.get(link)
            time.sleep(5)
            try:
                content_list.append(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
                # print(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
            except NoSuchElementException:
                try:
                    content_list.append(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
                    # print(driver.find_element(By.CSS_SELECTOR, '.news-detail__content').text)
                except NoSuchElementException:
                    content_list.append("no element")
                    print("no element")
                    continue
                continue

        #TODO Сохранение данных
        for data in range(len(link_list)):
            json_dict = JsoneFormater().get_format()
            json_dict['title'] = title_list[data]
            json_dict['url'] = link_list[data]
            json_dict['description'] = description_list[data]
            json_dict['date'] = date_list[data]
            json_dict['content'] = content_list[data]
            json_dict['type_report'] = "MARKET_OVERVIEW"
            all_data.append(json_dict)

        # print(all_data)
        save_json(all_data)
