import os.path
from typing import NamedTuple
from flask import session
from markdown import detect_tag
class File(NamedTuple):
    name: str
    path: str
    tags: list[str]

def spawn_file(name) -> File:
    _path = os.path.join(session['user_folder'], name)
    with open(_path, 'r') as file:
        markdown_text = file.read()
    _tags = detect_tag(markdown_text)
    return File(name, _path, _tags)

def spawn_files(name_list: list[str]) -> list[File]:
    return [spawn_file(file_name) for file_name in name_list]
