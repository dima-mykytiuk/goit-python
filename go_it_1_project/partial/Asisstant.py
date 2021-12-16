import os
import pickle

from AdressBook import *


class Asisstant:
    def __init__(self) -> None:
        self.address_book = AddressBook()
        self.address_book.load_data("data.bin")

    def add_contact(self) -> str:
        name = input("Name is key value, please write name: ")
        while len(name) == 0:
            name = input("Name is key value, please write name: ")
        new_contact = Record(
            name=name, phones=[], birthday=None, email=None, address=None
        )
        self.address_book.add_record(new_contact)
        phone = input("Phone is key value, please write phones: ")
        phones_list = phone.split(",") if phone is not None else []
        while self.address_book[name].get_phones() != phones_list:
            phones_list = phone.split(",") if phone is not None else []
            for item in phones_list:
                self.address_book[name].add_phone(item)
            self.address_book[name].delete_phone(
                []
            )
            if self.address_book[name].get_phones() != phones_list:
                self.address_book[name].phones.clear()
                phone = input("Phone is key value, please write phones: ")
        birthday = input(
            '"OPTIONAL" You can skip this info, just press enter\nWrite birthday: '
        )
        if len(birthday) == 0:
            self.address_book[name].birthday.value = None
        else:
            while str(self.address_book[name].birthday.value) != birthday:
                self.address_book[name].add_birthday(birthday)
                if str(self.address_book[name].birthday.value) != birthday:
                    birthday = input(
                        '"OPTIONAL" You can skip this info, just press enter\nWrite birthday: '
                    )
        email = input(
            '"OPTIONAL" You can skip this info, just press enter\nWrite email: '
        )
        if len(email) == 0:
            self.address_book[name].email.value = None
        else:
            while str(self.address_book[name].email.value) != email:
                self.address_book[name].add_email(email)
                if str(self.address_book[name].email.value) != email:
                    email = input(
                        '"OPTIONAL" You can skip this info, just press enter\nWrite email: '
                    )
        address = input(
            '"OPTIONAL" You can skip this info, just press enter\nWrite address: '
        )
        if len(address) == 0:
            self.address_book[name].address.value = None
        else:
            while str(self.address_book[name].address.value) != address:
                self.address_book[name].add_address(address)
                if str(self.address_book[name].address.value) != address:
                    address = input(
                        '"OPTIONAL" You can skip this info, just press enter\nWrite address: '
                    )
        self.address_book.save_data("data.bin")
        return f"Successfully added contact {name} to contact book"

    def find_contact(self) -> str:
        name = input("Write contact name: ")
        result = self.address_book.find_record(name)
        return result

    def change_contact(self) -> str:
        name = input("Write contact name: ")
        while name not in self.address_book.keys():
            print(f"I do not have {name} contact in my book")
            name = input("Write contact name: ")
        what_change = input("What you want to change?\n")
        if what_change == "phone":
            old_phone = input("Write old phone: ")
            while old_phone not in self.address_book[name].get_phones():
                old_phone = input(
                    f'I do not have such phone: "{old_phone}", write old phone: '
                )
            self.address_book[name].delete_phone(old_phone)
            new_phone = input("Write new phone: ")
            self.address_book[name].add_phone(new_phone)
            while new_phone not in self.address_book[name].get_phones():
                new_phone = input("Write new phone: ")
                self.address_book[name].add_phone(new_phone)
                self.address_book[name].delete_phone([])
            self.address_book.save_data("data.bin")
            return f"Successfully changed {what_change} for contact {name}"
        elif what_change == "name":

            new_name = input("Write new name: ")
            old_record = self.address_book.data[name]
            new_record = Record(
                name=new_name,
                phones=old_record.get_phones(),
                birthday=old_record.birthday.value,
                email=old_record.email.value,
                address=old_record.address.value,
            )
            self.address_book.add_record(new_record)
            self.address_book.delete_record(name)
            self.address_book.save_data("data.bin")
            return f"Successfully changed {what_change} for contact {name}"

        elif what_change == "birthday":
            new_birthday = input("Write new birthday: ")
            while str(self.address_book[name].birthday.value) != new_birthday:
                self.address_book[name].add_birthday(new_birthday)
                if str(self.address_book[name].birthday.value) != new_birthday:
                    new_birthday = input("Write new birthday: ")
            self.address_book.save_data("data.bin")
            return f"Successfully changed {what_change} for contact {name}"
        elif what_change == "email":
            new_email = input("Write new email: ")
            while str(self.address_book[name].email.value) != new_email:
                self.address_book[name].add_email(new_email)
                if str(self.address_book[name].email.value) != new_email:
                    new_email = input("Write new email: ")
            self.address_book.save_data("data.bin")
            return f"Successfully changed {what_change} for contact {name}"
        elif what_change == "address":
            new_address = input("Write new address: ")
            while str(self.address_book[name].address.value) != new_address:
                self.address_book[name].add_address(new_address)
                if str(self.address_book[name].address.value) != new_address:
                    new_address = input("Write new address: ")
            self.address_book.save_data("data.bin")
            return f"Successfully changed {what_change} for contact {name}"

    def del_contact(self) -> str:
        name = input("Write contact name: ")
        while name not in self.address_book.keys():
            print(f"I do not have {name} contact in my book")
            name = input("Write contact name: ")
        self.address_book.delete_record(name)
        print(self.address_book)
        return f"Successfully deleted contact {name} from contact book"

    def get_birthdays(self):
        days = input('For how many days do you want to know the birthdays?\n')
        while days.isdigit() is False:
            days = input('"Error please enter digits"\nFor how many days do you want to know the birthdays?\n')
        days = int(days)
        birthday_list = self.address_book.birthday_in_days(days)
        return birthday_list
