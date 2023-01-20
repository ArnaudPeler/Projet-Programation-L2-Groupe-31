import os
from enum import Enum
from flask import request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, SelectField

def get_tags(folder_path):
    tag_list = []
    for each in os.listdir(folder_path):
        with open(os.path.join(folder_path, each), 'r') as file:
            file_tags = detect_tag(file.read())
        if file_tags:
            for tag in file_tags:
                if not tag in tag_list:
                    tag_list.append(tag)
            return tag_list
class DashForm(FlaskForm):
    new_question_name = StringField(render_kw={'placeholder': "New Question"})
    new_question_button = SubmitField("New Question")
    search_text = SearchField(render_kw={'placeholder': "Search"})
    search_button = SubmitField('Search')
    select_tag = SelectField('Tag', choices=['Tag'])
class SubmitType(Enum):
    NEW = 'New'
    SEARCH = 'Search'
    AGGREGATE = 'Aggregate'


def get_submit_type(request_form: request.form) -> SubmitType:
    if request_form.get('new_button') == 'New':
        return SubmitType.NEW
    elif request_form.get('search_button') == 'Search':
        return SubmitType.SEARCH
    elif request_form.get('aggregate_button') == 'Aggregate':
        return SubmitType.AGGREGATE


def create_new_question(name, folder):
    if name == '':
        flash("Name of new question can't be empty!")
    else:
        try:
            with open(os.path.join(folder, name + '.md'), 'x') as new_file:
                pass
        except FileExistsError:
            flash("A question with this name already exist!")
