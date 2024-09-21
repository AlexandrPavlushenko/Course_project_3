from src.head_hunter_api import HHVacancyAPI
from src.database_create import DataBaseCreate

# Создаем БД
db = DataBaseCreate()
db.create_database("head_hunter")

# Создаем в БД таблицу для вакансий
db = DataBaseCreate(database="head_hunter")
db.create_table("vacancies", "vacancy_id INT, vacancy_name TEXT, area VARCHAR(100),"
                             "salary_from INT, salary_to INT,employer_id INT, employer_name TEXT,"
                             "vacancy_url CHAR(31), published_date DATE")

# Получаем данные с hh.ru и записываем их в таблицу БД
hh_api = HHVacancyAPI()
vacancies_list = []
quantity_page = 10  # Количество страниц (Каждая страница содержит 100 вакансий)

for page in range(quantity_page):
    vacancies = hh_api.get_data(search_query="Разработчик", area_id=1, page=page, per_page=100)
    for i in vacancies:
        if i['salary'] is None:
            salary_from = salary_to = None
        elif i['salary']['from'] is None and i['salary']['to']:
            salary_from = None
            salary_to = i['salary']['to']
        elif i['salary']['to'] is None and i['salary']['from']:
            salary_to = None
            salary_from = i['salary']['from']
        else:
            salary_from = i['salary']['from']
            salary_to = i['salary']['to']
        pub_date = i['published_at'][:10]
        vacancies_list.append(
            (i['id'], i['name'], i['area']['name'], salary_from, salary_to, i['employer'].get('id', None),
             i['employer']['name'], i['alternate_url'], pub_date))
db.clear_table("vacancies")
db.insert("vacancies", vacancies_list)
