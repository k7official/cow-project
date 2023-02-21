from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<Img {self.title}>'


@app.route('/')
def home():
    return render_template('index2.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['pic'].read()
        # print(file)
        new_img = Img(pic=file)

        with app.app_context():
            db.create_all()
            # Add record
            db.session.add(new_img)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_image.html')

    # pic = request.form['pic']
    # if not pic:
    #     return 'No pic uploaded!', 400
    #
    # filename = secure_filename(pic.filename)
    #
    # img = Img(img=pic.read())
    # db.session.add(img)
    # db.session.commit()
    #
    # return 'Img Uploaded!', 200


if __name__ == "__main__":
    app.run(debug=True)
