from typing import Any
import requests
from src.vac_getter import VacancyGetterHH, VacancyGetterSJ


def get_currency_rate(currency: str) -> float:
    """
    Функция принимает наименование валюты для получения курса по API и возвращает ее курс к рублю.
    :param currency:
    :return currency_rate:
    """
    url_cur = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url_cur)
    if response.status_code == 200:
        data = response.json()
        return data["Valute"][currency.upper()]["Value"] / data["Valute"][currency.upper()]["Nominal"]
    if currency.upper() == "USD":
        return 90
    elif currency.upper() == "EUR":
        return 100
    else:
        return 1


def normalize_salary(salary_from: Any, salary_to: Any, currency: float) -> int:
    """
    Функция принимает на вход данные по зарплате, полученные с сайта и возвращает значение зарплаты, в общем формате,
    приемлемом для сравнения.
    :param salary_from:
    :param salary_to:
    :param currency:
    :return salary_norm:
    """

    if not salary_from:
        salary_from = 0
    if not salary_to:
        salary_to = salary_from
    if currency == "RUR" or currency == "rub":
        salary_norm = max(salary_from, salary_to)
    else:
        salary_norm = int(max(salary_from, salary_to) * get_currency_rate(currency))

    return salary_norm


class VacancyHandler:
    """
    Класс преобразует полученные классами VacancyGetterHH и VacancyGetterSJ вакансии в общий список
    по заданным параметрам.
    """

    def __init__(self, a: VacancyGetterHH, b: VacancyGetterSJ):
        self.a = a
        self.b = b

    def get_vac_list(self, keyword=None, city=None):
        """
        Функция принимает экземпляры классов VacancyGetterHH и VacancyGetterSJ,
        возвращает отсортированный по убыванию зарплаты список вакансий.
        :param keyword:
        :param city:
        :return vacancy_list:
        """
        vacs_hh = self.a.get_vacancy(keyword, city)
        vacs_hh = [vc for vc in vacs_hh["items"] if vc["salary"]]
        vacs_sj = self.b.get_vacancy(keyword, city)["objects"]

        vac_list = []

        for vac in vacs_hh:
            vac_list.append(
                {
                    "source": "hh.ru",
                    "vacancy_id": vac["id"],
                    "vacancy_title": vac["name"],
                    "vacancy_loc": vac["area"]["name"],
                    "salary_from": vac["salary"]["from"],
                    "salary_to": vac["salary"]["to"],
                    "salary_currency": vac["salary"]["currency"],
                    "salary_r": normalize_salary(vac["salary"]["from"], vac["salary"]["to"], vac["salary"]["currency"]),
                    "company": vac["employer"]["name"],
                    "vacancy_url": vac["alternate_url"],
                }
            )

        for vac in vacs_sj:
            vac_list.append(
                {
                    "source": "superjob.ru",
                    "vacancy_id": vac["id"],
                    "vacancy_title": vac["profession"],
                    "vacancy_loc": vac["town"]["title"],
                    "salary_from": vac["payment_from"],
                    "salary_to": vac["payment_to"],
                    "salary_currency": vac["currency"],
                    "salary_r": normalize_salary(vac["payment_from"], vac["payment_to"], vac["currency"]),
                    "company": vac["firm_name"],
                    "vacancy_url": vac["link"],
                }
            )

        return vac_list
