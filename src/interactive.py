from datetime import datetime
import json
from src.vac_handler import VacancyHandler
from src.vac_getter import VacancyGetterHH, VacancyGetterSJ
from src.user_utils import caps_city, user_input_handler


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
        print("Такого города в списке нет, вакансии будут выданы по всей России\n")
        user_city = None

    print('Если вы хотите получить отсортированный по зарплате список вакансий, введите "sort",')
    print("а если список только самых доходных вакансий, введите их количество,")
    print("если нет, - нажмите ENTER, будет выведен перечень без сортировки по зарплате.")
    sort_input = input()

    user_list = VacancyHandler(VG_HH, VG_SJ).get_vac_list(keyword=user_keyword, city=user_city)

    user_input_handler(user_list, user_source, sort_input)
