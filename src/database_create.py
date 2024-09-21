import psycopg2


class DataBaseCreate:
    """Класс для создания БД и таблиц в PostgreSQL"""

    def __init__(self, host='localhost', user='postgres', password='Q1980qum%', database='postgres', port='5432'):
        self.__connection_params = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }

    def __str__(self):
        return f"База данных: {self.__connection_params['database']}"

    def __open(self):
        try:
            self.__connection = psycopg2.connect(**self.__connection_params)
            self.__connection.autocommit = True
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(f"Ошибка при открытии соединения: {e}")

    def __close(self):
        self.__cursor.close()
        self.__connection.close()

    def create_database(self, database):
        """Метод создания БД"""
        try:
            query_non_db = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"
            query = f"CREATE DATABASE {database};"
            self.__open()
            self.__cursor.execute(query_non_db, [database])
            exists = self.__cursor.fetchone()
            if not exists:
                self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            self.__close()

    def create_table(self, table_name, table_structure):
        """Метод создания таблицы в БД"""
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name}({table_structure})"
            self.__open()
            self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            self.__close()

    def insert(self, table, values):
        """Метод записи данных в таблицу БД"""
        try:
            query = f"INSERT INTO {table} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.__open()
            self.__cursor.executemany(query, values)
        except Exception as e:
            print(f"Ошибка записи данных в таблицу: {e}")
        finally:
            self.__close()

    def select(self, table, column="*"):
        """Метод возвращающий данные из таблицы БД"""
        try:
            query = f"SELECT {column} FROM {table}"
            self.__open()
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
        except Exception as e:
            print(f"Ошибка считывания данных из таблицы: {e}")
        else:
            return rows
        finally:
            self.__close()

    def clear_table(self, table):
        """Метод полного удаления данных из таблицы БД"""
        try:
            query = f"DELETE FROM {table};"
            self.__open()
            self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка удаления данных из таблицы: {e}")
        finally:
            self.__close()
