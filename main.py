from src.head_hunter_api import HHVacancyAPI
from src.database_create import DataBaseCreate
from src.database_manager import DBManager
from tqdm import tqdm
from prettytable import PrettyTable
from colorama import Fore, Style


def main():
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
    quantity_page = 1  # Количество страниц (Каждая страница содержит 100 вакансий)
    read_bar_format = "%s{l_bar}%s{bar}" % (
        "\033[0;32m", "\033[0;32m")
    for page in tqdm(range(quantity_page), desc="Загрузка вакансий в базу данных...", colour="green",
                     bar_format=read_bar_format):
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

    # Главное меню
    dbm = DBManager(database='head_hunter')

    print("""\n-------------------------------------------Выберите пункт----------------------------------------------\n
    1. Cписок всех компаний и количества вакансий у каждой компании
    2. Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
    3. Средняя зарплата по вакансиям
    4. Список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5. Список всех вакансий, в названии которых содержатся ключевое слово
    6. Выход\n""")
    while True:
        choice = input()
        if choice == '6':
            break
        elif choice == '1':
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in
                                 ["Название компании", "Количество вакансий"]]
            for row in dbm.get_companies_and_vacancies_count():
                table.add_row([row[0], row[1]])
            print(table)
        elif choice == '2':
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in
                                 ["Название компании", "Название вакансии", "Зарплата от", "Зарплата до",
                                  "Ссылка на вакансию"]]
            for row in dbm.get_all_vacancies():
                table.add_row([row[i] for i in range(5)])
            print(table)
        elif choice == '3':
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in ["Средняя зарплата по вакансиям"]]
            table.add_row(dbm.get_avg_salary())
            print(table)
        elif choice == '4':
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in
                                 ["id вакансии", "Название вакансии", "Населенный пункт", "Зарплата от", "Зарплата до",
                                  "id компании", "Название компании", "Ссылка на вакансию", "Дата публикации"]]
            for row in dbm.get_vacancies_with_higher_salary():
                table.add_row([row[i] for i in range(9)])
            print(table)
        elif choice == '5':
            key_word = input("Введите ключевое слово: ")
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in
                                 ["id вакансии", "Название вакансии", "Населенный пункт", "Зарплата от", "Зарплата до",
                                  "id компании", "Название компании", "Ссылка на вакансию", "Дата публикации"]]
            for row in dbm.get_vacancies_with_keyword(key_word):
                table.add_row([row[i] for i in range(9)])
            print(table)


if __name__ == "__main__":
    main()
