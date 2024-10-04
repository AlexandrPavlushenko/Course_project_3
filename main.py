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

    # Создаем в БД таблицу для работодателей
    db = DataBaseCreate(database="head_hunter")
    db.create_table("employers", "employer_id INT PRIMARY KEY, employer_name TEXT,"
                                 "employer_url VARCHAR(31), open_vacancies INT")

    # Создаем в БД таблицу для вакансий
    db.create_table("vacancies", "vacancy_id INT PRIMARY KEY, vacancy_name TEXT,"
                                 "area VARCHAR(255), salary_from INT, salary_to INT, employer_id INT,"
                                 "vacancy_url VARCHAR(31), published_date DATE,"
                                 "FOREIGN KEY (employer_id) REFERENCES employers(employer_id) ON DELETE CASCADE")

    # Получаем данные с hh.ru и записываем их в таблицы БД
    id_employers = [11481151, 783222, 10842295, 11444595, 10748139, 972961, 253771, 701365, 11482656, 5345596]
    hh_api = HHVacancyAPI()
    employers_list = []
    vacancies_list = []

    read_bar_format = "%s{l_bar}%s{bar}" % (
        "\033[0;32m", "\033[0;32m")

    for emp in tqdm(id_employers, desc="Загрузка таблицы работодателей в базу данных...", colour="green",
                    bar_format=read_bar_format):
        empl = hh_api.get_employer(emp)
        employers_list.append((empl['id'], empl['name'], empl['alternate_url'], empl['open_vacancies']))
    db.clear_table("employers")
    db.insert("employers", employers_list)

    read_bar_format = "%s{l_bar}%s{bar}" % (
        "\033[0;32m", "\033[0;32m")
    for vac in tqdm(id_employers, desc="Загрузка таблицы вакансий в базу данных...", colour="green",
                    bar_format=read_bar_format):
        vacancies = hh_api.get_data(vac)
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
                 i['alternate_url'], pub_date))
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
                                  "id компании", "Ссылка на вакансию", "Дата публикации"]]
            for row in dbm.get_vacancies_with_higher_salary():
                table.add_row([row[i] for i in range(8)])
            print(table)
        elif choice == '5':
            key_word = input("Введите ключевое слово.Внимание! Регистр букв важен! : ")
            table = PrettyTable()
            table.field_names = [f"{Fore.GREEN}{name}{Style.RESET_ALL}" for name in
                                 ["id вакансии", "Название вакансии", "Населенный пункт", "Зарплата от", "Зарплата до",
                                  "id компании", "Ссылка на вакансию", "Дата публикации"]]
            for row in dbm.get_vacancies_with_keyword(key_word):
                table.add_row([row[i] for i in range(8)])
            print(table)


if __name__ == "__main__":
    main()
