from abc import ABC, abstractmethod


class AbstractDataBase(ABC):
    """Абстрактный класс для работы с БД"""

    def __init__(self, host, user, password, database, port):
        """Инициализация БД c переданными параметрами подключения"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    @abstractmethod
    def open(self):
        """Открытие БД"""
        pass

    @abstractmethod
    def close(self):
        """Закрытие БД"""
        pass


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_data(self, *args, **kwargs):
        """Метод получения данных API"""
        pass
