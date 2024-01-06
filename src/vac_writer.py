from abc import ABC, abstractmethod
import json
import os

from src.vac_handler import VacancyHandler


class VacancyFileManager(ABC):
    """
    Абстрактный класс, определяющий необходимые методы для записи в json-файл для классов-наследников,
    для чтения json-файлов, для удаления записей из json-файлов.
    """

    @abstractmethod
    def write_vacancy(self):
        pass

    @abstractmethod
    def read_vacancy(self):
        pass

    @abstractmethod
    def del_vacancy(self):
        pass


class VacancyJsonFileManager(VacancyFileManager):
    """
    Класс - наследник от VacancyFileManager определяет методы для работы с json-файлами.
    """

    def __init__(self, vac_list: VacancyHandler) -> None:
        self.vac_list = vac_list

    def write_vacancy(self, dir_name: str, file_name: str) -> None:
        """
        Метод для записи в json-файл данных экземпляра класса VacancyHandler.
        Кроме экземпляра класса VacancyHandler принимает на вход название директории
        и имя файла для записи.
        :param dir_name:
        :param file_name:
        :return None:
        """
        os.makedirs(dir_name, exist_ok=True)
        file_path = dir_name + file_name
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.vac_list, file, ensure_ascii=False, indent=2)
        return None

    def read_vacancy(self, file_path: str) -> list[dict]:
        """
        Метод для чтения json-файла, принимает на вход путь к файлу
        и возвращает список словарей данных по вакансиям.
        :param file_path:
        :return vac_list:
        """
        with open(file_path, "r", encoding="utf-8") as file:
            vac_list = json.load(file)
        return vac_list

    def del_vacancy(self, file_path: str, vac_id: str):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for dct in data:
            if dct["vacancy_id"] == vac_id:
                data.remove(dct)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return None
