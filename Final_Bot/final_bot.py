from HW_12 import AddressBook, Phone, Name, Birthday, Record
import os
import pickle


def input_error(func):
    def inner(command):
        try:
            return func(command)
        except KeyError:
            return f'There is no phone with that name, please enter valid name!!'
        except ValueError:
            return f'Give me name and phone please'
        except IndexError:
            return f'Give me data for command,name and phone for commands "change" or "add", name for command "phone"'

    return inner


@input_error
def add_contact(command):
    name = command[1].capitalize()
    phone = command[2]
    if len(command) == 3:
        new_record = Record(name=Name(name), phones=Phone(phone))
        phone_book.add_record(new_record)
    elif len(command) == 4:
        birthday = command[3]
        new_record = Record(name=Name(name), phones=Phone(phone),birthday=Birthday(birthday))
        phone_book.add_record(new_record)
    return f'Successfully added user {name} to contact list!!'


@input_error
def add_phone_for_contact(command):
    name = command[1].capitalize()
    phone = command[2]
    if name in phone_book:
        phone_book[name].add_phone(phones=phone)
        return f'Successfully added phone for user: {name}!!'
    else:
        return f'{name} user is not found'


@input_error
def del_phone_for_contact(command):
    name = command[1].capitalize()
    phone = command[2]
    if phone in phone_book[name].phones.value:
        phone_book[name].delete_phone(phone=phone)
        return f'Successfully deleted phone: {phone} for user {name}'
    else:
        return f'{name} does not have such phone'


@input_error
def set_birthday(command):
    name = command[1].capitalize()
    birthday = command[2]
    if name in phone_book:
        phone_book[name].birthday.value = birthday
    return f'Successfully set birthday for user {name}'


@input_error
def change_phone(command):
    name = command[1].capitalize()
    old_phone = command[2]
    new_phone = command[3]
    if name in phone_book:
        if old_phone in phone_book[name].phones.value:
            phone_book[name].change_phone(old_phone=old_phone,new_phone=new_phone)
            return f'Successfully changed phone for user {name}!!!'
        else:
            return f'{name} does not have such phone'
    else:
        return f'{name} user is not found'


@input_error
def show_phone(command):
    name = command[1].capitalize()
    return phone_book[name].phones.value


@input_error
def find(command):
    name = command[1].capitalize()
    result = phone_book.full_search(name)
    return result


@input_error
def days_to_birthday(command):
    name = command[1].capitalize()
    result = phone_book[name].get_days_to_birthday()
    return f'{name} {result}'


def show_all():
    for info in phone_book.iterator(4):
        print(info)
    return f'------'


def save_data(name_file):
    with open(name_file, "wb") as file:
        pickle.dump(phone_book, file)
        print(f'Successfully saved in {name_file}')


def load_data(name_file):
    global phone_book
    if os.path.isfile(name_file) and os.path.getsize(name_file) > 0:
        with open(name_file, 'rb') as file:
            phone_book = pickle.load(file)
            print(f'Data was loaded from file {name_file}')


def main():
    file_name = 'data.bin'
    load_data(file_name)
    user_commands = {
        'add': add_contact,
        'change': change_phone,
        'phone': show_phone,
        'add_phone': add_phone_for_contact,
        'set_birthday': set_birthday,
        'find': find,
        'del_phone': del_phone_for_contact,
        'birthday': days_to_birthday,
    }
    default_commands = {
        'help': lambda: f'This bot supports these commands: {", ".join(commands_list)}',
        'hello': lambda: 'How can i help you?',
        'show_all': show_all,
    }

    commands_list = 'help', 'hello', 'add', 'change', 'phone', 'show_all', 'birthday', 'add_phone', 'set_birthday', 'find', 'del_phone', 'good_bye', 'close', 'exit'

    user_command = input('Write command: ')
    while user_command not in ['good_bye', 'close', 'exit']:
        user_input = user_command.lower().split()
        cmd_name = user_input[0]
        if cmd_name in user_commands.keys():
            print(user_commands.get(cmd_name)(user_input))
        elif cmd_name in default_commands.keys():
            print(default_commands.get(cmd_name)())
        else:
            print('Invalid command')
        user_command = input('Write command: ')
    save_data(file_name)
    print('Good bye!')


if __name__ == '__main__':
    phone_book = AddressBook()
    main()
