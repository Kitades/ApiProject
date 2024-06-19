from pathlib import Path

from prettytable import PrettyTable

from file_connector import JSONConnector
from file_connector.base import FileConnector
from src.api_clients import HeadHunterAPI
from src.api_clients.base import VacancyApiClient

BASE_PATH = Path(__file__).parent
VACANCIES_PATH_FILE = BASE_PATH.joinpath('vacancies.json')

api_client: VacancyApiClient = HeadHunterAPI()
json_connector: FileConnector = JSONConnector(VACANCIES_PATH_FILE)

welcome_massage = """
        Выберите дествия
1. Загрузить ваканисии в файл по ключевому слову
2. Вывести топ 10 вакансий из файла
0. Выйти
"""




def one_func():
    search_word = input('Ключевое слово для поиска: ')
    vacancies = api_client.get_vacancies(search_word.lower())
    for vac in vacancies:
        json_connector.add_vacancy(vac)


def two_func():
    vacancies = json_connector.get_vacancies()
    t = PrettyTable(['name', 'url', 'employer', 'salary'])

    for vac in sorted(vacancies, key=lambda x: x.salary, reverse=True)[:10]:
        salary = '{_from} -> {_to} -> {currency}'.format(
                _from=vac.salary.salary_from or None,
                _to=vac.salary.salary_to or None,
                currency=vac.salary.currency,
        )
        t.add_row([vac.name, vac.url, vac.employer_name, salary])

    print(t)


MAPPING = {
    '1': one_func, '2': two_func,
}


def main():
    while True:
        print(welcome_massage)
        user_input = input()
        if not user_input.isdigit():
            continue
        if user_input in MAPPING:
            callback = MAPPING[user_input]
            callback()
        elif user_input == '0':
            break


if __name__ == '__main__':
    main()
