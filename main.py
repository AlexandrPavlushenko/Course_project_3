from src.head_hunter_api import HHVacancyAPI
from src.database_create import DataBaseCreate

# Создаем БД
db = DataBaseCreate()
db.create_database("head_hunter")
del db

# Создаем в БД таблицу для вакансий
db = DataBaseCreate(database="head_hunter")
db.create_table("vacancies", "vacancy_id INT, vacancy_name VARCHAR(100), area VARCHAR(100),"
                             "salary_from VARCHAR(20), salary_to VARCHAR(20), employer_name VARCHAR(100),"
                             "vacancy_url VARCHAR(100), published_date DATE")

# Получаем данные с hh.ru и записываем их в таблицу БД
hh_api = HHVacancyAPI()
vacancies = hh_api.get_data(search_query="Разработчик", area_id=1, per_page=100)
vacancies_list = []
for i in vacancies:
    if i['salary'] is None:
        salary_from = salary_to = "Не указана"
    elif i['salary']['from'] is None and i['salary']['to']:
        salary_from = "Не указана"
        salary_to = i['salary']['to']
    elif i['salary']['to'] is None and i['salary']['from']:
        salary_to = "Не указана"
        salary_from = i['salary']['from']
    else:
        salary_from = i['salary']['from']
        salary_to = i['salary']['to']
    pub_date = i['published_at'][:10]
    vacancies_list.append((i['id'], i['name'], i['area']['name'], salary_from, salary_to, i['employer']['name'],
                   i['alternate_url'], pub_date))
db.clear_table("vacancies")
db.insert("vacancies", vacancies_list)
