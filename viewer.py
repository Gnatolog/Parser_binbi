import time
from googletrans import Translator, constants
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from presenter import JsoneFormater
from selenium.common.exceptions import NoSuchElementException
from model import save_json
import requests
import re
import json


class Parser:
    def __init__(self, qwery: str):
        self.qwery = qwery

    def request_db(self, request: list):

        with open('db_article.json', "r", encoding='utf-8') as fl:
            db = json.load(fl)
            for art in db:
                if request[0] in art.keys():
                    print("Возвращаем уже существующий отчет")
                    return art.values()

                else:
                    for request_art in request:
                        if request_art in art.keys():
                            print("запуск генерацию отчета")
                            index_art = db.index(art)
                            art[request[0]] = art[request_art]
                            db[index_art].pop(request_art)
                            with open('db_article.json', 'w', encoding='utf-8') as file_update:
                                json.dump(db, file_update, ensure_ascii=False, indent=2)
                            return " возвращаем обновленный Отчёт"
                        else:
                            print("догружаем статьи а ии")

                    print("запускаем отчет на формирование")

                    art[request[0]] = {"new_report": "response"}
                    with open('db_article.json', 'w', encoding='utf-8') as file_new:
                        json.dump(db, file_new, ensure_ascii=False, indent=2)

                    return 'Возвращаем новый отчёт'

    def date_valid(self, date: str) -> str:
        month_dict = {
            "янв": "01",
            "фев": "02",
            "мар": "03",
            "апр": "04",
            "мая": "05",
            "июн": "06",
            "июл": "07",
            "авг": "08",
            "сен": "09",
            "окт": "10",
            "ноя": "11",
            "дек": "12"
        }

        date_time_pattern_long = r'\d{2}\s\w{3}\s\d{4},\s\d{2}:\d{2}'
        date_time_pattern_short = r'\d{2}\s\w{3},\s\d{2}:\d{2}'
        count = 0

        for dig in date:
            if dig.isdigit():
                count += 1

        if count > 6:
            clear_date = re.search(date_time_pattern_long, date).group()
            clear_date = clear_date.replace(',', ' ')
            clear_date = clear_date.split()
            valid_date = str(
                clear_date[2] + "-" + month_dict[clear_date[1].lower()] + "-" + clear_date[0] + " " + clear_date[
                    3] + ":00")
        elif count == 6:
            clear_date = re.search(date_time_pattern_short, date).group()
            clear_date = clear_date.replace(',', ' ')
            clear_date = clear_date.split()
            valid_date = str(
                "2024" + "-" + month_dict[clear_date[1].lower()] + "-" + clear_date[0] + " " + clear_date[
                    2] + ":00")
        else:
            valid_date = "2024-06-17 16:23:00"

        return valid_date

    def rbc_parser(self, driver):
        """
        Парсер сайта РБК
        :param driver:
        :return:
        """
        url = 'https://www.rbc.ru/search/?query'
        url_add_article = 'http://147.45.152.87:8080/api/v1/article/addArticle'
        url_get_all_article = 'http://147.45.152.87:8080//api/v1/article/findAllArticles'

        link_list = []
        title_list = []
        description_list = []
        date_list = []
        all_data = []
        content_list = []

        driver.get(url + '=' + self.qwery)
        time.sleep(5)

        # # TODO Скролинг страницы
        # for scroll in range(0, 1):  # количество прокруторк до конца страницы
        #     hight_page = driver.execute_script("return document.body.scrollHeight")
        #     # Прокручиваем страницу вниз
        #     driver.execute_script(f"window.scrollTo(0, {hight_page});")
        #     time.sleep(5)

        find_elements = driver.find_elements(By.CSS_SELECTOR, '.search-item')
        zero_find_element = find_elements[0].find_element(By.CSS_SELECTOR, '.search-item__title').text
        with (open('db_article.json', "r", encoding='utf-8') as fl):
            db = json.load(fl)
            for art in db:
                if zero_find_element in art.keys():
                    print("Возвращаем уже существующий отчет")
                    return art.values()
                else:
                    #TODO Получение данных
                    for item in range(len(find_elements)):
                        try:
                            if item in art.keys():
                                print("запуск генерацию отчета")
                                index_art = db.index(art)
                                art[find_elements[0].find_element(By.CSS_SELECTOR, '.search-item__title').text] = art[item]
                                db[index_art].pop(item)
                                with open('db_article.json', 'w', encoding='utf-8') as file_update:
                                    json.dump(db, file_update, ensure_ascii=False, indent=2)
                                return " возвращаем обновленный Отчёт"
                            else:
                                print("догружаем статьи а ии")
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

                        print(link)  # ссылки для перехода
                        driver.get(link)
                        time.sleep(1)
                        try:
                            # content_list.append(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
                            data_add_article = {
                                "title": title_list[link_list.index(link)],
                                "url": link,
                                "description": description_list[link_list.index(link)],
                                "date": self.date_valid(date_list[link_list.index(link)]),
                                "content": driver.find_element(By.CSS_SELECTOR, '.article__text').text,
                                "typeReport": "MARKET_OVERVIEW"
                            }


                            headers = {
                                'Content-Type': 'application/json'
                            }
                            response = requests.post(url_add_article, data=json.dumps(data_add_article), headers=headers)
                            if response.status_code == 200:
                                print(response.text)
                            else:
                                print(f'Error: {response.status_code} - {response.text}')


                        except NoSuchElementException:
                            try:
                                # content_list.append(driver.find_element(By.CSS_SELECTOR, '.article__text').text)
                                # print(driver.find_element(By.CSS_SELECTOR, '.news-detail__content').text)

                                data_add_article = {
                                    "title": title_list[link_list.index(link)],
                                    "url": link,
                                    "description": description_list[link_list.index(link)],
                                    "date": self.date_valid(date_list[link_list.index(link)]),
                                    "content": driver.find_element(By.CSS_SELECTOR, '.article__text').text,
                                    "typeReport": "MARKET_OVERVIEW"
                                }

                                headers = {
                                    'Content-Type': 'application/json'
                                }
                                response = requests.post(url_add_article, data=json.dumps(data_add_article),
                                                         headers=headers)
                                if response.status_code == 200:
                                    print(response.text)
                                else:
                                    print(f'Error: {response.status_code} - {response.text}')

                            except NoSuchElementException:
                                # content_list.append("no element")
                                data_add_article = {
                                    "title": title_list[link_list.index(link)],
                                    "url": link,
                                    "description": description_list[link_list.index(link)],
                                    "date": self.date_valid(date_list[link_list.index(link)]),
                                    "content": "no element",
                                    "typeReport": "MARKET_OVERVIEW"
                                }

                                headers = {
                                    'Content-Type': 'application/json'
                                }
                                response = requests.post(url_add_article, data=json.dumps(data_add_article),
                                                         headers=headers)
                                if response.status_code == 200:
                                    print(response.text)
                                else:
                                    print(f'Error: {response.status_code} - {response.text}')

                                continue
                            continue

                    print("запускаем отчет на формирование")

                    art[zero_find_element] = {"new_report": "response"}

                    with open('db_article.json', 'w', encoding='utf-8') as file_new:
                        json.dump(db, file_new, ensure_ascii=False, indent=2)

                    # Запрос на получение всех статей
                    response = requests.get(url_get_all_article) # OK
                    if response.status_code == 200:
                        print(response.text)
                    else:
                        print(f'Error: {response.status_code} - {response.text}')


