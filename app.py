from flask import Flask, render_template, url_for, redirect, flash, session, request

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, LoginManager, logout_user
from flask_bcrypt import Bcrypt

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SearchField, SelectField
from wtforms.validators import InputRequired, Length

import os
import mistune
import markdown

from dashboard import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'a-secret-key-here'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User_db.query.get(int(user_id))


class User_db(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User_db.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user'] = user.username
                return redirect(url_for('dashboard'))
            else:
                flash("incorrect password, try again!")
        else:
            flash("Username unknown, try to register first !")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        new_user = User_db(username=form.username.data, password=hashed_pass)
        if User_db.query.filter_by(username=form.username.data).first():
            flash('Username already taken! Please choose another one!')
            return redirect(url_for('register'))
        else:
            db.session.add(new_user)
            db.session.commit()
            try:
                os.mkdir(os.path.join('users', new_user.username))
            except:
                pass
            flash('Thanks for registering, you can now login!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_folder = os.path.join(os.path.split(__file__)[0], 'users', session['user'])
    user_files = [file for file in os.listdir(user_folder) if file.split('.')[1] == 'md']

    dash_form = DashForm()
    dash_form.select_tag.choices.extend(get_tags(user_folder))
    if dash_form.validate_on_submit():
       match get_submit_type(request.form):
        case SubmitType.NEW:
            create_new_question(dash_form.new_question_name, user_folder)
        case SubmitType.SEARCH:
                pass
        case SubmitType.AGGREGATE:
            print(get_questions_to_aggregate())


    return render_template('dashboard_bare.html', user=session['user'], files=user_files, form=dash_form)


class EditorForm(FlaskForm):
    markdown_text = TextAreaField()
    submit = SubmitField("Save")


@app.route('/dashboard/<file>', methods=['GET', 'POST'])
@login_required
def editor(file):
    user_folder = os.path.join(os.path.split(__file__)[0], 'users', session['user'])
    file_path = os.path.join(user_folder, file)
    form = EditorForm()

    if form.validate_on_submit():
        print(form.markdown_text.data)
        with open(file_path, 'w') as markdown_file:
            markdown_file.write(form.markdown_text.data)
    else:
        with open(file_path, 'r') as markdown_file:
            form.markdown_text.data = markdown_file.read()
    html_content = particular_markdown(form.markdown_text.data)

    return render_template('editor.html', render=html_content, form=form)

if __name__ == '__main__':
    app.run(port=8888)

