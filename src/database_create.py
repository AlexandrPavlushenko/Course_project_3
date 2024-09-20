import psycopg2
from src.abs_classes import AbstractDataBase


class DataBaseCreate(AbstractDataBase):
    """Класс для создания БД и таблиц в PostgreSQL"""

    def __init__(self, host='localhost', user='postgres', password='Q1980qum%', database='postgres', port='5432'):
        super().__init__(host, user, password, database, port)
        self.__connection = None
        self.__cursor = None

    def __str__(self):
        return f"База данных: {self.database}"

    def open(self):
        """Открытие соединения с сервером PostgreSQL."""
        try:
            self.__connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.__connection.autocommit = True
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(f"Ошибка при открытии соединения: {e}")

    def close(self):
        """Закрытие соединения с сервером PostgreSQL."""
        self.__cursor.close()
        self.__connection.close()

    def create_database(self, database):
        """Метод создания БД"""
        try:
            query_non_db = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;"
            query = f"CREATE DATABASE {database}"
            self.open()
            self.__cursor.execute(query_non_db, [database])
            exists = self.__cursor.fetchone()
            if not exists:
                self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            self.close()

    def create_table(self, table_name, table_structure):
        """Метод создания таблицы в БД"""
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name}({table_structure})"
            self.open()
            self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            self.close()

    def insert(self, table, values):
        """Метод записи данных в таблицу БД"""
        try:
            query = f"INSERT INTO {table} VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.open()
            self.__cursor.executemany(query, values)
        except Exception as e:
            print(f"Ошибка записи данных в таблицу: {e}")
        finally:
            self.close()

    def select(self, table, column="*"):
        """Метод возвращающий данные из таблицы БД"""
        try:
            query = f"SELECT {column} FROM {table}"
            self.open()
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
        except Exception as e:
            print(f"Ошибка считывания данных из таблицы: {e}")
        else:
            return rows
        finally:
            self.close()

    def clear_table(self, table):
        """Метод полного удаления данных из таблицы БД"""
        try:
            query = f"DELETE FROM {table}"
            self.open()
            self.__cursor.execute(query)
        except Exception as e:
            print(f"Ошибка удаления данных из таблицы: {e}")
        finally:
            self.close()
