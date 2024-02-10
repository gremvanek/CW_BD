from database.utils import create_database, create_tables, insert_data
# def main():
#     # Создаем базу данных и таблицу
#     create_database('cw_db')
#     create_tables()
#     insert_data()
from database.db_manager import DBManager


def display_menu():
    print("Добро пожаловать в программу управления базой данных!")
    print("Выберите один из вариантов:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий с зарплатой выше средней")
    print("5. Получить список всех вакансий по ключевому слову")
    print("6. Завершить программу")


def main():
    db_manager = DBManager()  # Инициализируем объект DBManager

    while True:
        display_menu()
        # Создаем базу данных и таблицу
        create_database('cw_db')
        create_tables()
        insert_data()
        choice = input("Введите номер выбранного действия: ")

        if choice == '1':
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for company, vacancy_count in companies_and_vacancies:
                print(f"{company}: {vacancy_count} вакансий")
        elif choice == '2':
            all_vacancies = db_manager.get_all_vacancies()
            print("Список всех вакансий:")
            for vacancy in all_vacancies:
                print(f"Компания: {vacancy[2]}, Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}")
        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary[0][0]}")
        elif choice == '4':
            vacancies_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список вакансий с зарплатой выше средней:")
            for vacancy in vacancies_higher_salary:
                print(vacancy[0])
        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Список вакансий с ключевым словом '{keyword}':")
            for vacancy in vacancies_with_keyword:
                if vacancy in vacancies_with_keyword:
                    print(vacancy[0])
                else:
                    pass
        elif choice == '6':
            print("Завершение работы программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите номер от 1 до 6.")


if __name__ == "__main__":
    main()
#commits