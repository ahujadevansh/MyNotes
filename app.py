from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

db_user = "root"
db_pass = "root"
db_name = "my_notes"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{}:{}@localhost/{}".format(db_user, db_pass, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


@app.route("/")
def index():
    notes_sql = "Select * from notes"
    notes = db.session.execute(notes_sql)
    # print(type(notes))
    # for note in notes:
    #     print(note)
    return render_template('index.html', notes = notes)

@app.route("/create", methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        folders_sql = "Select * from folder"
        folders = db.session.execute(folders_sql)
        return render_template('create.html', folders = folders)
    elif request.method == 'POST':

        form = request.form
        params = {
            "title" : form['title'],
            "content" : form.get('title', ''),
            "folder_id" : form.get('folder_id', ''),
        }
        if not params['folder_id']:
            params['folder_id'] = None
        
        sql = f"insert into notes (`title`, `content`, `folder_id`) values(:title, :content, :folder_id)"
        
        db.session.execute(sql, params)
        db.session.commit()
        return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)