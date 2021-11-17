from collections import UserDict
import re
from datetime import datetime


class AddressBook(UserDict):
    # Добавляем элементы в словарь если получим список или если получим только 1 элемент
    def add_record(self, record):
        if isinstance(record, list):
            for item in record:
                self.data[item.name.value] = item
        else:
            self.data[record.name.value] = record
        return self.data
    # Итерируемся по данным в словаре данных и добавляем в строку данные этого пользователя для последующего вывода
    # Если в итератор заходит число N которое больше чем длина словаря то возвращаем ошибку.

    def iterator(self, N):
        new = iter(self.data.values())
        if len(self.data.values()) < N:
            return f'I dont have {N} contacts in my AddressBook!!'
        res = ''
        num = 0
        while num < N:
            next_it = next(new)
            res += f'Name: {next_it.name.value}, Phones: {next_it.phones.value}, Birthday: {next_it.birthday.value}\n'
            num += 1
        return res


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    @property
    def value(self):
        return self.__value

    # Создаем новый список для наполнения его телефонами пользователя, если пользователь ввел несколько мобильных
    # телефонов в списке тогда мы распаковываем этот список и пороверяем проходит ли проверку этот телефон если да то
    # добавляем его в список, если список не был наполнен то задаем значинию мфдгу None если все норм тогда присваеваем
    # value этот список, если пользователь просто ввел 1 телефон строкой тогда мы проверяем на корректность этот телефон
    # и если все норма то присваиваем value этот телефон если что-то не так то присваиваем value None.
    @value.setter
    def value(self, new_value):
        new_list = []
        if isinstance(new_value, list):
            try:
                for item in new_value:
                    if len(item) == 12 and item.isdigit():
                        new_list.append(item)
                        print(f'Number was added successfully: {item}!!!')
                    else:
                        print(f'Invalid number: {item} for class Phone!!!')
                if len(new_list) != 0:
                    self.__value = new_list
                else:
                    self.__value = None
            except:
                print('Invalid phone format or length, phone must be only digit and 12 numbers!!!')
                self.__value = None
        elif isinstance(new_value, str):
            if len(new_value) == 12 and new_value.isdigit():
                self.__value = [new_value]
                print(f'Number was added successfully: {new_value}!!!')
            else:
                self.__value = None
                print(f'Invalid number: {new_value} for class Phone!!!')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    @property
    def value(self):
        return self.__value
    # Ищем в строке числа с помощью регулярки если получаем список с 3 значениями делаем datetime обьект
    # получаем возраст пользователя и если все проходит проверку то присваиваем значению value наш datetime обьект
    # Если пользователь вводит не корректную дату или дату где получается что ему больше 100 лет тогда выдаем ошибку и
    # присваиваем value None
    @value.setter
    def value(self, new_value):
        try:
            date_numbers = re.findall(r'\d{1,4}', new_value)
            date_format = datetime(int(date_numbers[2]), int(date_numbers[1]), int(date_numbers[0]))
            age = datetime.today().year - date_format.year
            if len(date_numbers) != 3 or age > 100:
                print('Invalid date for class Birthday!!!')
                self.__value = None
            else:
                self.__value = datetime(date_format.year, date_format.month, date_format.day).date()
                print(f'Successfully set date')
        except:
            print("Invalid date for class Birthday!!!")
            self.__value = None


