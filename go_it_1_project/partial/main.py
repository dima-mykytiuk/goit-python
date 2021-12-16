import sys
from Asisstant import Asisstant


def main():
    jarvis = Asisstant()
    commands_list = (
        "add_contact",
        "find_contact",
        "change_contact",
        "del_contact",
        "get_birthdays",
        "show_all",
        "birthday",
        "add_phone",
        "set_birthday",
        "find",
        "del_phone",
    )
    if len(sys.argv) == 1:
        print(f'Hello my name is "Jarvis" i am your virtual assistant.\nI am support these commands: {commands_list}')
    cmd = input("Write your command: ").capitalize()
    repl = cmd.replace("Jarvis", "").strip()
    user_commands = {
        "add_contact": jarvis.add_contact,
        "find_contact": jarvis.find_contact,
        "change_contact": jarvis.change_contact,
        "del_contact": jarvis.del_contact,
        "get_birthdays": jarvis.get_birthdays,
    }
    if repl in user_commands.keys():
        print(user_commands.get(repl)())
    else:
        print(f"I do not support this command {repl}")


if __name__ == "__main__":
    main()
