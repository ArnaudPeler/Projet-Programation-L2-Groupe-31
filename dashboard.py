import os
from enum import Enum
from flask import request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, SelectField

from markdown import detect_tag


def get_tags(folder_path: str) -> list[str]:
    """

    :param folder_path: Le chemin du dossier utilisateur duquel on veut rechercher l'ensemble des tags
    :return: La liste de l'ensemble des tags de toutes les notes markdown de l'utilisateur
    """
    tag_list: list[str] = []
    for each in os.listdir(folder_path):
        with open(os.path.join(folder_path, each), 'r') as file:
            file_tags = detect_tag(file.read())
        if file_tags:
            for tag in file_tags:
                if tag not in tag_list:
                    tag_list.append(tag)
            return tag_list


class DashForm(FlaskForm):
    """
    Le formulaire du dashboard
    """
    new_question_name = StringField(render_kw={'placeholder': "New Question"})
    new_question_button = SubmitField("New Question")
    search_text = SearchField(render_kw={'placeholder': "Search"})
    search_button = SubmitField('Search')
    select_tag = SelectField('Tag', choices=['Tag'])
    aggregate_button = SubmitField('Aggregate')


class SubmitType(Enum):
    """
    Une énumération pour aider avec le formulaire du dashboard
    """
    NEW = 'New'
    SEARCH = 'Search'
    AGGREGATE = 'Aggregate'


def get_submit_type(request_form) -> SubmitType:
    """
    Une fonction pour aider avec le formulaire du dashboard
    :param request_form: La variable request.form de flask.request suite à la soumission d'un formulaire
    :return: Une des valeurs de l'énumération SubmitType
    """
    if request_form.get('new_button') == 'New':
        return SubmitType.NEW
    elif request_form.get('search_button') == 'Search':
        return SubmitType.SEARCH
    elif request_form.get('aggregate_button') == 'Aggregate':
        return SubmitType.AGGREGATE


def create_new_question(name, folder) -> None:
    """
    Une fonction pour créer une note markdown
    :param name: nom de la note
    :param folder: dossier où créer la note
    :return: None
    """
    if name == '':
        flash("Name of new question can't be empty!")
    else:
        try:
            with open(os.path.join(folder, name + '.md'), 'x') as new_file:
                pass
        except FileExistsError:
            flash("A question with this name already exist!")


def get_questions_to_aggregate(request_form) -> list[str]:
    """

    :param request_form: La variable request.form de flask.request suite à la soumission d'un formulaire
    :return: La liste des noms des fichier à utiliser pour générer un QCM
    """
    questions = []
    for each in request_form:
        if '_selected' in each:
            questions.append(each.replace('_selected', ''))

    return questions
