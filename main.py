from src.head_hunter_api import HHVacancyAPI
from src.database_create import DataBaseCreate
from src.database_manager import DBManager
from tqdm import tqdm

# Создаем БД
# db = DataBaseCreate()
# db.create_database("head_hunter")

# Создаем в БД таблицу для вакансий
# db = DataBaseCreate(database="head_hunter")
# db.create_table("vacancies", "vacancy_id INT, vacancy_name TEXT, area VARCHAR(100),"
#                              "salary_from INT, salary_to INT,employer_id INT, employer_name TEXT,"
#                              "vacancy_url CHAR(31), published_date DATE")

# Получаем данные с hh.ru и записываем их в таблицу БД
# hh_api = HHVacancyAPI()
# vacancies_list = []
# quantity_page = 10  # Количество страниц (Каждая страница содержит 100 вакансий)
# read_bar_format = "%s{l_bar}%s{bar}" % (
#     "\033[0;32m", "\033[0;32m")
# for page in tqdm(range(quantity_page), desc="Загрузка вакансий в базу данных...", colour="green",
#                  bar_format=read_bar_format):
#     vacancies = hh_api.get_data(search_query="Разработчик", area_id=1, page=page, per_page=100)
#     for i in vacancies:
#         if i['salary'] is None:
#             salary_from = salary_to = None
#         elif i['salary']['from'] is None and i['salary']['to']:
#             salary_from = None
#             salary_to = i['salary']['to']
#         elif i['salary']['to'] is None and i['salary']['from']:
#             salary_to = None
#             salary_from = i['salary']['from']
#         else:
#             salary_from = i['salary']['from']
#             salary_to = i['salary']['to']
#         pub_date = i['published_at'][:10]
#         vacancies_list.append(
#             (i['id'], i['name'], i['area']['name'], salary_from, salary_to, i['employer'].get('id', None),
#              i['employer']['name'], i['alternate_url'], pub_date))
# db.clear_table("vacancies")
# db.insert("vacancies", vacancies_list)

import tkinter as tk
from tkinter import messagebox
import getpass

dbm = DBManager()  # Создадим экземпляр класса


def companies_and_vacancies_count():
    messagebox.showinfo("Пункт", "Пункт 1")


def all_vacancies():
    messagebox.showinfo("Пункт 2", "Пункт 2")


def avg_salary():
    messagebox.showinfo("Пункт 3", "Пункт 3")


def vacancies_with_higher_salary():
    messagebox.showinfo("Пункт 4", "Пункт 4")


def vacancies_with_keyword():
    def get_input():
        # Получаем текст из поля ввода и присваиваем его переменной
        user_input = entry.get()
        root.destroy()

        messagebox.showinfo("Пункт 5", f"{user_input}")

    # Создаем главное окно
    root = tk.Tk()
    root.title("Ключевое слово")

    # Устанавливаем размеры окна
    root.geometry("300x150")

    # Создаем поле ввода
    entry = tk.Entry(root, width=30)
    entry.pack(pady=10)

    # Создаем кнопку для подтверждения ввода
    btn_submit = tk.Button(root, text="Подтвердить", command=get_input)
    btn_submit.pack(pady=5)

    # Создаем метку для отображения результата
    label = tk.Label(root, text="")
    label.pack(pady=10)

    # Запуск главного цикла
    root.mainloop()


def exit_program():
    root.quit()


# Создаем главное окно
root = tk.Tk()
root.title("Менеджер базы данных")

# Устанавливаем размеры окна
root.geometry("700x300")  # Ширина 800 пикселей и высота 400 пикселей

# Создаем кнопки
btn_companies_and_vacancies_count = tk.Button(root, text="Список всех компаний и количество вакансий у каждой компании",
                                              command=companies_and_vacancies_count, width=86)
btn_companies_and_vacancies_count.pack(pady=10)

btn_all_vacancies = tk.Button(root, text="Cписок всех вакансий с указанием названия компании,"
                                         " названия вакансии, зарплаты и ссылки на вакансию", command=all_vacancies)
btn_all_vacancies.pack(pady=10)

btn_avg_salary = tk.Button(root, text="Cредняя зарплата по вакансиям", command=avg_salary, width=86)
btn_avg_salary.pack(pady=10)

btn_vacancies_with_higher_salary = tk.Button(root,
                                             text="Список всех вакансий, у которых зарплата "
                                                  "выше средней по всем вакансиям",
                                             command=vacancies_with_higher_salary, width=86)
btn_vacancies_with_higher_salary.pack(pady=10)

btn_vacancies_with_keyword = tk.Button(root,
                                       text="Список всех вакансий, в названии"
                                            " которых содержится ключевое слово",
                                       command=vacancies_with_keyword,
                                       width=86)
btn_vacancies_with_keyword.pack(pady=10)

btn_exit = tk.Button(root, text="Выход", command=exit_program, width=86)
btn_exit.pack(pady=10)


# Запуск главного цикла
root.mainloop()
