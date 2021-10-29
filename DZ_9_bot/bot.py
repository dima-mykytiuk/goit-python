phone_dict = {
    'Dima': '0106074864', 'Anton': '0206074864', 'Vasya': '0306074864', 'Petya': '0406074864', 'Nikita': '0506074864',
    'Anatolii': '0606074864', 'Nastya': '0706074864', 'Vika': '0806074864', 'Alex': '0906074864', 'Eugene': '1006074864'
}


def hello_handler():
    return 'How can i help you?'


def add_handler(command):
    split = command.split(' ')
    phone_dict[split[1].capitalize()] = split[2]
    return f'Successfully added user phone: {split[1].capitalize()}!!'


def change_handler(command):
    split = command.split(' ')
    phone_dict[split[1].capitalize()] = split[2]
    return f'Successfully changed phone for user: {split[1].capitalize()}!!'


def show_phone_handler(command):
    split = command.split(' ')
    return f'{phone_dict.get(split[1].capitalize())}'


def show_all_handler():
    full_list = []
    for item in phone_dict.items():
        full_list.append(item)
    return f'{full_list}'


def close():
    return 'Good bye!'


if __name__ == '__main__':
    wait_for_command = True
    while wait_for_command is True:
        user_command = input('Write command: ')
        if user_command.lower() == 'hello':
            print(hello_handler())
        elif user_command.lower().startswith('add '):
            print(add_handler(user_command))
        elif user_command.lower().startswith('change '):
            print(change_handler(user_command))
        elif user_command.lower().startswith('phone '):
            print(show_phone_handler(user_command))
        elif user_command.lower() == ('show all'):
            print(show_all_handler())
        elif user_command.lower() in ["good bye", "close", "exit"]:
            print(close())
            break
