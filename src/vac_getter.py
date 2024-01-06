from abc import ABC, abstractmethod
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

with open("city.json", "r", encoding="utf-8") as file:
    CITY_DICT = json.load(file)
    CITY_LIST = list(CITY_DICT.keys())


class VacancyGetter(ABC):
    """
    Абстрактный класс, определяющий необходимый метод для классов-наследников.
    """

    @abstractmethod
    def get_vacancy(self):
        pass


class VacancyGetterHH(VacancyGetter):
    """
    Класс для получения списка вакансий с hh.ru.
    """

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv;47.0) Gecko/20100101 Firefox/47.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def get_vacancy(self, keyword=None, city=None):
        """
        Метод для получения вакансий с сайта hh.ru
        возвращает словарь с полученными вакансиями в формате сайта вакансий.
        :return vacancy_dict:
        """
        try:
            if keyword:
                if city in CITY_LIST:
                    response = requests.get(
                        self.url,
                        {"area": CITY_DICT[city], "page": 1, "per_page": 100, "text": f"NAME:{keyword}"},
                        headers=self.headers,
                    )
                elif city not in CITY_LIST:
                    response = requests.get(
                        self.url,
                        {"area": 113, "page": 1, "per_page": 100, "text": f"NAME:{keyword}"},
                        headers=self.headers,
                    )
                else:
                    response = requests.get(
                        self.url,
                        {"area": 113, "page": 1, "per_page": 100, "text": f"NAME:{keyword}"},
                        headers=self.headers,
                    )
            else:
                if city:
                    response = requests.get(
                        self.url, {"area": CITY_DICT[city], "page": 1, "per_page": 100}, headers=self.headers
                    )
                else:
                    response = requests.get(self.url, {"area": 113, "page": 1, "per_page": 100}, headers=self.headers)
            # print(response.request.url)
            return response.json()
        except ConnectionError:
            print("Connection error!")
        except requests.HTTPError:
            print("HTTP error")
        except TimeoutError:
            print("Timeout error")
        return {}


class VacancyGetterSJ(VacancyGetter):
    """
    Класс для получения списка вакансий с superjob.ru.
    """

    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/vacancies/?no_agreement=true&count=100"
        self.headers = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}

    def get_vacancy(self, keyword=None, city=None):
        """
        Метод для получения вакансий с сайта superjob.ru
        возвращает словарь с полученными вакансиями в формате сайта вакансий.
        :return vacancy_dict:
        """
        try:
            if keyword:
                if city in CITY_LIST:
                    self.url += f"&town={city}&keyword={keyword}"
                elif city not in CITY_LIST:
                    self.url += f"&keyword={keyword}"
                else:
                    self.url += f"&keyword={keyword}"
            else:
                if city:
                    self.url += f"&town={city}"

            response = requests.get(self.url, headers=self.headers)
            # print(response.request.url)
            return response.json()
        except ConnectionError:
            print("Connection error!")
        except requests.HTTPError:
            print("HTTP error")
        except TimeoutError:
            print("Timeout error")
        return {}
