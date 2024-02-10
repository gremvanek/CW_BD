import psycopg2 as pq
from database.hh_vacansies import get_vacancies_and_companies


def create_database(database_name):
    """Создание базы данных."""
    conn = pq.connect(user='postgres', password='050305', host='localhost')
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    except pq.errors.InvalidCatalogName:
        print('База данных не существует')

    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_tables():
    """Создание таблиц в созданной базе данных."""
    conn = pq.connect(database='cw_db', user='postgres', password='050305', host='localhost')
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(255) UNIQUE
         )
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name TEXT NOT NULL,
                salary INT,
                employer_id INT REFERENCES employers(employer_id)
            )
            """)
    conn.commit()
    conn.close()


def insert_data():
    """Заполнение таблиц данными."""
    conn = pq.connect(database='cw_db', user='postgres', password='050305', host='localhost')
    with conn.cursor() as cur:
        # Получаем данные о компаниях и вакансиях
        employers = [{'id': ['3127', '3776', '4934', '3529', '4181', '78638', '54979', '816144', '1601', '3093544']}]
        hh_data = get_vacancies_and_companies(employers)

        # Вставка данных о компаниях и их вакансиях
        for item in hh_data:
            employer_id = item['employer']['id']
            employer_name = item['employer']['name']
            vacancy_name = item['name']
            salary_from = item['salary']['from'] if item['salary'] is not None else 0
            salary_to = item['salary']['to'] if item['salary'] is not None else 0
            if salary_from is not None and salary_to is not None:
                salary = (salary_from + salary_to) / 2
            elif salary_from is not None:
                salary = salary_from
            elif salary_to is not None:
                salary = salary_to
            else:
                salary = None

            # Вставляем данные о компании, если ее еще нет в таблице
            cur.execute("INSERT INTO employers (employer_id, employer_name) "
                        "VALUES (%s, %s) ON CONFLICT (employer_id) DO NOTHING",
                        (employer_id, employer_name))

            # Вставляем данные о вакансии
            cur.execute("INSERT INTO vacancies (vacancy_name, salary, employer_id) VALUES (%s, %s, %s)",
                        (vacancy_name, salary, employer_id))
    conn.commit()
    conn.close()
