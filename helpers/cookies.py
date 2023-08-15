import os

from typing import List, Dict


def get_cookies(cookies_folder_path: str) -> List[List[Dict[str, str]]]:
    """
    Выдает список файлов в папке с куками

    :param cookies_folder_path: Путь до папки с куками
    """

    file_list = [
        cookies_folder_path + file for file in os.listdir(cookies_folder_path)
        if file.endswith('.txt')
    ]

    if not file_list:
        raise Exception("Файлы с куками не найдены")

    return [parse_cookie_from_file(file_path) for file_path in file_list]


def parse_cookie_from_file(cookie_path) -> List[Dict[str, str]]:
    """
    Парсит куки с файла

    :param cookie_path: Путь до файла куки
    """

    cookies = list()

    with open(cookie_path, "r") as file:
        lines = file.read().splitlines()

    for line in lines:
        if line != "# Netscape HTTP Cookie File":
            line = line.strip().split("\t")
            data = dict(name=line[5], value=line[6], domain=line[0], path=line[2], expires=line[4])
            cookies.append(data)

    return cookies
