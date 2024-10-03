import requests


class HHVacancyAPI:
    """Класс API запроса для получения данных о вакансиях на сайте hh.ru"""

    __base_url = "https://api.hh.ru/vacancies"
    __area_url = "https://api.hh.ru/areas"
    __employers_url = "https://api.hh.ru/employers"

    def get_data(self, employer_id):
        """Метод прлучения данных о вакнсиях"""
        params = {"employer_id": employer_id}
        response = requests.get(self.__base_url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return []

    def get_employer(self, id_employer):
        """Метод получения данных о работодателях"""
        response = requests.get(f"{self.__employers_url}/{id_employer}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return []

    @staticmethod
    def get_area_id(user_area):
        """Метод получения id населенного пункта"""
        response = requests.get(HHVacancyAPI.__area_url)
        if response.status_code == 200:
            data_list = response.json()
            for regions in data_list:
                for region in regions["areas"]:
                    if region["name"] == user_area:
                        return int(region["id"])
                    elif not region["areas"]:
                        continue
                    for area in region["areas"]:
                        if area["name"] == user_area:
                            return int(area["id"])
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return None
