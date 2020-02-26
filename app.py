from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

# modelo base de datos


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))


@app.route('/chain', methods=['GET'])
def home():

    tasks = Task.query.all()  # mostrar listado completo en home.

    return render_template('index.html', tasks=tasks)


@app.route('/chain', methods=['POST'])
def create():
    # recibe parametro content del formulario y lo guarda en base de datos
    task = Task(content=generate_password_hash(request.form['content']))
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/chain/last', methods=['GET'])
def last():
    last = Task.query.all()
    return str(last[-1].content)


@app.route('/api/v1/chain/', methods=['GET'])
def json():
    tasks = Task.query.all()  # mostrar listado completo en home.
    tasks_json = []
    for i in range(0, len(tasks)-1):
        aux = {
            'index': int(i)+1,
            'hash': tasks[i].content,
        }
        tasks_json.append(aux)

    return render_template('index2.html', tasks=tasks_json)


if __name__ == '__main__':
    # host defecto flask, puerto 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
