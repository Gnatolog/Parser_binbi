from presenter import JsoneFormater
import requests
import json


url_hello = 'http://147.45.152.87:8080/api/v1/openai/hello'
url_add_article = 'http://147.45.152.87:8080/api/v1/article/addArticle'
url_get_all_article = 'http://147.45.152.87:8080//api/v1/article/findAllArticles'



data_add_article = {
    "title": "В Татарстане создадут кластер разработки компьютерных игр",
    "url": "https://rt.rbc.ru/tatarstan/freenews/668f8e349a79475faa159212",
    "description": "В Татарстане хотят начать разрабатывать компьютерные игры. Для этого в Казани создадут GameDev-кластер. Разработчикам окажут содействие в привлечении инвестиций и окажут другую поддержку",
    "date": "2023-06-19 00:00:00",
    "content": "В Татарстане хотят начать разрабатывать компьютерные игры. Для этого в Казани создадут GameDev-кластер. Разработчикам окажут содействие в привлечении инвестиций и окажут другую поддержку\nФото: РБК Татарстан\nВ этом году в Казани на базе IT-парка на ул. Петербургской намерены запустить GameDev-кластер. Об этом рассказал министр цифрового развития, информационных технологий и связи РТ Айрат Хайруллин.\nGameDev (games development) – это процесс создания и разработки видеоигр. Он включает в себя программирование, дизайн игрового мира, создание графики и звукового сопровождения, тестирование, оптимизацию и выполнение других задач вплоть до выпуска на рынок.\nРазработчикам игр предлагается акселерационная программа, пространство для развития перспективных проектов и доступ к инвестициям специальных фондов.\n«Мы видим большие возможности в области GameDev. Не только разработка компьютерных игр, киберспорт. Это очень быстрорастущий рынок. Это возможность экспортировать не только сам продукт, но и ценности, культурный код своей страны», — сказал Хайруллин.\nПодпишись на Telegram РБК Татарстан",
    "typeReport": "MARKET_OVERVIEW"
}


headers = {
    'Content-Type': 'application/json'
}



# Проверка связи
# response = requests.get(url_hello)    # OK

# Запрос на добавление статей
# response = requests.post(url_add_article, data=json.dumps(data_add_article), headers=headers)

# Запрос на получение всех статей
response = requests.get(url_get_all_article) # OK




if response.status_code == 200:
    print(response.text)
else:
    print(f'Error: {response.status_code} - {response.text}')