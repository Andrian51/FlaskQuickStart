from flask import Flask, render_template, url_for, request, redirect, session, flash
from forms.login_form import LoginForm
from forms.registration_form import RegistrationForm

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users_database.db"
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


with app.app_context():
    db.create_all()

user_database = {
    "Andrian": "123456",
    "Bogdan": "123456"
}


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/users/")
def users():
    users_list = [
        {"name": 'Богдан', "username": 'Bogdan'},
        {"name": 'Андріан', "username": 'Andrian'},
    ]
    return render_template(
        'users.html',
        users_list=users_list
    )


@app.route("/users/<string:username>")
def user(username):
    if 'username' in session and session['username'] == username:
        return render_template(
            'user.html',
            username=username
        )
    else:
        return redirect(url_for('login'))


@app.route("/posts")
def posts():
    return render_template('posts.html', posts=range(1, 11))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        username = request.form['username']
        password = request.form['password']

        if username in user_database and user_database[username] == password:
            session['username'] = username
            flash(f'Вітаємо, {username}! ви успішно авторизувалися!')

            return redirect(url_for('user', username=username))
        else:
            flash('Невірний логін або пароль.')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():

        username = request.form['username']
        password = request.form['password']

        new_user = User(
            username=username,
            password=password,
        )
        db.session.add(user)
        db.session.commit()

        if username not in user_database:
            user_database[username] = password
            session['username'] = username
            flash(f"Вітаємо {username}! Ви успішно зареєструвались!")
            return redirect(url_for('user', username=username))
        else:
            flash(f"Користувач з іменем {username} вже існує. Будь ласка, виберіть інше ім'я.")

    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    return render_template('user.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
