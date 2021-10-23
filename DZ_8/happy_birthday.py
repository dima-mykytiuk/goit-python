import datetime


def get_birthday_per_week(users):
    # Проходим по списку словарей и дабавляем валидные данные в новый список словарей
    # (Пользователей и дни рождения у которых день рождение в ближайшею неделю).
    delta_days = 1
    while delta_days != 8:
        for item in users:
            valid_days = datetime.datetime.now() + datetime.timedelta(days=delta_days)
            for value in item.values():
                if type(value) != str:
                    if value.month == valid_days.month and value.day == valid_days.day:
                        valid_list.append(item)
        delta_days += 1
    # Проходим по созданному списку словарей с валидными данными
    # Меняем год на текущий чтобы получать точные дни
    # Дабавляем имя именника в список который соответсвует дню когда у него день рождения
    # Если у него день рождение в субботу или воскресенье то добавляем в список "Monday"
    for item in valid_list:
        date = item.get('birthday')
        valid_year = date.replace(year=current_year)
        day = valid_year.strftime("%A")
        full_week.get(day).append(item.get('name'))

    # Проходим по ключам словаря "workdays" берем значение ключа и делаем из него строку.
    # Проверяем длину списка если она не равна 0 то выводим в консоль
    for work_day in work_days.keys():
        list_names = work_days.get(work_day)
        valid_names = ', '.join(list_names)
        if len(list_names) != 0:
            print(f'{work_day}: {valid_names}')


if __name__ == '__main__':
    current_year = datetime.datetime.now().year
    valid_list = []
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    work_days = {
        'Monday': monday,
        'Tuesday': tuesday,
        'Wednesday': wednesday,
        'Thursday': thursday,
        'Friday': friday,
    }
    full_week = {
        'Saturday': monday,
        'Sunday': monday,
        **work_days,
    }

    get_birthday_per_week([{'name': 'Dmytro', 'birthday': datetime.datetime(1998, 10, 17)},
                           {'name': 'Anton', 'birthday': datetime.datetime(1998, 10, 5)},
                           {'name': 'Petya', 'birthday': datetime.datetime(1998, 10, 26)},
                           {'name': 'Alex', 'birthday': datetime.datetime(1998, 11, 30)},
                           {'name': 'Tolya', 'birthday': datetime.datetime(1998, 10, 28)},
                           {'name': 'Vasya', 'birthday': datetime.datetime(1998, 10, 23)},
                           {'name': 'Nick', 'birthday': datetime.datetime(1998, 10, 25)},
                           {'name': 'Nikita', 'birthday': datetime.datetime(1998, 10, 26)},
                           {'name': 'Vitaliy', 'birthday': datetime.datetime(1998, 10, 30)}])
