import psycopg2


class DBManager:
    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(database='cw_db', user='postgres', password='050305', host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT employer_name, COUNT(vacancy_id) FROM '
                    'vacancies JOIN employers ON vacancies.employer_id = employers.employer_id GROUP BY employer_name')
                answer = cur.fetchall()
        return answer

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий"""
        with psycopg2.connect(database='cw_db', user='postgres', password='050305', host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT vacancies.vacancy_name, vacancies.salary, employers.employer_name FROM '
                    'vacancies JOIN employers ON vacancies.employer_id = employers.employer_id')
                answer = cur.fetchall()
        return answer

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(database='cw_db', user='postgres', password='050305', host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT avg(salary) FROM vacancies')
                answer = cur.fetchall()
        return answer

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(database='cw_db', user='postgres', password='050305', host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name FROM '
                            'vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)')
                answer = cur.fetchall()
        return answer

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with psycopg2.connect(database='cw_db', user='postgres', password='050305', host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT vacancy_name FROM vacancies WHERE LOWER(vacancy_name) LIKE LOWER(%s)",
                            ('%' + keyword + '%',))
                answer = cur.fetchall()
        return answer
