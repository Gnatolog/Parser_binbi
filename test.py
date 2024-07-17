from presenter import JsoneFormater
import requests
import json
import re

# url_hello = 'http://147.45.152.87:8080/api/v1/openai/hello'
# url_add_article = 'http://147.45.152.87:8080/api/v1/article/addArticle'
# url_get_all_article = 'http://147.45.152.87:8080//api/v1/article/findAllArticles'
#
#
#
# data_add_article = {
#     "title": "В Татарстане создадут кластер разработки компьютерных игр",
#     "url": "https://rt.rbc.ru/tatarstan/freenews/668f8e349a79475faa159212",
#     "description": "В Татарстане хотят начать разрабатывать компьютерные игры. Для этого в Казани создадут GameDev-кластер. Разработчикам окажут содействие в привлечении инвестиций и окажут другую поддержку",
#     "date": "2023-06-19 00:00:00",
#     "content": "В Татарстане хотят начать разрабатывать компьютерные игры. Для этого в Казани создадут GameDev-кластер. Разработчикам окажут содействие в привлечении инвестиций и окажут другую поддержку\nФото: РБК Татарстан\nВ этом году в Казани на базе IT-парка на ул. Петербургской намерены запустить GameDev-кластер. Об этом рассказал министр цифрового развития, информационных технологий и связи РТ Айрат Хайруллин.\nGameDev (games development) – это процесс создания и разработки видеоигр. Он включает в себя программирование, дизайн игрового мира, создание графики и звукового сопровождения, тестирование, оптимизацию и выполнение других задач вплоть до выпуска на рынок.\nРазработчикам игр предлагается акселерационная программа, пространство для развития перспективных проектов и доступ к инвестициям специальных фондов.\n«Мы видим большие возможности в области GameDev. Не только разработка компьютерных игр, киберспорт. Это очень быстрорастущий рынок. Это возможность экспортировать не только сам продукт, но и ценности, культурный код своей страны», — сказал Хайруллин.\nПодпишись на Telegram РБК Татарстан",
#     "typeReport": "MARKET_OVERVIEW"
# }
#
#
# headers = {
#     'Content-Type': 'application/json'
# }


# Проверка связи
# response = requests.get(url_hello)    # OK

# Запрос на добавление статей
# response = requests.post(url_add_article, data=json.dumps(data_add_article), headers=headers)

# Запрос на получение всех статей
# response = requests.get(url_get_all_article) # OK


#
# if response.status_code == 200:
#     print(response.text)
# else:
#     print(f'Error: {response.status_code} - {response.text}')


# valid_date = "2023-06-19 00:00:00"
# date_time_long = "РБК+, Новости партнеров, 28 ноя 2023, 14:39"
# date_time_short = "РБК, 11 июл, 14:38"


# def date_valid(date: str) -> str:
#     month_dict = {
#         "янв": "01",
#         "фев": "02",
#         "мар": "03",
#         "апр": "04",
#         "май": "05",
#         "июн": "06",
#         "июл": "07",
#         "авг": "08",
#         "сен": "09",
#         "окт": "10",
#         "ноя": "11",
#         "дек": "12"
#     }
#
#     valid_date = ""
#     date_time_pattern_long = r'\d{2}\s\w{3}\s\d{4},\s\d{2}:\d{2}'
#     date_time_pattern_short = r'\d{2}\s\w{3},\s\d{2}:\d{2}'
#     count = 0
#
#     for dig in date:
#         if dig.isdigit():
#             count += 1
#     if count > 6:
#         clear_date = re.search(date_time_pattern_long, date).group()
#         clear_date = clear_date.replace(',', ' ')
#         clear_date = clear_date.split()
#         valid_date = str(
#             clear_date[2] + "-" + month_dict[clear_date[1].lower()] + "-" + clear_date[0] + " " + clear_date[3] + ":00")
#     else:
#         clear_date = re.search(date_time_pattern_short, date).group()
#         clear_date = clear_date.replace(',', ' ')
#         clear_date = clear_date.split()
#         valid_date = str(
#             "2024" + "-" + month_dict[clear_date[1].lower()] + "-" + clear_date[0] + " " + clear_date[2] + ":00")
#
#     return valid_date

#
# print(date_valid(date_time_short))


# method_request_db


request_list = ["В Татарстане создадут кластер разработки компьютерных игр 9",
                "В Татарстане создадут кластер разработки компьютерных игр 2",
                "В Татарстане создадут кластер разработки компьютерных игр 3",
                "В Татарстане создадут кластер разработки компьютерных игр 5", ]


def request_db(request: list):

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


print(request_db(request_list))
