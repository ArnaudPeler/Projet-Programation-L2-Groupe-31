import os
from enum import Enum
from typing import NamedTuple
from flask import request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, SelectField

from files import File, spawn_file, get_file_from_name
from markdown import detect_tag

def detect_tag(markdown_content:str) -> list[str]:
    first_line = markdown_content.split('\n')[0]
    if '@' in first_line:
        return first_line.split('@')[1::]
    else:
        return []

def get_tags(files: list[File]) -> list[str]:
    """

    :param files: La liste des fichiers desquelles on cherche l'ensemble des tags
    :return: La liste de l'ensemble des tags de toutes les notes markdown de l'utilisateur
    """
    tag_list = []
    for file in files:
        for tag in file[2] or []:  # file[2] = file.tags
            if tag not in tag_list:
                tag_list.append(tag)

    tag_list.sort()
    return tag_list


class DashForm(FlaskForm):
    """
    Le formulaire du dashboard
    """
    new_name = StringField(render_kw={'placeholder': "New Question"})
    new_button = SubmitField("New Question")
    search_text = SearchField(render_kw={'placeholder': "Search"})
    search_button = SubmitField('Search')
    select_tag = SelectField('All Tags', choices=['All Tags'])
    aggregate_button = SubmitField('Aggregate')
    delete_button = SubmitField('Delete')


class SubmitType(Enum):
    """
    Une énumération pour aider avec le formulaire du dashboard
    """
    NEW = 'New'
    SEARCH = 'Search'
    AGGREGATE = 'Aggregate'
    DELETE = 'Delete'


def get_submit_type(request_form) -> SubmitType:
    """
    Une fonction pour aider avec le formulaire du dashboard
    :param request_form: La variable request.form de flask.request suite à la soumission d'un formulaire
    :return: Une des valeurs de l'énumération SubmitType
    """
    if request_form.get('new_button') == 'New Question':
        return SubmitType.NEW
    elif request_form.get('search_button') == 'Search':
        return SubmitType.SEARCH
    elif request_form.get('aggregate_button') == 'Aggregate':
        return SubmitType.AGGREGATE
    elif request_form.get('delete_button') == 'Delete':
        return SubmitType.DELETE


def create_note(name) -> None:
    """
    Une fonction pour créer une note markdown
    :param name: nom de la nouvelle note
    :return: None
    """
    if name == '' or '.' in name:
        flash("Name of new question can't be empty or contain '.'!")
    else:
        try:
            with open(os.path.join(session['user_folder'], name + '.md'), 'x'):
                session['user_files'] = session['user_files'] + [spawn_file(name + '.md')]  # La session qui casse les couilles

        except FileExistsError:
            flash("A question with this name already exist!")


def delete_files(files: list[File]) -> None:
    """
    Une fonction pour supprimer des fichier
    :param files: La liste des fichier à supprimer
    :return: None
    """
    for file in files:
        session['user_files'] = [each for each in session['user_files'] if each != file]  # La session qui casse les couilles

        os.unlink(file[1])


def get_selected_files(request_form) -> list[File]:
    """

    :param request_form: La variable request.form de flask.request suite à la soumission d'un formulaire
    :return: La liste des fichier sélectionnés
    """
    file_list = []
    for each in request_form:
        if '_selected' in each:
            file_list.append(each.replace('_selected', ''))

    return [get_file_from_name(file) for file in file_list]


def refresh_tags():
    for each in session['user_files']:
        with open(each[1], 'r') as file:
            tags = detect_tag(file.read())

        print()
        if set(tags) != set(each[2] or []):
            # Enlever each de session['user_files'] :
            session['user_files'] = [file for file in session['user_files'] if file != each]
            # Rajouter each actualisé dans session['user_files'] :
            session['user_files'] = session['user_files'] + [spawn_file(each[0])]


def filter_files(files: list[str], name_filter: str, tag_filter: str):
    filtered_files = []
    for file in files:
        print(file[2], '\n', tag_filter)
        if name_filter in file[0] and ((tag_filter in file[2] or []) if tag_filter != 'All Tags' else True):
            filtered_files.append(file)
    return filtered_files

