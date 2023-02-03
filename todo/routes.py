import os

from flask import Flask, render_template, request, redirect, url_for
from todo.models import ToDo, db


def create_app():
    """Создаем приложение фласк"""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    return app


app = create_app()


@app.get('/')
def home():
    todo_list = ToDo.query.all()
    return render_template('todo/index.html', todo_list=todo_list, title='Главная страница')


@app.post('/add')
def add():
    title = request.form.get('title')
    if not title:
        return redirect(url_for('home'))
    new_todo = ToDo(title=title, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/update/<int:todo_id>')
def update(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.is_complete = not todo.is_complete
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))
