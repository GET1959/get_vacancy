from datetime import datetime
import json
from typing import Any

from src.vac_handler import VacancyHandler, get_hh_vacs, get_sj_vacs, sort_by_salary
from src.vac_getter import VacancyGetterHH, VacancyGetterSJ
from src.vac_writer import VacancyJsonFileManager


GREETING = (
    "Доброе утро!" * (4 <= datetime.now().hour < 11)
    + "Добрый день!" * (11 <= datetime.now().hour < 16)
    + "Добрый вечер!" * (16 <= datetime.now().hour < 23)
    + "Доброй ночи!" * (datetime.now().hour == 23)
    + "Доброй ночи!" * (0 <= datetime.now().hour < 4)
)

with open("city.json", "r", encoding="utf-8") as file:
    CITY_LIST = list(json.load(file).keys())

VG_HH = VacancyGetterHH()
VG_SJ = VacancyGetterSJ()


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


def user_input_handler(lst: list[dict], us_input: Any) -> None:
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
        for vac in sort_by_salary(lst):
            print(vac)
    elif us_input.isdigit():
        n = int(us_input)
        user_json_writer(sort_by_salary(lst)[:n], "../user_vacancies/", "user_vac_list.json")
        for vac in sort_by_salary(lst)[:n]:
            print(vac)
    else:
        user_json_writer(lst, "../user_vacancies/", "user_vac_list.json")
        for vac in lst:
            print(vac)


def user_func() -> None:
    """
    Функция выводит вакансии на основании пользовательского ввода.
    :return None:
    """
    print(GREETING)
    print("В этом приложении вы можете получить список актуальных вакансий с сайтов hh.ru и superjob.ru.")

    print("Если вы хотите получить вакансии с сайта hh.ru, введите hh,")
    print("если с сайта superjob.ru - введите sj.")
    print("Для получения вакансий с обоих сайтов нажмите ENTER")
    user_source = input()
    if user_source not in ["hh", "sj", ""]:
        print("Такого ресурса нет, вакансии будут выданы с сайтов hh.ru и superjob.ru\n")

    print("Введите ключевое слово, которое должно присутствовать в тексте вакансии.")
    print("Если ключевого слова нет, нажмите ENTER")
    kw_input = input()
    if kw_input == "":
        user_keyword = None
    else:
        user_keyword = kw_input

    print("Введите название города, в котором вы хотите найти вакансии (например, Нижний Новгород).")
    print("Если вы ищете вакансии по всей России, нажмите ENTER")
    city_input = input()
    if caps_city(city_input) in CITY_LIST:
        user_city = caps_city(city_input)
        print(user_city)
    elif city_input == "":
        user_city = None
    else:
        print("Такого города в списке нет, вакансии будут выданы по всей России")
        user_city = None

    print('Если вы хотите получить отсортированный по зарплате список вакансий, введите "sort",')
    print("а если список только самых доходных вакансий, введите их количество,")
    print("если нет, - нажмите ENTER, будет выведен перечень без сортировки.")
    sort_input = input()

    user_list = VacancyHandler(VG_HH, VG_SJ).get_vac_list(keyword=user_keyword, city=user_city)

    if user_source not in ["hh", "sj"]:
        user_input_handler(user_list, sort_input)
    elif user_source == "hh":
        user_input_handler(get_hh_vacs(user_list), sort_input)
    elif user_source == "sj":
        user_input_handler(get_sj_vacs(user_list), sort_input)
