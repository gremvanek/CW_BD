import requests


def get_vacancies_and_companies(employers):
    hh_data_list = []
    employer_ids = employers[0]['id']  # Получаем список идентификаторов компаний из employers
    for employer_id in employer_ids:
        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            hh_data = response.json()['items']
            hh_data_list.extend(hh_data)
        else:
            print(f"Ошибка получения данных по номеру работодателя {employer_id}. "
                  f"Код ошибки: {response.status_code}")
    return hh_data_list
