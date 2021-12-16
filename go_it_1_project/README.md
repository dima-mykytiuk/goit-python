# JARVIS
## _Your personal asistant_




Jarvis is your own asisstant with personal notes, contacts and features.

- save contacts / change contacts / expplore your contacts book
- save notes / edit notes / discard your notes
- sort your folder trees
- check your friends birthdays in N upcoming days
- ✨Magic ✨

## Installation

- Copy this repository to your PC
- Change directory to `bot-asisstant`
- Type `pip install -e .`   NOTE: python3 and pip must be installed in your system 
- After installation, type `jarvis` in your command line to see list of commands
- Done! You can use any available command!

# Usage Example


Type `jarvis` to see full list of commands
# 
```sh
jarvis add contact
```
Type name, adress, phones, email of your contact(some fields are optional)
```sh
jarvis show contacts
```
See all records in your contact book

# 
```sh
jarvis add note
```
Type your note, you can add any Tag(optional)
```sh
jarvis show notes
```
See all your notes

```sh
jarvis find note todo
```
Get all your note with todo tag

## Features

_Jarvis can sort your folder tree and check your friends birthdays in next N days_

```sh
jarvis sort folder PATH_TO_FOLDER
```
Organize your folder tree
```sh
jarvis get birthdays 7
```
Check your friends birthdays in upcoming 7 days

----
## Full list of commands

```sh
jarvis add contact
```
-Add contact to your book
```sh
jarvis show contacts
```
-Show contacts in your book
```sh
jarvis find contact {name}
```
-Find contact by name
```sh
jarvis add phone {name}
```
-Add phone to contact's phone list
```sh
jarvis change contact {name}
```
-Change any field in your contact
```sh
jarvis delete contact {name}
```
-Delete your contact
```sh
jarvis get birthdays {days_to}
```
-Check your friends birthdays in next N days 
```sh
jarvis add note
```
-Add note to your notebook
```sh
jarvis show notes
```
-See all your notes
```sh
jarvis find note {id/text/tag}
```
-Find note by any text or id or tag
```sh
jarvis change note {id}
```
-Change text in your note
```sh
jarvis delete note {id}
```
-Delete your note
```sh
jarvis add tags {id}
```
-Add any tag to your note
```sh
jarvis sort folder {path_to_folder}
```
-Sort your folder tree