class Record:
    # Здесь я добавил слишком много в init не знаю или так можно. Сделал это для того чтобы сразу value
    # присваивать значения которые заходят в класс и была проверка на то что ввел пользователь
    # чтобы пользователь если вводил не корректные значения чтобы использовались setter определенных классов
    def __init__(self, name, phones=Phone(None), birthday=Birthday(None)):
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.data = AddressBook()  # !!!!!!!!!!!!!!!!
        self.birthday.value = birthday.value
        self.phones.value = phones.value

    # Делаем проверку введенного пользователем телефона если все нормально то проверяем были ли у нас раньше какие-то
    # данные в телефонной книге если были то мы просто добавляем к списку телефон который вошел в функцию
    # если у нас до этого value было None то мы присваиваем value наш телефон.
    # если телефон не прошел проверку выводим пользователю ошибку
    def add_phone(self, phones):
        if len(phones) == 12 and phones.isdigit():
            if self.phones.value is None:
                self.phones.value = [phones]
                return f'Number was added successfully: {phones}!!!'
            else:
                self.phones.value.append(phones)
                return f'Number was added successfully: {phones}!!!'
        else:
            return f'Invalid phone format or length, phone must be only digit and 12 numbers!!!'

    # Проверяем есть ли у нас в данных телефон который надо изменить если есть то проверяем новый телефон на корректность
    # Если все проверки прошли успешно тогда удаляем старый телефон и добавляем новый если что-то не так то возвращаем пользователю ошибку
    # если старого номера нету в данных AddressBook то возвращаем пользователю ошибку
    def change_phone(self, old_phone, new_phone):
        if old_phone in self.phones.value:
            if len(new_phone) == 12 and new_phone.isdigit():
                self.phones.value.remove(old_phone)
                self.phones.value.append(new_phone)
                return f'Successfully changed phone for user: {self.name.value}!!'
            else:
                print(f'Invalid phone: {new_phone}')
        else:
            return 'Error i dont have such phone in my AddressBook!!'

    # Удаляем телефон который ввел пользователь если он есть в данных AddressBook
    def delete_phone(self, phone):
        if phone in self.phones.value:
            self.phones.value.remove(phone)
            return f'Successfully deleted phone for user: {self.name.value}!!\n{self.data}'
        else:
            return 'Error i dont have such phone in my AddressBook!!'

    # Рассчитываем сколько дней до дня рождения контакта в AddressBook. Меняем год на текущий чтобы получать правильные
    # значения проверяем прошло ли уже день рождение у нашего пользователя или нет и возвращаем количество дней до ДР
    def days_to_birthday(self):
        valid_year = self.birthday.value.replace(year=datetime.now().year)
        if valid_year.month < datetime.now().month:
            valid = valid_year - datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {valid.days} days!!!'
        else:
            valid = valid_year - datetime(datetime.now().year, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {valid.days} days!!!'


if __name__ == '__main__':
    Bill = Record(name=Name('Bill'), phones=Phone('43'), birthday=Birthday('1-1-1998'))  # Invalid number: 43 for class Phone!!!
    print(Bill.phones.value)  # None
    print(Bill.add_phone('521421214241'))  # Number was added successfully: 521421214241!!!
    print(Bill.add_phone('121421214241'))  # Number was added successfully: 521421214241!!!
    print(Bill.phones.value)  # ['521421214241']
    print(Bill.birthday.value)  # 1998-01-01
    print(Bill.change_phone('121421214241', '222222222222'))  # Successfully changed phone for user: Bill!!
    Bill.birthday.value = '17-10-1998'  # Successfully set date
    print(Bill.birthday.value)  # 1998-10-17
    print(Bill.days_to_birthday())  # Birthday in 335 days!!!
    address = AddressBook()
    Petya = Record(name=Name('Petya'), phones=Phone('111111111111'), birthday=Birthday('1-1-1997'))
    Zhenya = Record(name=Name('Zhenya'), phones=Phone('222222222222'), birthday=Birthday('2-1-1897'))  # Invalid date for class Birthday!!!
    Dima = Record(name=Name('Dima'), phones=Phone('333333333333'), birthday=Birthday('3-1-1997'))
    Vasya = Record(name=Name('Vasya'), phones=Phone('444444444444'), birthday=Birthday('4-1-1997'))
    Anton = Record(name=Name('Anton'), phones=Phone('555555555555'), birthday=Birthday('5-1-1997'))
    Zheka = Record(name=Name('Zheka'), phones=Phone('555555555555'), birthday=Birthday('5-1-1997'))
    add_rec = address.add_record([Bill, Petya, Zhenya, Dima, Vasya, Anton])
    address.add_record(Zheka)
    print(add_rec)  # {'Bill': <__main__.Record object at 0x7fea58027ac0>, 'Petya': <__main__.Record object at 0x7fea5801c250>, 'Zhenya': <__main__.Record object at 0x7fea5801c4f0>, 'Dima': <__main__.Record object at 0x7fea5801d9a0>, 'Vasya': <__main__.Record object at 0x7fea5801dd00>, 'Anton': <__main__.Record object at 0x7fea58023040>, 'Zheka': <__main__.Record object at 0x7fea580232b0>}
    print(address.iterator(2))  # Name: Bill, Phones: ['521421214241', '222222222222'], Birthday: 1998-10-17 Name: Petya, Phones: ['111111111111'], Birthday: 1997-01-01
    print(address.iterator(7))  # Name: Bill, Phones: ['521421214241', '222222222222'], Birthday: 1998-10-17 Name: Petya, Phones: ['111111111111'], Birthday: 1997-01-01 Name: Zhenya, Phones: ['222222222222'], Birthday: 2-1-1897 Name: Dima, Phones: ['333333333333'], Birthday: 1997-01-03 Name: Vasya, Phones: ['444444444444'], Birthday: 1997-01-04 Name: Anton, Phones: ['555555555555'], Birthday: 1997-01-05 Name: Zheka, Phones: ['555555555555'], Birthday: 1997-01-05
    print(address.iterator(8))  # I dont have 8 contacts in my AddressBook!!