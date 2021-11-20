from collections import UserDict
import re
from datetime import datetime
import pickle
import os

# Function for saving data
def save_data(name_file):
    with open(name_file, "wb") as file:
        pickle.dump(address, file)
        print('Successfully saved in data')

# A function to open a file with data, if there is such a file and its size is greater than 1
# then we open it and reassign address, if there is no such file, then we use the default address = AddressBook()
def load_data(name_file):
    global address
    if os.path.isfile(name_file) and os.path.getsize(name_file) > 0:
        with open(name_file, 'rb') as file:
            address = pickle.load(file)


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
    def iterator(self, step=10):
        contact_list = []
        for info in self.data.values():
            contact_list.append(f'Name: {info.name.value}, Phones: {info.phones.value}, Birthday: {info.birthday.value}')
        for n in range(0, len(contact_list), step):
            yield contact_list[n:n + step]

    def full_search(self, user_or_phone):
        full_info = []
        # We search by the value of our contacts dictionary
        # if the contact's name is in our dictionary then add the contact data to the full_info string
        for info in self.data.values():
            if user_or_phone in info.name.value:
                full_info.append(
                    f'Name: {info.name.value}, Phones: {info.phones.value}, Birthday: {info.birthday.value}')
        # We search by the value of our contacts dictionary
        # if the contact number is in our dictionary then add the contact data to the full_info string
            elif user_or_phone.isdigit() and len(user_or_phone) > 3:
                for phone in info.phones.value:
                    if user_or_phone in phone:
                        full_info.append(
                            f'Name: {info.name.value}, Phones: {info.phones.value}, Birthday: {info.birthday.value}')
        return full_info


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
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Phone(Field):

    def __init__(self, value):
        super().__init__(value)
        self.value = value

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
                    new_list.append(item) if len(item) == 12 and item.isdigit() else print(f'Invalid number: {item}!!!')
                self.__value = new_list if len(new_list) != 0 else []
            except TypeError:
                print('Invalid phone format or length, phone must be only digit and 12 numbers!!!')
                self.__value = []
        elif isinstance(new_value, str):
            value_valid = len(new_value) == 12 and new_value.isdigit()
            self.__value = [new_value] if value_valid else []
            valid_message = f'Number was added successfully: {new_value}!!!'
            error_message = f'Invalid number: {new_value} for class Phone!!!'
            print(valid_message if value_valid else error_message)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    # We are looking for numbers in the string using the regular, if we get a list with 3 values,
    # we make a datetime object, we get the user's age, and if everything passes the validation,
    # then we assign the value to our datetime object.
    @value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                get_date_numbers = re.findall(r'\d{1,4}', new_value)
                date_format = datetime(int(get_date_numbers[2]), int(get_date_numbers[1]), int(get_date_numbers[0]))
                get_age = datetime.today().year - date_format.year
                if len(get_date_numbers) != 3 or get_age > 100:
                    print('Invalid date for class Birthday!!!')
                    self.__value = None
                else:
                    self.__value = date_format.date()
                    print(f'Successfully set date')
            except IndexError as info:
                print(f"Invalid date for class Birthday!!! {info}")
                self.__value = None
            except TypeError as info:
                print(f"Invalid date for class Birthday!!! {info}")
                self.__value = None
            except ValueError as info:
                print(f"Invalid date for class Birthday!!! {info}")
                self.__value = None


class Record:
    def __init__(self, name, phones=Phone(None), birthday=Birthday(None)):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, phones):
        len(phones) == 12 and phones.isdigit() and self.phones.value.append(phones)
        return f'valid number: {phones}!!!' if len(phones) == 12 and phones.isdigit() else f'Invalid number: {phones}!!!'

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

    def delete_phone(self, phone):
        is_phone_in_contacts = phone in self.phones.value
        is_phone_in_contacts and self.phones.value.remove(phone)
        valid_message = f'Successfully deleted phone for user: {self.name.value}!!'
        error_message = 'Error i dont have such phone in my AddressBook!!'
        return valid_message if is_phone_in_contacts else error_message

    def get_days_to_birthday(self):
        get_valid_year = self.birthday.value.replace(year=datetime.now().year)
        if get_valid_year.month < datetime.now().month:
            get_days = get_valid_year - datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {get_days.days} days!!!'
        else:
            get_days = get_valid_year - datetime(datetime.now().year, datetime.now().month, datetime.now().day).date()
            return f'Birthday in {get_days.days} days!!!'


if __name__ == '__main__':
    pass
