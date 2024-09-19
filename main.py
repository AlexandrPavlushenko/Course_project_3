import requests

from src.head_hunter_api import HHVacancyAPI
from src.database_create import DataBaseCreate

hh_api = HHVacancyAPI()

vacances = hh_api.get_data(area_id='1')
print(len(vacances))
for i in vacances:
    print(i['employer']['name'])
