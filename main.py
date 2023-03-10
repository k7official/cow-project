from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64
from ultralytics import YOLO
import os

# Load a model
model = YOLO('best_musa.pt')


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

    def __repr__(self):
        return f'<Cow {self.animal_id}>'


class Img(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pic = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<Img {self.title}>'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/identify', methods=["GET", "POST"])
def identify():
    return render_template("identify.html")


@app.route('/predict', methods =["GET", "POST"])
def predict():
    if request.method == "POST":
        # TODO: file is a byte string that represents the contents of the uploaded file.
        #  need to convert it back to image for the format required by the model
        file = request.files['fileUpload'].read()
        print(type(file))
        results = model(file, save=True)  # predict on an image....results not image
        print(results)

        # set the path to the directory where the results will be saved
        results_dir = '/Users/musa.official/PycharmProjects/project-webapp/runs/detect'

        # run the object detection model and save the results to a file in the results_dir directory
        # ...

        # get the list of files in the results_dir directory
        files = os.listdir(results_dir)

        # filter the list of files to include only files starting with 'predict'
        predict_files = [f for f in files if f.startswith('predict')]

        # sort the list of predict_files based on modification time, in descending order
        predict_files.sort(key=lambda x: os.path.getmtime(os.path.join(results_dir, x)), reverse=True)

        # get the latest predict file
        latest_predict_file = predict_files[0]

        # get the full path of the latest predict file
        latest_predict_path = os.path.join(results_dir, latest_predict_file)

        # print the path of the latest predict file....
        # TODO: think about what to do with the predicted path(file), how to show it to non-technical stakeholders
        print('Latest predict file:', latest_predict_path)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_cow = Cow(
            animal_id=request.form["animal_id"],
            ear_tag=request.form["ear_tag"],
            animal_type=request.form["animal_type"],
            breed=request.form["breed"],
            color=request.form["color"],
        )
        file = request.files['pic'].read()
        new_img = Img(id=request.form["animal_id"], pic=file)
        db.session.add(new_img)

        # Add record
        db.session.add(new_cow)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error adding data to database: {e}")
            db.session.rollback()
        finally:
            db.session.close()

        return redirect(url_for('home'))

    return render_template("add_animal.html")


@app.route('/display_all', methods=["GET", "POST"])
def display_all():
    with app.app_context():
        all_cows = db.session.query(Cow).all()
    return render_template('display_all.html', cows=all_cows)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    # UPDATE RECORD
    cow_id = request.args['id']
    cow_to_update = Cow.query.get(cow_id)
    image_object = Img.query.get(cow_id)
    # print(type(image_object))
    image_to_update = image_object.pic
    # print(type(image_to_update))
    encoded_image = base64.b64encode(image_to_update)
    image = encoded_image.decode('UTF-8')
    # print(type(image))
    return render_template('edit.html', cow=cow_to_update, img=image)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables before running the app
    app.run(debug=True)