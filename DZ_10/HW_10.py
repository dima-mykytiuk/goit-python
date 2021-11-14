from collections import UserDict


class Record:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.data = AddressBook()

    def add_user(self):
        self.data[self.name] = self.name
        self.data[self.phone] = int(self.phone)
        return f'Successfully added user phone: {self.name}!!\n{self.data}'

    def change_user(self, name, phone):
        if name not in self.data.keys():
            return self.data[self.name]
        else:
            self.data.pop(self.phone)
            self.phone = phone
            self.data[self.phone] = int(phone)
            return f'Successfully changed phone for user: {self.name}\n{self.data}!!'

    def delete_user(self):
        self.data.pop(self.name)
        self.data.pop(self.phone)
        return f'Successfully deleted user with name: {self.name} and phone: {self.phone}\n{self.data}'


class AddressBook(UserDict):
    pass


class Field:
    pass


class Name:
    pass


class Phone:
    pass


if __name__ == '__main__':
    Bill = Record('Bill', 421312)
    print(Bill.add_user())  # Successfully added user phone: Bill!!
    print(Bill.change_user('Bill', 1234))  # Successfully changed phone for user: Bill
    Petya = Record('Petya', 102)
    print(Petya.add_user())  # Successfully added user phone: Petya!!
    print(Petya.change_user('Petya', 1012))  # Successfully changed phone for user: Petya
    print(Petya.delete_user())  # Successfully deleted user with name: Petya and phone: 1012
    print(Bill.name)  # Bill
    print(Bill.phone)  # 1234
    print(Bill.data)  # {'Bill': 'Bill', 1234: 1234}
