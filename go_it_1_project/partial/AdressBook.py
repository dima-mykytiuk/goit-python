import os
import pickle
from collections import UserDict
from typing import Optional, List
from datetime import date, timedelta
import re


class Field:
    """Fields of records in contact book : name , phone/phones , etc."""

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Name(Field):
    """Name class field of class Record"""


class Adress(Field):
    """Name class field of class Record"""


class Phone(Field):
    """Phone of the contact"""

    def __init__(self, value):
        if len(value) == 13 and value[0] == "+" and value[1:].isdigit():
            super().__init__(value)
        else:
            print(
                f"Invalid format for phone: {value}, please enter all phones in format +380123456789"
            )
            self.value = []

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def __str__(self):
        return f"Phone:{self.value}"


class Birthday(Field):
    """Birthday field of cls Record"""

    def __init__(self, value):
        try:
            value = date.fromisoformat(value)
            super().__init__(value)
        except ValueError:
            print("Incorrect format date was given.")
            self.value = None
        except TypeError:
            self.value = None


class Email(Field):
    def __init__(self, value):
        if value is not None:
            if (
                re.match(r"^.+@(\w+\.){0,2}[a-z]{2,6}$", value, re.IGNORECASE)
                is not None
            ):
                super().__init__(value)
            else:
                print(f'Invalid email "{value}"!')
                self.value = None
        else:
            self.value = None


class Address(Field):
    def __init__(self, value):
        if value is not None:
            if value is not None and len(value) > 5:
                super().__init__(value)
            else:
                print(f'Invalid address "{value}" must be more than 5 letters')
                self.value = None
        else:
            self.value = None


class Record:
    """Records(contacts) in users contact book.
    Only one name , but it can be more than one phone"""

    def __init__(
        self,
        name: str,
        phones: List[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> None:
        if phones:
            self.phones = [Phone(p) for p in phones]
        else:
            self.phones = []
        self.birthday = Birthday(birthday)
        self.name = Name(name)
        self.email = Email(email)
        self.address = Address(address)

    def add_phone(self, phone_number: str) -> None:
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def delete_phone(self, phone: str) -> None:
        phone_to_delete = self.__find_phone_single_value(phone)
        self.phones.remove(phone_to_delete) if phone_to_delete else None

    def change_phone(self, old_phone, new_phone) -> None:
        new_phone = Phone(new_phone)
        phone_to_remove = self.__find_phone_single_value(old_phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
            self.phones.append(new_phone)

    def __find_phone_single_value(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"""\nName: {self.name.value}
Phones: {[p.value for p in self.phones]}
Adress: {self.address.value}
Birthday: {self.birthday.value}
Email: {self.email.value}
                   """

    def __repr__(self):
        return f"Record of {self.name.value}, phones {[p.value for p in self.phones]}"

    def get_phones(self):
        return [phone.value for phone in self.phones]

    def add_birthday(self, birthday_date):
        """
        Add 'Birthday' object
        """
        self.birthday = Birthday(birthday_date)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def days_to_birthday(self) -> int:
        """
        If b-day is added: counts days before next one.

        """

        if self.birthday.value is None:
            print(f"No b-day added for {self.name.value}")
            return

        date_now = date.today()
        birthday_date = self.birthday.value
        birthday_date = birthday_date.replace(year=date_now.year)
        # Check if user's birthday passed this year => year + 1
        if birthday_date <= date_now:
            birthday_date = birthday_date.replace(year=date_now.year + 1)
        days_delta = birthday_date - date_now
        return days_delta.days

    def __next__(self):
        return self


class AddressBook(UserDict):
    """All contacts data"""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find_record(self, value: str) -> str:
        if value in self.data.keys():
            return f"{self.data[value].name.value}: phones: {self.data[value].get_phones()}, birthday: {self.data[value].birthday.value}, Email: {self.data[value].email.value}, Address: {self.data[value].address.value}"
        else:
            return f"I do not have such contact: {value}"

    def delete_record(self, value: str) -> None:
        self.data.pop(value)

    def save_data(self, name_file):
        with open(name_file, "wb") as file:
            pickle.dump(self.data, file)

    def load_data(self, name_file):
        if os.path.isfile(name_file) and os.path.getsize(name_file) > 0:
            with open(name_file, "rb") as file:
                self.data = pickle.load(file)

    def __str__(self):
        return str(self.data)

    def show_all_records(self):
        for record in self:
            print(record)

    def __iter__(self):
        return iter(self.data.values())

    def __len__(self) -> int:
        return len(self.data.values())

    def page_iterator(self, number_records: int = 3):
        """
        Generator  n-sized
        """
        records = [record for record in self]
        for i in range(0, len(records), number_records):
            yield records[i : i + number_records]

    def search_subtext(self, subtext: str) -> list:
        """
        Method returns list with records which contains subtext.
        """
        result_records = []
        for record in self:
            if subtext in record.name.value:
                result_records.append(record)

            for phone_number in record.phones:
                if subtext in phone_number.value:
                    result_records.append(record)
        return result_records

    def birthday_in_days(self, step: int = 7) -> List[str]:
        try:
            step = int(step)
        except ValueError:
            raise ValueError("Input a number")
        result = []
        for record in self.data.values():
            if record.birthday and record.birthday.value:
                if record.days_to_birthday() <= step:
                    birthday = f'{record.name.value} {record.birthday.value.strftime("%d-%m-%Y")}'
                    result.append(birthday)
        return result
