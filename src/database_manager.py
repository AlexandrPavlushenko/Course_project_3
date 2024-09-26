import psycopg2


class DBManager:
    """Класс-менеджер для работы с БД PostgreSQL."""

    def __init__(self, host="localhost", user="postgres", password="Q1980qum%", database="postgres", port="5432"):
        self.__connection_params = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
        }

    def __execute_query(self, query):
        try:
            with psycopg2.connect(**self.__connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall() if query.strip().lower().startswith("select") else None
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def get_companies_and_vacancies_count(self):
        """Метод получения списка всех компаний и количества вакансий у каждой компании."""
        return self.__execute_query(
            "SELECT employer_name, COUNT(*) " 
            "FROM vacancies " 
            "GROUP BY employer_name " 
            "ORDER BY COUNT(*) DESC")

    def get_all_vacancies(self):
        """Метод получения списка всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""
        return self.__execute_query(
            "SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url " 
            "FROM vacancies")

    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям."""
        return (self.__execute_query("SELECT AVG((salary_from + salary_to) / 2) " 
                                     "FROM vacancies"))[0]

    def get_vacancies_with_higher_salary(self):
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        return self.__execute_query(
            "SELECT * "
            "FROM vacancies "
            "WHERE (salary_from + salary_to) / 2 > (SELECT AVG((salary_from + salary_to) / 2) "
            "FROM vacancies) "
            "ORDER BY salary_to DESC"
        )

    def get_vacancies_with_keyword(self, key_words):
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова"""
        return self.__execute_query(f"SELECT * " 
                                    "FROM vacancies " 
                                    "WHERE vacancy_name " 
                                    f"LIKE '%{key_words}%'")
