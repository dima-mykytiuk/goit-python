import shutil
from pathlib import Path
import os
from sys import argv, platform
import re


def normalize(name):
    table_symbols = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ', (
        'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
        't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', 'A', 'B', 'V', 'H', 'G', 'D', 'E', 'Ye',
        'Zh', 'Z', 'Y', 'I', 'Yi', 'Y', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', 'KH', 'TS', 'CH', 'SH',
        'SHCH', 'YU', 'YA', 'Y', 'YE', '_', '_', '_', '_', 'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i',
        'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'Kh', 'Ts', 'Ch', 'Sh', 'Shch', 'Yu', 'Aa',
        'y', 'Ye', '_', '_', '_', '_'))
    map_cyr_to_latin = {ord(src): dest for src, dest in zip(*table_symbols)}
    rx = re.compile(r"[^\w_]")
    return rx.sub('_', name.translate(map_cyr_to_latin))


def make_folders():
    for x in range(0, len(folder_list)):
        if not os.path.exists(str(_dir) + folder_sep + folder_list[x]):
            os.makedirs(str(_dir) + folder_sep + folder_list[x])


def move_files(path, item_name, file_type, folder_name, base_path_to):
    if file_type in files_type.get(folder_name) and not os.path.exists(str(path) + folder_name + folder_sep + normalize(
            item_name.removesuffix('.' + file_type)) + '.' + file_type):
        FROM = str(path) + folder_sep + item_name
        TO = str(base_path_to) + folder_sep + folder_name + folder_sep + normalize(
            item_name.removesuffix('.' + file_type)) + '.' + file_type
        shutil.move(FROM, TO)


def find_sort_files(path):
    for item_name in os.listdir(path):
        if item_name not in folder_list:
            if os.path.isfile(path + folder_sep + item_name) and item_name != '.DS_Store':
                file_type = item_name.split('.')[-1]
                for folder_name in folder_list:
                    if folder_name != 'archives':
                        move_files(path, item_name, file_type, folder_name, main_path)
                    elif file_type in files_type.get('archives') and not os.path.exists(
                            str(path) + '/archives/' + normalize(item_name.removesuffix('.' + file_type))):
                        shutil.unpack_archive(str(path) + folder_sep + item_name,
                                              str(main_path) + '/archives/' + normalize(
                                                  item_name.removesuffix('.' + file_type)))
                        os.remove(str(path) + folder_sep + item_name)
            elif os.path.isdir(path + folder_sep + item_name):
                find_sort_files(path + folder_sep + item_name)


def rename_files_and_folders(path):
    for folder_item in os.listdir(path):
        if folder_item not in folder_list:
            if os.path.isfile(path + folder_sep + folder_item) and folder_item != '.DS_Store':
                file_type = folder_item.split('.')[-1]
                if file_type not in files_type.keys():
                    shutil.move(str(path) + folder_sep + folder_item,
                                str(path) + folder_sep + normalize(
                                    folder_item.removesuffix('.' + file_type)) + '.' + file_type)
            elif os.path.isdir(path + folder_sep + folder_item):
                shutil.move(str(path) + folder_sep + folder_item, str(path) + folder_sep + normalize(folder_item))
                rename_files_and_folders(str(path) + folder_sep + normalize(folder_item))


def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, folders, folders_items in walk[::-1]:
        folder_name = path.split(folder_sep)[-1]
        normal_path = folder_name not in folder_list and path == str(_dir) + folder_sep + folder_name
        is_len_0 = len(os.listdir(path)) == 0 and normal_path
        is_len_1 = len(os.listdir(path)) == 1 and '.DS_Store' in folders_items and normal_path
        if is_len_0 or is_len_1:
            shutil.rmtree(path)


if __name__ == '__main__':
    if platform == "win32":
        folder_sep = '//'
    else:
        folder_sep = '/'
    _dir = Path(argv[1])
    main_path = _dir
    folder_list = ['images', 'documents', 'audio', 'video', 'archives']
    files_type = {
        'video': ['avi', 'mp4', 'mov', 'mkv'],
        'audio': ['mp3', 'ogg', 'wav', 'amr'],
        'images': ['jpeg', 'png', 'jpg', 'svg'],
        'archives': ['zip', 'gz', 'tar'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    }
    make_folders()
    find_sort_files(str(_dir))
    rename_files_and_folders(str(_dir))
    remove_empty_folders(_dir)
