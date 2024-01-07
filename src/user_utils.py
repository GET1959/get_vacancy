from typing import Any

from src.vac_handler import VacancyHandler, get_hh_vacs, get_sj_vacs, sort_by_salary
from src.vac_writer import VacancyJsonFileManager

def caps_city(text: str) -> str:
    """
    Функция принимает название российского города и возвращает его отформатированным
    в соответствии со списком городов CITY_LIST.
    :param text:
    :return city_name:
    """
    if "-" in text:
        city_name = "-".join(word.capitalize() if word.lower() != "на" else word.lower() for word in text.split("-"))
    else:
        city_name = " ".join(word.capitalize() for word in text.split(" "))
    return city_name


def user_json_writer(lst: VacancyHandler, dir_name, file_name) -> None:
    """
    Функция принимает список вакансий, название директории и имя файла для записи данных,
    записывает в json-файл данные, полученные по запросу пользователя.
    :param lst:
    :param dir_name:
    :param file_name:
    :return None:
    """
    js_writer = VacancyJsonFileManager(lst)
    js_writer.write_vacancy(dir_name, file_name)
    return None


def user_input_sorter(lst: list[dict], us_input: Any) -> None:
    """
    Функция принимает на вход список вакансий и пользовательские условия его обработки,
    если условие 'sort': выводятся отсортированные по зарплате вакансии,
    если условие - это число: выводятся вакансии с наибольшими зарплатами в количестве,
    соответствующем введенному числу. Полученные данные записываются в json-файл.
    :param lst:
    :param us_input:
    :return None:
    """
    if us_input == "sort":
        user_json_writer(sort_by_salary(lst), "../user_vacancies/", "user_vac_list.json")
        a = len(sort_by_salary(lst))
        for vac in sort_by_salary(lst):
            print(vac)
        print(
            f"По вашему запросу получено {a} {'вакансия' * (str(a)[-1] == '1' and a % 100 != 11)}"
            f"{'вакансии' * (str(a)[-1] in ['2', '3', '4'] and a % 100 not in [11, 12, 13, 14])}"
            f"{'вакансий' * (str(a)[-1] in ['0', '5', '6', '7', '8', '9'] or a % 100 in [11, 12, 13, 14])}"
        )
    elif us_input.isdigit():
        n = int(us_input)
        user_json_writer(sort_by_salary(lst)[:n], "../user_vacancies/", "user_vac_list.json")
        for vac in sort_by_salary(lst)[:n]:
            print(vac)
        print(
            f"По вашему запросу получено {n} {'вакансия' * (str(n)[-1] == '1' and n % 100 != 11)}"
            f"{'вакансии' * (str(n)[-1] in ['2', '3', '4'] and n % 100 not in [11, 12, 13, 14])}"
            f"{'вакансий' * (str(n)[-1] in ['0', '5', '6', '7', '8', '9'] or n % 100 in [11, 12, 13, 14])}"
        )
    else:
        user_json_writer(lst, "../user_vacancies/", "user_vac_list.json")
        b = len(lst)
        for vac in lst:
            print(vac)
        print(
            f"По вашему запросу получено {b} {'вакансия' * (str(b)[-1] == '1' and b % 100 != 11)}"
            f"{'вакансии' * (str(b)[-1] in ['2', '3', '4'] and b % 100 not in [11, 12, 13, 14])}"
            f"{'вакансий' * (str(b)[-1] in ['0', '5', '6', '7', '8', '9'] or b % 100 in [11, 12, 13, 14])}"
        )


def user_input_handler(lst: list[dict], us_source: str, us_input: Any) -> None:
    """
    Функция принимает список словарей и пользовательский ввод.
    На основании пользовательского ввода выбирает ресурс, из которого
    формируется список вакансий.
    :param lst:
    :param us_source:
    :param us_input:
    :return None:
    """
    if us_source not in ["hh", "sj"]:
        user_input_sorter(lst, us_input)
    elif us_source == "hh":
        user_input_sorter(get_hh_vacs(lst), us_input)
    elif us_source == "sj":
        user_input_sorter(get_sj_vacs(lst), us_input)
