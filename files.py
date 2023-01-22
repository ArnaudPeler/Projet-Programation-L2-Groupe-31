import os.path
from typing import NamedTuple, Tuple
from flask import session
from markdown import detect_tag


class File(NamedTuple):
    """
    Une classe pour représenter les fichier,
    peu utilisé dans sa forme initiale car la session de Flask n'agit pas vraiment comme un dictionnaire normal
    et donc une liste à l'intérieur de la session n'accepte pas les mêmes opérateurs que les listes standard en python,
    les fichiers seront ainsi directement convertis en tuple par Flask
    """
    name: str # ou File[0] si tuple
    path: str # ou File[1] si tuple
    tags: list[str] # ou File[2] si tuple


def spawn_file(_name: str) -> File:
    """
    Permet de générer un fichier de type Fichier à partir d'un nom
    """
    _path = os.path.join(session['user_folder'], _name)
    with open(_path, 'r') as file:
        markdown_text = file.read()
    _tags = detect_tag(markdown_text)
    return File(_name, _path, _tags)


def spawn_files(name_list: list[str]) -> list[File]:
    """
    Permet de générer une liste de fichier à partir d'une liste de nom
    """
    return [spawn_file(file_name) for file_name in name_list]


def get_file_from_name(name: str) -> File:
    """
    Permet de retrouver un fichier dans une liste à partir de son nom
    """
    for file in session['user_files']:
        if file[0] == name:
            return file
