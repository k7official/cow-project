from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cow(db.Model):
    animal_id = db.Column(db.Integer(), primary_key=True)
    ear_tag = db.Column(db.String(100), unique=True, nullable=False)
    animal_type = db.Column(db.String(250), nullable=False)
    breed = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)
    image = db.LargeBinary()

    def __repr__(self):
        return f'<Cow {self.title}>'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/identify', methods=["GET", "POST"])
def identify():
    return render_template("identify.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        if 'image' not in request.files:
            # Handle case where no image is uploaded
            pass
        else:
            image_data = request.files['image'].read()
            encoded_image = base64.b64encode(image_data)
            new_cow = Cow(
                animal_id=request.form["animal_id"],
                ear_tag=request.form["ear_tag"],
                animal_type=request.form["animal_type"],
                breed=request.form["breed"],
                color=request.form["color"],
                image=encoded_image
            )
            with app.app_context():
                db.create_all()
                # Add record
                db.session.add(new_cow)
                db.session.commit()

        return redirect(url_for('home'))

    return render_template("add_animal.html")


if __name__ == "__main__":
    app.run(debug=True)
