Проект get_vacancy состоит из пяти рабочих модулей и файла main.py, запускающего программу.
Модуль vac_getter содержит классы и методы, позволяющие по запросу получить список вакансий с
сайтов hh.ru и superjob.ru.
Модуль vac_handler позволяет из полученных данных извлечь ключевые характеристики каждой
вакансии: id, название, город, данные по зарплате, название компании, url и ресурс, с которого
она получена, и сформировать из них общий список вакансий.
Модуль vac_writer отвечает за работу с файлами: запись в файл, чтение файла, удаление записей из файла.
Модуль user_utils содержит функции, обрабатывающие пользовательский ввод и формирующие в соответствии
с ним список вакансий.
Модуль interactive непосредственно взаимодействует с пользователем и получает от него аргументы для
формирования списка вакансий.
При запуске файла main.py пользователю предлагается ввести свои требования по выбору вакансий,
в консоли формируется ответ пользователю. Одновременно этот ответ записывается в файл user_vac_list.json
в директории user_vacancies.