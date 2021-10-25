import datetime


def get_birthday_per_week(users):
    # We go through the list of dictionaries and add valid data to the new list of dictionaries
    # (Users and dates of birth who have a birthday in the next week).
    delta_days = 1
    while delta_days != 8:
        for item in users:
            valid_days = datetime.datetime.now() + datetime.timedelta(days=delta_days)
            for value in item.values():
                if type(value) != str:
                    if value.month == valid_days.month and value.day == valid_days.day:
                        valid_list.append(item)
        delta_days += 1
    # We go through the created list of dictionaries with valid data
    # Change the year to the current one to get correct days
    # Add the name of the birthday person to the list that corresponds to the day when his birthday
    # If his birthday is on Saturday or Sunday, then add to the list "Monday"
    for item in valid_list:
        date = item.get('birthday')
        valid_year = date.replace(year=current_year)
        day = valid_year.strftime("%A")
        full_week.get(day).append(item.get('name'))

    # We go through the keys of the "workdays" dictionary, take the key value and make a string from it
    # Check the length of the list if it is not equal to 0 then output to the console
    for work_day in work_days.keys():
        list_names = work_days.get(work_day)
        valid_names = ', '.join(list_names)
        if len(list_names) != 0:
            print(f'{work_day}: {valid_names}')


if __name__ == '__main__':
    current_year = datetime.datetime.now().year
    valid_list = []

    work_days = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
    }
    full_week = {
        'Saturday': work_days.get('Monday'),
        'Sunday': work_days.get('Monday'),
        **work_days,
    }

    get_birthday_per_week([{'name': 'Dmytro', 'birthday': datetime.datetime(1998, 10, 17)},
                           {'name': 'Anton', 'birthday': datetime.datetime(1998, 10, 5)},
                           {'name': 'Petya', 'birthday': datetime.datetime(1998, 10, 26)},
                           {'name': 'Alex', 'birthday': datetime.datetime(1998, 11, 30)},
                           {'name': 'Tolya', 'birthday': datetime.datetime(1998, 10, 28)},
                           {'name': 'Vasya', 'birthday': datetime.datetime(1998, 10, 23)},
                           {'name': 'Nick', 'birthday': datetime.datetime(1998, 10, 26)},
                           {'name': 'Nikita', 'birthday': datetime.datetime(1998, 10, 31)},
                           {'name': 'Vitaliy', 'birthday': datetime.datetime(1998, 10, 30)}])
