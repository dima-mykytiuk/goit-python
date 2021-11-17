from collections import UserDict
import re
from datetime import datetime


class AddressBook(UserDict):
    # Add items to the dictionary if we get a list or if we get only 1 item
    def add_record(self, record):
        if isinstance(record, list):
            for value in record:
                self.data[value.name.value] = value
        else:
            self.data[record.name.value] = record
        return self.data

    # Iterate over the data in the data dictionary and add this user data to the list for later output
    # I have used an iterator to return a certain number of values entered by the user. I have used list slice.
    # I used an iterator when the length of the list was equal to the number entered by the user
    # and then I used an iterator to display the remaining items
    def iterator(self, N):
        CONST_N = N
        iterable = iter(self.data.values())
        contact_list = []
        num = 0
        while len(contact_list) != len(self.data.values()):
            rec = next(iterable)
            contact_list.append([f'Name: {rec.name.value}, Phones: {rec.phones.value}, Birthday: {rec.birthday.value}'])
            if len(contact_list) == N:
                yield contact_list[num:N]
                num = num + CONST_N
                N += CONST_N
        if N / len(contact_list) != 0:
            yield contact_list[num:]


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

    # Create a new list to fill it with the user's phones, if the user has entered several mobile phones in the list,
    # then we unpack this list and check whether this phone passes the validation, if so, add it to the list,
    # if the list was not filled, then set the value to None if all Normally, then we assign value to this list,
    # if the user simply entered 1 phone number in a string, then we check this phone for correctness and
    # if everything is normal, then we assign value to this phone, if something is wrong, then we assign value None.
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
                    self.__value = []
            except:
                print('Invalid phone format or length, phone must be only digit and 12 numbers!!!')
                self.__value = []
        elif isinstance(new_value, str):
            if len(new_value) == 12 and new_value.isdigit():
                self.__value = [new_value]
                print(f'Number was added successfully: {new_value}!!!')
            else:
                self.__value = []
                print(f'Invalid number: {new_value} for class Phone!!!')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    @property
    def value(self):
        return self.__value

    # We are looking for numbers in the string using the regular, if we get a list with 3 values,
    # we make a datetime object, we get the user's age, and if everything passes the validation,
    # then we assign the value to our datetime object. assign value to None
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
    # Here, in init, I made sure to immediately assign value to the values that enter the class and there was a check on
    # what the user entered so that the user, if he entered incorrect values, would use the setter of certain classes
    def __init__(self, name, phones=Phone(None), birthday=Birthday(None)):
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.birthday.value = birthday.value
        self.phones.value = phones.value

    # We do a check of the phone entered by the user, if everything is fine, then we check whether
    # we had any data in the phone book before, if there was, then we simply append the phone that entered
    # the function to the list, if we had None before this value, then we assign value to our phone.
    # if the phone has not passed the validation, we display an error to the user
    def add_phone(self, phones):
        if len(phones) == 12 and phones.isdigit():
            self.phones.value.append(phones)
            return f'Number was added successfully: {phones}!!!'
        else:
            return f'Invalid phone format or length, phone must be only digit and 12 numbers!!!'

    # We check if we have a phone in the data that needs to be changed if there is,
    # then we check the new phone for correctness If all validations were successful,
    # then we delete the old phone and add a new one, if something is wrong, we return the error to the user
    # if the old number is not in the AddressBook data, then we return user error
    def change_phone(self, old_phone, new_phone):
        if old_phone in self.phones.value:
            if len(new_phone) == 12 and new_phone.isdigit():
                self.phones.value.remove(old_phone)
                self.phones.value.append(new_phone)
                return f'Successfully changed phone for user: {self.name.value}!!'
            else:
                return f'Invalid phone: {new_phone}'
        else:
            return 'Error i dont have such phone in my AddressBook!!'

    # Delete the phone that the user entered if it is in the AddressBook data
    def delete_phone(self, phone):
        if phone in self.phones.value:
            self.phones.value.remove(phone)
            return f'Successfully deleted phone for user: {self.name.value}!!'
        else:
            return 'Error i dont have such phone in my AddressBook!!'

    # We calculate how many days until the birthday of a contact in AddressBook.
    # We change the year to the current one in order to get the correct values,
    # we check whether our user's birthday has already passed or not and return the number of days before the birthday
    def days_to_birthday(self):
        valid_year = self.birthday.value.replace(year=datetime.now().year)
        if valid_year.month < datetime.now().month:
            valid = valid_year - datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {valid.days} days!!!'
        else:
            valid = valid_year - datetime(datetime.now().year, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {valid.days} days!!!'


if __name__ == '__main__':
    Bill = Record(name=Name('Bill'), phones=Phone('4333'), birthday=Birthday('1-1-1998'))  # Invalid number: 43 for class Phone!!!
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
    Petya = Record(name=Name('Petya'), phones=Phone('211111111111'), birthday=Birthday('1-1-1997'))
    Zhenya = Record(name=Name('Zhenya'), phones=Phone('211122222222'), birthday=Birthday('2-1-1897'))  # Invalid date for class Birthday!!!
    Dima = Record(name=Name('Dima'), phones=Phone('333333333333'), birthday=Birthday('3-1-1997'))
    Vasya = Record(name=Name('Vasya'), phones=Phone('444444444444'), birthday=Birthday('4-1-1997'))
    Anton = Record(name=Name('Anton'), phones=Phone('555555555555'), birthday=Birthday('5-1-1997'))
    Zheka = Record(name=Name('Zheka'), phones=Phone('555555555555'), birthday=Birthday('5-1-1997'))
    add_rec = address.add_record([Bill, Petya, Zhenya, Dima, Vasya, Anton])
    address.add_record(Zheka)
    print(add_rec)  # {'Bill': <__main__.Record object at 0x7fea58027ac0>, 'Petya': <__main__.Record object at 0x7fea5801c250>, 'Zhenya': <__main__.Record object at 0x7fea5801c4f0>, 'Dima': <__main__.Record object at 0x7fea5801d9a0>, 'Vasya': <__main__.Record object at 0x7fea5801dd00>, 'Anton': <__main__.Record object at 0x7fea58023040>, 'Zheka': <__main__.Record object at 0x7fea580232b0>}
    address_iterator = address.iterator(4)
    for item in address_iterator:  #  [['Name: Bill, Phones: [], Birthday: 1998-01-01'], ["Name: Petya, Phones: ['211111111111'], Birthday: 1997-01-01"], ["Name: Zhenya, Phones: ['211122222222'], Birthday: None"], ["Name: Dima, Phones: ['333333333333'], Birthday: 1997-01-03"]]
        print(item)                #  [["Name: Vasya, Phones: ['444444444444'], Birthday: 1997-01-04"], ["Name: Anton, Phones: ['555555555555'], Birthday: 1997-01-05"], ["Name: Zheka, Phones: ['555555555555'], Birthday: 1997-01-05"]]
