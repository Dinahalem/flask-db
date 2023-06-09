from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/courses_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __int__(self, name, description):
        self.name = name
        self.description = description


@app.route("/")
def index():
    all_data = Data.query.all()

    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        my_data = Data(name, description)
        db.session.add(my_data)
        db.session.commit()

        flash("Course Added Successfully")
        return redirect(url_for('index'))
    else:
        return redirect(url_for('add.html'))


@app.route("/edit/", methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.description = request.form['description']
        db.session.commit()

        flash("Employee Edited Successfully")
        return redirect(url_for("index"))
    else:
        return render_template("add.html")


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("course Deleted Successfully")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
