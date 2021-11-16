from collections import UserDict
import re
from datetime import datetime


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return self.data


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
        if new_value.isalpha():
            self.__value = new_value
        else:
            print('Invalid items in name')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        new_list = []
        if isinstance(new_value, list):
            try:
                for item in new_value:
                    if len(item) == 12 and item.isdigit():
                        new_list.append(item)
                        # print(f'Number was added successfully: {item}!!!')
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

    @value.setter
    def value(self, new_value):
        try:
            date_numbers = re.findall(r'\d{1,4}', new_value)
            date_format = datetime(int(date_numbers[2]), int(date_numbers[1]), int(date_numbers[0]))
            age = datetime.today().year - date_format.year
            if len(date_numbers) != 3 or age > 100:
                print('Invalid Date')
            else:
                self.__value = datetime(date_format.year, date_format.month, date_format.day).date()
                print(f'Successfully changed date')
        except:
            print("Invalid date for class Birthday!!!")
            self.__value = None


class Record:
    def __init__(self, name, phones=Phone(None), birthday=Birthday(None)):
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.data = AddressBook()  # !!!!!!!!!!!!!!!!
        self.birthday.value = birthday.value
        self.phones.value = phones.value
        self.data['name'] = name
        self.data['phones'] = phones
        self.data['birthday'] = birthday

    def add_phone(self, phones):
        if len(phones) == 12 and phones.isdigit():
            if self.phones.value is None:
                self.phones.value = [phones]
                self.data['phones'] = self.phones
                return f'Number was added successfully: {phones}!!!'
            else:
                self.phones.value.append(phones)
                return f'Number was added successfully: {phones}!!!'
        else:
            return f'Invalid phone format or length, phone must be only digit and 12 numbers!!!'

    def change_phone(self, old_phone, new_phone):
        if len(new_phone) == 12 and new_phone.isdigit():
            self.phones.value.remove(old_phone)
            self.phones.value.append(new_phone)
            self.data.pop('phones')
            self.data['phones'] = self.phones
            return f'Successfully changed phone for user: {self.name.value}!!'
        else:
            print(f'Invalid phone: {new_phone}')

    def delete_phone(self, phone):
        self.phones.value.remove(phone)
        return f'Successfully deleted phone for user: {self.name}!!\n{self.data}'

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
    print(Bill.add_phone('121421214241'))  # Number was added successfully: 121421214241!!!
    print(Bill.phones.value)  # ['521421214241', '121421214241']
    print(Bill.birthday.value)  # 1998-01-01
    print(Bill.change_phone('121421214241', '222222222222'))  # Successfully changed phone for user: Bill!!
    Bill.birthday.value = '17-10-1998'  # Successfully changed date
    print(Bill.birthday.value)  # 1998-10-17
    print(Bill.days_to_birthday())  # Birthday in 335 days!!!
    address = AddressBook()
    add_rec = address.add_record(Bill)
    print(add_rec)  # {'Bill': <__main__.Record object at 0x7f9060086e20>}
    print(Bill.data)  # {'name': <__main__.Name object at 0x7fd1f80b6f10>, 'birthday': <__main__.Birthday object at 0x7fd1f80b6d90>, 'phones': <__main__.Phone object at 0x7fd1f80b6e50>}
    Petya = Record(name=Name('Petya'), phones=Phone('111111111111'), birthday=Birthday('1-1-1997'))
    add_rec = address.add_record(Petya)
    print(add_rec)  # {'Bill': <__main__.Record object at 0x7fc2980b69d0>, 'Petya': <__main__.Record object at 0x7fc2980ab2b0>}