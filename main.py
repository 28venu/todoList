from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.secret_key = "tolistdo"
db.init_app(app)


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    var = db.Column(db.String)
    status = db.Column(db.String)


with app.app_context():
    db.create_all()



def getsizes():
    with app.app_context():
        total = Todos.query.all()
        x = 0
        y = 0
        for it in total:
            if it.status == "completed":
                y += 1
            x += 1
        db.session.commit()
        print(x)
        print(y)
        return x, y


@app.route('/', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        task = request.form['todotask']
        if task == '':
            flash("enter something to create an todo")
            return redirect(url_for('view'))
        status = 'pending'
        newtodo = Todos(var=task, status=status)
        db.session.add(newtodo)
        db.session.commit()
    tasks = Todos.query.order_by(
        db.case(
            (Todos.status == 'pending', 1),
            (Todos.status == 'completed', 2)
        )
    ).all()

    x, y = getsizes()
    return render_template('view.html', tasks=tasks, a=x, b=y)


@app.route('/update-status/<int:id>', methods=['POST', 'GET'])
def upst(id):
    if request.method == 'POST':
        # status = request.form['status']
        status = 'completed' if request.form.get('status') else 'pending'
        with app.app_context():
            record = db.session.execute(db.select(Todos).where(Todos.id==id)).scalar()
            if status == 'completed':
                record.status = 'completed'
            else:
                record.status = 'pending'
            db.session.commit()
        print(status)
        return redirect(url_for('view'))
    return redirect(url_for('view'))


@app.route('/editing/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'POST':
        editing_todo = request.form['editedtodo']
        with app.app_context():
            required_todo = db.session.execute(db.select(Todos).where(Todos.id == id)).scalar()
            required_todo.var = editing_todo
            db.session.commit()
    return redirect(url_for('view'))


@app.route('/deleting/<int:id>',methods=['GET','POST'])
def deleting(id):
    if request.method == 'GET':
        with app.app_context():
            record = db.session.execute(db.select(Todos).where(Todos.id == id)).scalar();
            if not record is None:
                db.session.delete(record)
                db.session.commit()
            return redirect(url_for('view'))
    return redirect(url_for('view'))


@app.route('/check/<int:id>', methods=['GET', 'POST'])
def check(id):
    if request.form == 'POST':
        return redirect(url_for('home'))
    return redirect(url_for('view'))


if __name__ == '__main__':
    app.run(debug=True)
