from collections import UserDict


class Record:
    def __init__(self, name, phones=''):
        self.name = name
        self.phones = list(phones)
        self.data = AddressBook()  # !!!!!!!!!!!!!!!!

    def add_phone(self, name, phones):
        self.phones.append(phones)
        self.data[self.name] = name
        self.data['phones'] = self.phones
        return f'Successfully added phone for user: {self.name}!!\n{self.data}'

    def change_phone(self, old_phone, new_phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)
        self.data.pop('phones')
        self.data['phones'] = self.phones
        return f'Successfully changed phone for user: {self.name}!!\n{self.data}'

    def delete_phone(self, phone):
        self.phones.remove(phone)
        return f'Successfully deleted phone for user: {self.name}!!\n{self.data}'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


if __name__ == '__main__':
    Bill = Record('Bill')
    print(Bill.add_phone('Bill', 123))  # Successfully added phone for user: Bill!!
    print(Bill.add_phone('Bill', 521))  # Successfully added phone for user: Bill!!
    print(Bill.change_phone(521, 1234))  # Successfully changed phone for user: Bill!!
    Petya = Record('Petya')
    print(Petya.add_phone('Petya', 102))  # Successfully added phone for user: Petya!!
    print(Petya.change_phone(102, 1012))  # Successfully changed phone for user: Petya!!
    print(Petya.delete_phone(1012))  # Successfully deleted phone for user: Petya!!
    print(Bill.name)  # Bill
    print(Bill.phones)  # [123, 1234]
    print(Bill.data)  # {'Bill': 'Bill', 'phones': [123, 1234]}
