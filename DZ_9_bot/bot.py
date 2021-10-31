phone_dict = {
    'Dima': '0106074864', 'Anton': '0206074864', 'Vasya': '0306074864', 'Petya': '0406074864', 'Nikita': '0506074864',
    'Anatolii': '0606074864', 'Nastya': '0706074864', 'Vika': '0806074864', 'Alex': '0906074864', 'Eugene': '1006074864'
}


def input_error(func):
    def inner(command):
        try:
            return func(command)
        except KeyError as key_err:
            return key_err
        except ValueError as val_err:
            return val_err
        except IndexError:
            return f'Give me data for command,name and phone for commands "change" or "add", name for command "phone"'

    return inner


def hello_handler():
    return 'How can i help you?'


@input_error
def add_handler(command):
    split = command.split(' ')
    if split[1].capitalize() not in phone_dict.keys():
        if split[2].isdigit():
            phone_dict[split[1].capitalize()] = split[2]
            return f'Successfully added user phone: {split[1].capitalize()}!!'
        else:
            return f'Phone number must be digit'
    else:
        return f'There is user with that name, change name!!'


@input_error
def change_handler(command):
    split = command.split(' ')
    if split[1].capitalize() in phone_dict.keys():
        if split[2].isdigit():
            phone_dict[split[1].capitalize()] = split[2]
            return f'Successfully changed phone for user: {split[1].capitalize()}!!'
        else:
            return f'Phone number must be digit'
    else:
        return f'There is no user with that name'


@input_error
def show_phone_handler(command):
    split = command.split(' ')
    if phone_dict.get(split[1].capitalize()):
        return f'{phone_dict.get(split[1].capitalize())}'
    else:
        return f'There is no phone with that name, please enter valid name!!'


def show_all_handler():
    full_list = []
    for item in phone_dict.items():
        full_list.append(item)
    return f'{full_list}'


def close():
    return 'Good bye!'


def main():
    user_input_handlers = {
        'add': add_handler,
        'change': change_handler,
        'phone': show_phone_handler,
    }
    default_commands = {
        'help': lambda: f'This bot supports these commands: {", ".join(commands_list)}',
        'hello': hello_handler,
        'show all': show_all_handler,
    }
    commands_list = ['help', 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', 'exit']
    while True:
        user_command = input('Write command: ')
        user_input = user_command.lower()
        if user_input.split()[0] in user_input_handlers.keys():
            print(user_input_handlers.get(user_input.split()[0])(user_command))
        elif user_input in default_commands.keys():
            print(default_commands.get(user_input)())
        elif user_input in ['good bye', 'close', 'exit']:
            print(close())
            break
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
