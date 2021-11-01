phone_dict = {
    'Dima': '0106074864', 'Anton': '0206074864', 'Vasya': '0306074864', 'Petya': '0406074864', 'Nikita': '0506074864',
    'Anatolii': '0606074864', 'Nastya': '0706074864', 'Vika': '0806074864', 'Alex': '0906074864', 'Eugene': '1006074864'
}


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


def hello_handler():
    return 'How can i help you?'


@input_error
def add_handler(command):
    phone_dict[command[1].capitalize()] = int(command[2])
    return f'Successfully added user phone: {command[1].capitalize()}!!'


@input_error
def change_handler(command):
    name = command[1].capitalize()
    if name not in phone_dict.keys():
        return phone_dict[name]
    else:
        phone_dict[name] = int(command[2])
        return f'Successfully changed phone for user: {name}!!'


@input_error
def show_phone_handler(command):
    name = command[1].capitalize()
    return phone_dict[name]


def show_all_handler():
    full_list = []
    for item in phone_dict.items():
        full_list.append(item)
    return f'{full_list}'


def main():
    user_commands = {
        'add': add_handler,
        'change': change_handler,
        'phone': show_phone_handler,
    }
    default_commands = {
        'help': lambda: f'This bot supports these commands: {", ".join(commands_list)}',
        'hello': hello_handler,
        'show': show_all_handler,
    }

    commands_list = ['help', 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', 'exit']

    user_command = input('Write command: ')
    while user_command not in ['good bye', 'close', 'exit']:
        user_input = user_command.lower().split()
        name = user_input[0]
        if user_input[0] in user_commands.keys():
            print(user_commands.get(name)(user_input))
        elif user_input[0] in default_commands.keys():
            print(default_commands.get(name)())
        else:
            print('Invalid command')
        user_command = input('Write command: ')
    print('Good bye!')


if __name__ == '__main__':
    main()
