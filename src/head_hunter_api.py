import requests
from src.abs_classes import AbstractAPI


class HHVacancyAPI(AbstractAPI):
    """Класс API запроса для получения данных о вакансиях на сайте hh.ru """
    __base_url = "https://api.hh.ru/vacancies"
    __area_url = "https://api.hh.ru/areas"

    def get_data(self, search_query='', area_id=None, page=0, per_page=100, employer_id=None):
        """Метод прлучения данных о вакнсиях"""
        params = {"text": f"NAME:{search_query}", "area": area_id, "page": page, "per_page": per_page,
                  "employer_id": employer_id}
        response = requests.get(self.__base_url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print("Ошибка при получении данных: ", response.status_code)
            return []

    def get_area_id(self, user_area):
        """Метод получения id населенного пункта"""
        response = requests.get(self.__area_url)
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
