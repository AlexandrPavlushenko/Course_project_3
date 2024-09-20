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
vacances = hh_api.get_data(search_query="Разработчик", area_id=3, per_page=100)
v_data = []
for i in vacances:
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
    time = i['published_at'][:10]
    v_data.append((i['id'], i['name'], i['area']['name'], salary_from, salary_to, i['employer']['name'],
                   i['alternate_url'], time))
db.clear_table("vacancies")
db.insert("vacancies", v_data)
